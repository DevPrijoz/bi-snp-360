"""Conferência conjunta LOA + execução + RAP + pagamentos, sem importar dados.

Conferência de estrutura por contrato e data de corte. NÃO concilia registros e
NÃO atesta legitimidade da autorização. Emite somente um relatório local com
contagens/hashes; não copia, envia ou expõe valores financeiros de origem.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
import json
import os
from pathlib import Path
import tempfile
from uuid import uuid4

from scripts.inspect_dataset import IntakeError, ROOT, inspect

CONTRACT_ORDER = ('loa', 'execucao', 'rap', 'pagamentos')


def prepare(files: dict[str, Path], *, classification: str, cutoff: str,
            authorization_ref: str, output_dir: Path) -> dict:
    if set(files) != set(CONTRACT_ORDER):
        raise IntakeError('O pacote orçamentário exige LOA, execução, RAP e pagamentos.')
    try:
        if date.fromisoformat(cutoff).isoformat() != cutoff:
            raise ValueError('Data fora do formato ISO')
    except ValueError as exc:
        raise IntakeError('Data de corte inválida; usar AAAA-MM-DD.') from exc
    target = output_dir.resolve()
    permitted = (ROOT / 'local_data').resolve()
    if target == ROOT or (ROOT in target.parents and target != permitted and permitted not in target.parents):
        raise IntakeError('Relatórios dentro do projeto só são permitidos em local_data/.')

    # Cada arquivo é conferido integralmente, sem produzir saída final parcial.
    results = []
    with tempfile.TemporaryDirectory(prefix='snp_budget_check_') as temporary:
        for contract_id in CONTRACT_ORDER:
            outcome = inspect(Path(files[contract_id]), contract_id, classification, cutoff,
                              authorization_ref, Path(temporary))
            manifest = json.loads(Path(outcome['manifest_path']).read_text(encoding='utf-8'))
            results.append({
                'contract_id': contract_id,
                'source_id': manifest['source_id'],
                'rows': manifest['rows'],
                'file_sha256': manifest['file_sha256'],
                'contract_version': manifest['contract_version'],
                'validation_state': manifest['validation_state'],
            })

    package = {
        'schema_version': 1,
        'package_id': str(uuid4()),
        'scope': 'LOA + execução + RAP + pagamentos',
        'cutoff': cutoff,
        'classification': classification,
        'authorization_ref': authorization_ref.strip(),
        'validation_state': 'pendente_homologacao',
        'publishable': False,
        'official_values_computed': False,
        'reconciliation_performed': False,
        'notes': 'Somente conferência estrutural. Não há junção, apuração ou homologação de valores oficiais.',
        'datasets': results,
    }
    target.mkdir(parents=True, exist_ok=True)
    final_path = target / f'pacote-orcamentario-{package["package_id"]}.json'
    # Gravação atômica do relatório único, que contém hashes e contagens, não linhas.
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target,
                                     prefix='.incompleto-', suffix='.tmp', delete=False) as temp:
        temp_path = Path(temp.name)
        try:
            json.dump(package, temp, ensure_ascii=False, indent=2)
            temp.write('\n')
        except BaseException:
            temp_path.unlink(missing_ok=True)
            raise
    os.replace(temp_path, final_path)
    return {'report_path': str(final_path), 'datasets': len(results),
            'rows_checked': sum(x['rows'] for x in results),
            'status': 'pendente_homologacao', 'publishable': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in CONTRACT_ORDER:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--classification', choices=['publico', 'interno', 'restrito'], required=True)
    parser.add_argument('--cutoff', required=True)
    parser.add_argument('--authorization-ref', required=True)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'local_data' / 'manifests')
    args = parser.parse_args()
    try:
        outcome = prepare({name: getattr(args, name) for name in CONTRACT_ORDER},
                          classification=args.classification, cutoff=args.cutoff,
                          authorization_ref=args.authorization_ref, output_dir=args.output_dir)
    except (IntakeError, OSError, UnicodeError, ValueError, csv.Error) as exc:
        parser.exit(2, f'Conferência recusada: {exc}\n')
    print(json.dumps(outcome, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
