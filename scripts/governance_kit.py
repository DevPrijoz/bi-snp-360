"""Gera kit inicial de solicitações e confere metadados de recebimento SEM dados brutos.

Este utilitário não cria autorizações, não consulta SEI e não altera situação oficial.
"""
from __future__ import annotations

import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'contracts' / 'governance_workstreams.json'
ALLOWED_STATUS = {'nao_iniciado', 'solicitado', 'recebido_para_analise', 'em_homologacao'}
ALLOWED_CLASS = {'publico', 'interno', 'restrito', 'a_definir'}

class GovernanceError(ValueError):
    pass


def workstreams() -> list[dict]:
    obj = json.loads(CATALOG.read_text(encoding='utf-8'))
    items = obj['workstreams']
    keys = [i['id'] for i in items]
    if len(items) != 7 or len(keys) != len(set(keys)):
        raise GovernanceError('Catálogo de prioridades deve ter sete IDs únicos.')
    for item in items:
        if any(dep not in keys or dep == item['id'] for dep in item['dependencies']):
            raise GovernanceError('Dependência inválida.')
    return items


def assert_safe_target(folder: Path) -> Path:
    target = folder.resolve()
    # Evita criar prontuários ou relatórios de recebimento sob áreas publicadas/versionadas.
    if target == ROOT or (ROOT in target.parents and not (target == ROOT / 'local_data' or ROOT / 'local_data' in target.parents)):
        raise GovernanceError('Dentro do projeto, gerar resultados apenas em local_data/.')
    return target


def write_kit(folder: Path) -> list[Path]:
    target = assert_safe_target(folder)
    items = workstreams()
    target.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in items:
        text = (f'# BI SNP 360° — Solicitação {i["id"]}: {i["title"]}\n\n'
                '**MODELO DE TRABALHO — não é ofício expedido nem autorização concedida.**\n\n'
                f'**Prioridade:** {i["priority"]}  \n**Destinatário proposto:** {i["owner_proposed"]}  \n'
                f'**Referência de processo institucional:** [a preencher no SEI]  \n'
                '**Ponto focal institucional:** [a designar]  \n**Situação:** Não iniciada\n\n'
                f'## Texto sugerido\n\nSolicita-se a avaliação da viabilidade de {i["request"].lower()} '
                'O fornecimento e o tratamento das informações dependem da autorização da unidade gestora, '
                'da classificação e de ambiente corporativo aprovado. Não enviar bases internas ao GitHub, '
                'Vercel ou ferramentas públicas.\n\n'
                '## Documentos/definições a solicitar\n\n' + ''.join(f'- [ ] {e}\n' for e in i['required_evidence']) +
                f'\n## Critério de aceite\n\n{i["acceptance"]}\n\n'
                f'**Dependências:** {", ".join(i["dependencies"]) or "Nenhuma"}\n\n'
                '## Registro da resposta\n\n- Protocolo da decisão: [a preencher no ambiente institucional]\n'
                '- Data do aceite: [a preencher]\n- Gestor que homologou: [a preencher]\n'
                '- Evidências e localização institucional: [a preencher]\n')
        p = target / f'solicitacao_{i["id"]}.md'
        p.write_text(text, encoding='utf-8')
        paths.append(p)
    matrix = target / 'matriz_acompanhamento.csv'
    with matrix.open('w', encoding='utf-8-sig', newline='') as output:
        writer = csv.writer(output, delimiter=';', quoting=csv.QUOTE_ALL)
        writer.writerow(['id', 'prioridade', 'assunto', 'responsavel_proposto', 'dependencias', 'situacao', 'protocolo_interno', 'prazo_acordado'])
        for i in items:
            writer.writerow([i['id'], i['priority'], i['title'], i['owner_proposed'], ','.join(i['dependencies']), 'nao_iniciado', '', ''])
    paths.append(matrix)
    return paths


def check_handover(data: dict) -> dict:
    """Valida apenas protocolo de RECEBIMENTO, nunca a autenticidade da autorização.

    Não recebe dados brutos, pessoas, números oficiais, segredos nem anexos.
    """
    ids = {x['id'] for x in workstreams()}
    allowed = {'workstream_id', 'status', 'classification', 'authorization_reference',
               'dictionary_reference', 'owner_role', 'cutoff_date', 'official_approval'}
    if not isinstance(data, dict) or set(data) != allowed:
        raise GovernanceError('Formato de metadados inválido: somente os oito campos documentados.')
    if data['workstream_id'] not in ids or data['status'] not in ALLOWED_STATUS:
        raise GovernanceError('Trilha ou estado inválido.')
    if data['classification'] not in ALLOWED_CLASS or type(data['official_approval']) is not bool:
        raise GovernanceError('Classificação ou marcação de aprovação inválida.')
    for key in ('authorization_reference', 'dictionary_reference', 'owner_role'):
        value = data[key]
        if not isinstance(value, str) or len(value)>120 or any(ord(c)<32 for c in value):
            raise GovernanceError(f'Campo {key} deve conter referência curta, sem dados pessoais ou anexos.')
        if re.search(r'(?:password|token|senha|secret|-----BEGIN)', value, re.I):
            raise GovernanceError('Possível segredo em campo de referência.')
    cutoff = data['cutoff_date']
    if cutoff:
        if not isinstance(cutoff, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', cutoff):
            raise GovernanceError('Data de corte inválida.')
        try:
            date.fromisoformat(cutoff)
        except ValueError as exc:
            raise GovernanceError('Data de corte inválida.') from exc
    missing = [k for k in ('authorization_reference', 'dictionary_reference', 'owner_role', 'cutoff_date') if not data[k]]
    # Booleano declaratório NÃO concede aprovação formal. Sempre exige conferência humana.
    return {'workstream_id': data['workstream_id'], 'status': data['status'],
            'fields_missing': missing, 'complete_for_human_review': not missing,
            'automatic_approval': False, 'publishable': False,
            'notes': 'Metadados somente; aprovação e integridade devem ser confirmadas por gestor autorizado.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    kit = sub.add_parser('kit', help='Gerar solicitações e planilha de acompanhamento sem dados reais.')
    kit.add_argument('--output-dir', type=Path, default=ROOT / 'local_data' / 'governanca')
    val = sub.add_parser('conferir', help='Conferir metadados, nunca dados brutos, nem conceder homologação.')
    val.add_argument('file', type=Path)
    args = parser.parse_args()
    try:
        if args.action == 'kit':
            result = {'created': len(write_kit(args.output_dir)), 'location': str(args.output_dir), 'official_approvals': 0}
        else:
            if args.file.stat().st_size > 8_192:
                raise GovernanceError('Metadados excedem o limite de tamanho.')
            result = check_handover(json.loads(args.file.read_text(encoding='utf-8')))
    except (GovernanceError, FileNotFoundError, json.JSONDecodeError) as exc:
        parser.exit(2, f'Recusado: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
