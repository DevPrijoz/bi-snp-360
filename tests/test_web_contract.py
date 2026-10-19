"""Testa o contrato da demo publicada, não os indicadores oficiais."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
WEB=ROOT/'web'

def test_health_declares_demo_only():
    m=json.loads((WEB/'health.json').read_text('utf-8'))
    assert m['synthetic'] is True and m['environment']=='DEMONSTRACAO'
    assert m['institutional_backend'] is False and m['official_integrations']==0

def test_security_headers_and_directory_scope():
    v=json.loads((WEB/'vercel.json').read_text('utf-8'))
    vals={h['key']:h['value'] for h in v['headers'][0]['headers']}
    assert vals['X-Content-Type-Options']=='nosniff'
    assert "frame-ancestors 'none'" in vals['Content-Security-Policy']
    assert "connect-src 'self'" in vals['Content-Security-Policy']

def test_full_navigation_has_source_readiness():
    js=(WEB/'assets/app.js').read_text('utf-8')
    assert "function readiness()" in js
    assert "['readiness','Situação das integrações'" in js
    assert 'Aguardando fonte e homologação' in js

def test_no_backend_in_public_folder():
    assert not (WEB/'backend').exists()
    assert not list(WEB.rglob('*.py'))
    assert not list(WEB.rglob('*.db'))

def test_export_hardens_spreadsheet_formulas():
    js=(WEB/'assets/app.js').read_text('utf-8')
    assert r'[=+@-]' in js

def test_health_and_demo_both_declare_synthetic():
    assert json.loads((WEB/'data/demo_public.json').read_text('utf-8'))['metadata']['synthetic'] is True
