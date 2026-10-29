"""Exporta APENAS web/ para novo repositório público (sem histórico Git interno)."""
from __future__ import annotations
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / 'web'
ALLOWED = {'.html', '.js', '.css', '.json', '.svg'}

def export(destination: Path) -> Path:
    meta=json.loads((WEB/'data/demo_public.json').read_text(encoding='utf-8'))['metadata']
    if meta.get('synthetic') is not True or meta.get('environment')!='DEMONSTRACAO':
        raise ValueError('Publicação cancelada: dados não são estritamente fictícios')
    files=[p for p in WEB.rglob('*') if p.is_file()]
    for p in files:
        if p.is_symlink() or not (p.name == '.nojekyll' or p.suffix.lower() in ALLOWED):
            raise ValueError(f'Arquivo não permitido na demonstração: {p}')
        if p.stat().st_size>1_000_000:
            raise ValueError(f'Revisar arquivo maior que 1 MB: {p}')
    data=sorted(str(p.relative_to(WEB)) for p in (WEB/'data').rglob('*') if p.is_file())
    if data != ['data/demo_public.json']:
        raise ValueError(f'Fontes inesperadas na pasta pública: {data}')
    destination.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(destination,'w',ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.relative_to(WEB))
        z.writestr('README_PUBLICACAO.txt',
                   'BI SNP 360 — demonstração pública. Somente dados FICTÍCIOS.\n'
                   'Esta exportação não contém o histórico Git interno.\n'
                   'Hospede a raiz deste ZIP em repositório público NOVO e limpo.\n'
                   'Nunca adicione diretoria/, planilhas oficiais, senhas nem documentos.\n')
    return destination

if __name__=='__main__':
    print(export(ROOT.parent/'BI_SNP_360_DEMO_PUBLICA_LIMPA.zip'))
