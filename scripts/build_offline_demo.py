"""Produzir HTML autônomo APENAS para apresentação com o JSON sintético versionado."""
from pathlib import Path
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]


def build(output: Path) -> Path:
    source=ROOT/'web/index.html'
    css=(ROOT/'web/assets/styles.css').read_text(encoding='utf-8')
    js=(ROOT/'web/assets/app.js').read_text(encoding='utf-8')
    obj=json.loads((ROOT/'web/data/demo_public.json').read_text(encoding='utf-8'))
    if obj.get('metadata',{}).get('synthetic') is not True or obj['metadata'].get('environment') != 'DEMONSTRACAO':
        raise ValueError('A versão offline aceita exclusivamente base declarada DEMONSTRACAO.')
    expected="fetch('./data/demo_public.json',{cache:'no-store'})"
    if js.count(expected)!=1:
        raise ValueError('A aplicação mudou o ponto de carregamento de dados; revisar manualmente antes de empacotar.')
    js=js.replace(expected,"Promise.resolve({ok:true,json:async()=>window.__SNP_DEMO_DATA__})")
    blob=json.dumps(obj,ensure_ascii=True,separators=(',',':')).replace('<','\\u003c')
    html=source.read_text(encoding='utf-8')
    link='<link rel="stylesheet" href="./assets/styles.css">'
    script='<script src="./assets/app.js" type="module"></script>'
    if link not in html or script not in html:
        raise ValueError('Estrutura HTML incompatível, revisão manual necessária.')
    html=html.replace(link,'<style>\n'+css+'\n</style>')
    html=html.replace(script, '<script>window.__SNP_DEMO_DATA__='+blob+';</script>\n<script type="module">\n'+js+'\n</script>')
    html=re.sub(r'<link rel="icon"[^>]+>', '', html)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(html,encoding='utf-8')
    return output

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parent/'BI_SNP_360_Demonstracao_Offline.html'
    print(build(path))
