"""Teste HTTP da demonstração publicada. Execute em runner com acesso à internet."""
import json
import urllib.request
import sys
import time
BASE = 'https://bi-snp-360.vercel.app'

def get(path):
    req=urllib.request.Request(BASE+path,headers={'User-Agent':'BI-SNP-360-Smoke/1.0'})
    with urllib.request.urlopen(req,timeout=25) as res:
        if res.status != 200: raise RuntimeError(f'{path}: HTTP {res.status}')
        return res.read(), dict(res.headers)

if __name__ == '__main__':
    # Vercel inicia o deploy automaticamente após o commit; espere a troca do alias.
    for attempt in range(12):
        try:
            raw,headers=get('/health.json')
            break
        except Exception as exc:
            if attempt==11: raise
            print(f'Aguardando o site publicado ({attempt+1}/12): {exc}',flush=True)
            time.sleep(5)
    o=json.loads(raw)
    assert o['synthetic'] is True and o['environment']=='DEMONSTRACAO' and o['institutional_backend'] is False
    h,_=get('/')
    assert b'BI SNP 360' in h and b'assets/app.js' in h
    j,_=get('/data/demo_public.json')
    d=json.loads(j)
    assert d['metadata']['synthetic'] is True and len(d['records'])==12
    a,_=get('/assets/app.js')
    assert b'function readiness()' in a
    print('OK: HTTPS, HTML, ativos JS, status demonstrativo e JSON publico verificados.')
