#!/usr/bin/env python3
"""Conferência interna de planilhas SNP, executada APENAS em estação autorizada.

Requer artifact_tool instalado no ambiente local. Não envia nenhum dado pela rede,
não faz commit, não transfere arquivos para o frontend público ou para o backend piloto.

Uso:
 python scripts/analyze_official_workbooks_local.py \
  --history '01 - SÉRIE HISTÓRICA 2019-2026.xlsx' \
  --execution 'Execução Orçamentária  LOA+RAP SNP - 2026.xlsx' \
  --pending 'PROCESSOS PENTENDES.xlsx' \
  --secondary 'Dados secundarios.xlsx' \
  --output-dir /pasta-institucional-protegida --ack-authorized-internal-use
"""
from __future__ import annotations
import argparse
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from backend.official_finance import (
    MONETARY_FIELDS, extract_execution_rows, extract_historical_totals,
    summarize, identify_pending, InvalidFinancialSource,
)

def xdate(raw):
    if isinstance(raw,(int,float)) and not isinstance(raw,bool):
        return (datetime(1899,12,30)+timedelta(days=float(raw))).strftime('%Y-%m-%d')
    return None

def load(path):
    from artifact_tool import Blob, SpreadsheetFile
    return SpreadsheetFile.import_xlsx(Blob.load(str(path)))

def amount_json(x):
    if isinstance(x,Decimal):return format(x,'.2f')
    if isinstance(x,(list,tuple)):return [amount_json(v) for v in x]
    if isinstance(x,dict):return {k:amount_json(v) for k,v in x.items()}
    return x

def main():
    pa=argparse.ArgumentParser(description='Conferência preliminar offline SNP')
    for key in ('history','execution','secondary','pending'):
        pa.add_argument('--'+key,required=True,type=Path)
    pa.add_argument('--output-dir',required=True,type=Path)
    pa.add_argument('--ack-authorized-internal-use',action='store_true')
    args=pa.parse_args()
    if not args.ack_authorized_internal_use:
        pa.error('É obrigatória ciência da autorização e classificação institucional de uso.')
    directory=args.output_dir.expanduser().resolve()
    repo=Path(__file__).resolve().parents[1]
    # Prevent writing to source tree or to public web hosting directory.
    if directory==repo or repo in directory.parents or directory==repo/'web':
        pa.error('NUNCA gravar resultados oficiais dentro do repositório, web/ ou local_data versionado.')
    directory.mkdir(mode=0o700,parents=True,exist_ok=True)
    filenames={k:getattr(args,k).expanduser().resolve() for k in ('history','execution','secondary','pending')}
    for p in filenames.values():
        if not p.is_file():pa.error('Planilha não encontrada: '+str(p))
    wh=load(filenames['history']);we=load(filenames['execution'])
    ws=load(filenames['secondary']);wp=load(filenames['pending'])
    matrix_execution=we.worksheets.get_item_at(0).get_range('A1:AG57').values
    result,total,differences=extract_execution_rows(matrix_execution)
    matrix_historical=wh.worksheets.get_item('Resumo 2019 - 2026').get_range('A1:N247').values
    annual=extract_historical_totals(matrix_historical)
    summary={'cutoff_historical':xdate(matrix_historical[10][13]),'history':annual,
             'totals':total,'differences_to_sheet_total':differences,
             'by_sector':summarize(result,by='sector'),
             'by_action':summarize(result,by='action')}
    # Source-metadata: never assume secondary authorizations represent disbursements.
    secondary=ws.worksheets.get_item_at(0).get_range('A1:H3').values
    secrows=[{'action':str(r[0]),'po':str(r[1]),'description':r[2],
              'process':str(r[3]),'authorization':str(r[4]),
              'authorized':r[5], 'loa':r[6], 'rap':r[7]} for r in secondary[1:] if r[0] is not None]
    sec_rows=wp.worksheets.get_item_at(0).get_range('A1:H7').values
    sga_rows=wp.worksheets.get_item_at(1).get_range('A1:I9').values
    items=identify_pending(sec_rows,'Ordenador') + identify_pending(sga_rows,'SGA')
    summary['sources']={k:{'filename':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in filenames.items()}
    summary['detail_rows']=len(result)
    summary['pending_rows']=len(items)
    summary['pending']=items
    summary['secondary']=secrows
    summary['status']='EM_CONFERENCIA_NAO_HOMOLOGADO'
    summary['privacy']='USO_INTERNO_NAO_PUBLICAR_WEB'
    summary['quality']=[
        'Exigir conciliação independente entre histórico e detalhamento.',
        'Validar campos vazios, estornos e chaves de ação/PO com gestores.',
        'Não contar totais de planilhas como registros adicionais.',
        'Verificar relação entre RAP inscrito, RAP pago e RAP a pagar sem somar como LOA.',
    ]
    dest=directory/'conferencia_restrita.json'
    dest.write_text(json.dumps(amount_json(summary),indent=2,ensure_ascii=False),encoding='utf-8')
    try:os.chmod(dest,0o600)
    except OSError:pass
    print(f'Conferência preliminar em {dest} (arquivo local restrito, não homologado).')
    print(f'Linhas analíticas: {len(result)}; pendências: {len(items)}; divergências de soma: '
          f'{sum(1 for x in differences.values() if x!=0)}')

if __name__=='__main__':
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    main()
