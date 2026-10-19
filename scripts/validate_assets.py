from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'web/data/demo_public.json').read_text('utf-8'))
assert data['metadata']['synthetic'] is True and data['metadata']['environment']=='DEMONSTRACAO'
modules={'direcao','orcamento','investimentos','outorgas','planejamento','governanca','coordenacao','processos','riscos','desempenho','inovacao','relatorios'}
units={u['code'] for u in data['units']}
ids=set()
for record in data['records']:
    assert record['id'] not in ids;ids.add(record['id'])
    assert record['module'] in modules and record['unit'] in units
    assert record['validation']=='pendente' and not record['evidence_url']
print(f'VALIDADO: {len(data["records"])} registros DEMO; {len(units)} unidades; {len(data["sources"])} fontes previstas.')
