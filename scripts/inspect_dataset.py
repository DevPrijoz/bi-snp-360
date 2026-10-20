"""Validar um CSV autorizado sem publicá-lo; gerar SOMENTE manifesto de ingestão local.

Uso: python scripts/inspect_dataset.py BASE.csv --contract loa --classification interno
      --cutoff 2026-10-19 --authorization-ref PROCESSO-AUTORIZADO --output-dir local_data/manifests
O CSV jamais é escrito no frontend nem versionado.
"""
from __future__ import annotations
import argparse
import csv
from datetime import date
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / 'contracts' / 'datasets.json'
ALLOWED_CLASS = {'publico', 'interno', 'restrito'}

class IntakeError(ValueError):
    pass


def validate_field(value: str, kind: str) -> bool:
    """Não supor zeros ou interpretar moeda brasileira sem dicionário homologado."""
    if kind.endswith('_optional') and not value.strip():
        return True
    if not value.strip():
        return False
    kind = kind.removesuffix('_optional')
    if kind == 'string':
        return len(value) <= 3000
    if kind == 'year':
        return len(value) == 4 and value.isdigit() and 2000 <= int(value) <= 2100
    if kind == 'date':
        try:
            date.fromisoformat(value)
            return len(value) == 10
        except ValueError:
            return False
    if kind == 'origem_pagamento':
        return value in {'LOA', 'RAP'}
    if kind == 'decimal':
        try:
            d = Decimal(value)
            return d.is_finite() and len(value) <= 36
        except InvalidOperation:
            return False
    raise IntakeError(f'Tipo de campo não suportado no contrato: {kind}')


def inspect(path: Path, contract_name: str, classification: str, cutoff: str, authorization_ref: str,
            output_dir: Path, max_bytes: int = 50_000_000) -> dict:
    if classification not in ALLOWED_CLASS:
        raise IntakeError('Classificação inválida.')
    if not authorization_ref or len(authorization_ref.strip()) < 5:
        raise IntakeError('Referência à autorização ou licença da fonte é obrigatória.')
    try:
        date.fromisoformat(cutoff)
    except ValueError as exc:
        raise IntakeError('Data de corte inválida; usar AAAA-MM-DD.') from exc
    config = json.loads(CONTRACTS.read_text(encoding='utf-8'))
    if contract_name not in config['datasets']:
        raise IntakeError(f'Contrato não localizado: {contract_name}')
    contract = config['datasets'][contract_name]
    if not path.is_file() or path.suffix.lower() != '.csv':
        raise IntakeError('Fonte deve ser arquivo CSV existente.')
    if path.stat().st_size > max_bytes:
        raise IntakeError('Arquivo excede o tamanho máximo permitido de 50 MB.')
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    duplicates = set()
    count = 0
    cutoff_count = 0
    with path.open('r', encoding='utf-8-sig', newline='') as stream:
        reader = csv.DictReader(stream, delimiter=';', strict=True)
        fields = contract['fields']
        if reader.fieldnames is None or not set(fields).issubset(set(reader.fieldnames)):
            raise IntakeError('Cabeçalho incompatível com os campos do contrato, delimitador ;.')
        if len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise IntakeError('Cabeçalho possui colunas duplicadas.')
        for line, record in enumerate(reader, start=2):
            if None in record:
                raise IntakeError(f'Linha {line}: quantidade inesperada de colunas.')
            for field, kind in fields.items():
                value = record.get(field)
                if value is None or not validate_field(value, kind):
                    raise IntakeError(f'Linha {line}: valor inválido no campo {field}.')
            key = tuple(record[field] for field in contract['primary_key'])
            if key in duplicates:
                raise IntakeError(f'Linha {line}: chave primária duplicada.')
            duplicates.add(key)
            count += 1
            if record.get('data_corte') == cutoff:
                cutoff_count += 1
            else:
                raise IntakeError(f'Linha {line}: data_corte divergente do corte informado.')
    if not count:
        raise IntakeError('Não aceitar dataset vazio.')
    manifest = {
        'manifest_version': '1', 'contract_version': config['contract_version'],
        'source_id': contract['source_id'], 'contract_id': contract_name,
        'file_sha256': digest.hexdigest(), 'rows': count, 'cutoff': cutoff,
        'classification': classification, 'authorization_ref': authorization_ref.strip(),
        'unit': contract['unit'], 'primary_key': contract['primary_key'],
        'validation_state': 'pendente_homologacao',
        'publishable': False,
        'notes': 'Manifesto técnico: não homologado, não publicado e sem conciliação automática.'
    }
    output_dir = output_dir.resolve()
    if output_dir == ROOT or ROOT in output_dir.parents and output_dir.parts[:len(ROOT.parts) + 1] != (*ROOT.parts, 'local_data'):
        raise IntakeError('Manifestos gerados dentro do projeto devem ficar somente em local_data/ ignorado pelo Git.')
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f'{contract_name}-{uuid.uuid4().hex}.json'
    output_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {'manifest_path': str(output_file), 'rows': count, 'sha256': digest.hexdigest(), 'status': 'pendente_homologacao'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', type=Path)
    parser.add_argument('--contract', required=True)
    parser.add_argument('--classification', choices=sorted(ALLOWED_CLASS), required=True)
    parser.add_argument('--cutoff', required=True)
    parser.add_argument('--authorization-ref', required=True)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'local_data' / 'manifests')
    args = parser.parse_args()
    try:
        report = inspect(args.file, args.contract, args.classification, args.cutoff, args.authorization_ref, args.output_dir)
    except (IntakeError, UnicodeError, csv.Error) as exc:
        print(f'ERRO: {exc}', file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
