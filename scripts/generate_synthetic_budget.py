"""Gera exemplos *fictícios* de 4 contratos no diretório ignorado local_data/.

Nunca usar amostras reais para demonstrar o site. Não integra com sistemas oficiais.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path

from scripts.inspect_dataset import ROOT, IntakeError

SYNTHETIC = {
    'loa': [dict(identificador_linha='DEMO-LOA-001', exercicio='2026', uo='00000', acao='DEMO-01',
                 plano_orcamentario='DEMO-PO', fonte='FICTICIA', dotacao_atualizada='100000.00')],
    'execucao': [dict(identificador_linha='DEMO-EXEC-001', exercicio='2026', uo='00000', acao='DEMO-01',
                      plano_orcamentario='DEMO-PO', empenhado='60000.00', liquidado='30000.00', pago='20000.00')],
    'rap': [dict(identificador_linha='DEMO-RAP-001', exercicio_inscricao='2025', uo='00000', acao='DEMO-01',
                rap_inscrito='12000.00', rap_pago='3000.00', rap_cancelado='1000.00')],
    'pagamentos': [dict(identificador_linha='DEMO-PAG-001', exercicio='2026', uo='00000', acao='DEMO-01',
                       tipo_origem='LOA', documento_pagamento='DOC-DEMO', valor_pago='20000.00',
                       data_pagamento='2026-10-01')],
}


def generate(directory: Path, cutoff: str = '2026-10-19') -> list[Path]:
    from datetime import date
    try:
        if date.fromisoformat(cutoff).isoformat() != cutoff:
            raise ValueError()
    except ValueError as exc:
        raise IntakeError('Data inválida; use AAAA-MM-DD.') from exc
    target = directory.resolve()
    allowed = (ROOT / 'local_data').resolve()
    if not (target == allowed or allowed in target.parents):
        raise IntakeError('Geração de CSVs somente dentro de local_data/ ignorado pelo Git.')
    config=json.loads((ROOT/'contracts/datasets.json').read_text(encoding='utf-8'))
    target.mkdir(parents=True, exist_ok=True)
    result=[]
    for contract_id, records in SYNTHETIC.items():
        fields=list(config['datasets'][contract_id]['fields'])
        path=target / f'{contract_id}.csv'
        with path.open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f, fieldnames=fields, delimiter=';', extrasaction='ignore')
            writer.writeheader()
            for row in records:
                writer.writerow({**row,'data_corte':cutoff})
        result.append(path)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=ROOT/'local_data'/'sintetico')
    parser.add_argument('--cutoff', default='2026-10-19')
    args=parser.parse_args()
    try:
        for path in generate(args.output_dir,args.cutoff):print(path)
    except IntakeError as exc:
        parser.exit(2,f'Erro: {exc}\n')
