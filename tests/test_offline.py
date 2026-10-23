import pytest
from scripts.build_offline_demo import build


def test_offline_demo_is_standalone_and_fictitious(tmp_path):
    path=build(tmp_path/'demo.html')
    html=path.read_text(encoding='utf-8')
    assert 'window.__SNP_DEMO_DATA__' in html
    assert 'DEMONSTRACAO' in html
    assert 'v0.6.0' in html
    assert 'href="./assets/styles.css"' not in html
    assert 'src="./assets/app.js"' not in html
    assert "fetch('./data/demo_public.json'" not in html
    assert len(html)>20_000
