"""Guardião de publicação: executar antes de commits, releases e GitHub Pages.

Não substitui revisão de classificação institucional nem scanners de segurança.
"""
from __future__ import annotations
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_SUFFIXES = {'.xlsx', '.xls', '.pdf', '.sqlite', '.db', '.pem', '.pfx', '.p12', '.key'}
SAFE_CSV = {'scripts/exemplo_importacao.csv'}
ALLOWED_WEB_DATA = {'web/data/demo_public.json'}
# Montar nomes de marcadores em segmentos para evitar correspondência no próprio scanner.
SECRET_MARKERS = [
    re.compile('-----BEGIN ' + 'PRIVATE KEY-----'),
    re.compile('ghp_' + r'[A-Za-z0-9]{30,}'),
    re.compile('github_' + 'pat_' + r'[A-Za-z0-9_]{30,}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
]


def tracked_files() -> list[Path]:
    result = subprocess.run(['git','ls-files','-z','--cached','--others','--exclude-standard'], cwd=ROOT,
                            check=True, stdout=subprocess.PIPE)
    return [Path(p.decode('utf-8')) for p in result.stdout.split(b'\0') if p]


def check_release() -> list[str]:
    errors=[]
    data_path=ROOT/'web/data/demo_public.json'
    try:
        data=json.loads(data_path.read_text(encoding='utf-8'))
        meta=data.get('metadata',{})
        if meta.get('synthetic') is not True or meta.get('environment') != 'DEMONSTRACAO':
            errors.append('Snapshot público sem a classificação explícita de demonstração.')
        for rec in data.get('records',[]):
            if rec.get('validation')!='pendente' or rec.get('evidence_url'):
                errors.append('Registro demonstrativo sem bloqueio de validação/evidência.')
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f'Snapshot público inválido: {exc}')
    for relative in tracked_files():
        path=(ROOT/relative)
        if not path.is_file():
            continue
        name=relative.as_posix()
        if (name == '.env' or name.startswith('.env.') and name != '.env.example'
                or name.startswith('local_data/') or name.startswith('data/')
                or relative.suffix.lower() in FORBIDDEN_SUFFIXES):
            errors.append(f'Arquivo confidencial/persistente não permitido no release: {name}')
        if relative.suffix.lower()=='.csv' and name not in SAFE_CSV:
            errors.append(f'CSV não autorizado no repositório: {name}')
        if name.startswith('web/data/') and name not in ALLOWED_WEB_DATA:
            errors.append(f'Arquivo de dados inesperado na demo pública: {name}')
        if path.stat().st_size > 1_000_000:
            errors.append(f'Arquivo maior que 1 MB precisa de revisão explícita: {name}')
        if relative.suffix.lower() in {'.py','.js','.json','.md','.html','.yml','.yaml','.txt','.env','.example','.csv','.css'}:
            try:
                txt=path.read_text('utf-8')
            except UnicodeError:
                errors.append(f'Texto UTF-8 inválido: {name}')
                continue
            if any(pattern.search(txt) for pattern in SECRET_MARKERS):
                errors.append(f'Marcador de segredo detectado: {name}')
    return sorted(set(errors))


def main():
    errors=check_release()
    if errors:
        print('BLOQUEADO — publicação impedida.\n'+ '\n'.join('- '+e for e in errors), file=sys.stderr)
        raise SystemExit(1)
    print('RELEASE VALIDADO — somente arquivos permitidos e snapshot sintético. Revisão humana ainda necessária.')


if __name__=='__main__':
    main()
