from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "web"


def test_sector_playbook_loaded_in_public_html():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    assert './assets/sector-playbook.js' in html
    assert './assets/sector-playbook.css' in html


def test_all_modules_have_technical_profile():
    js = (WEB / "assets/sector-playbook.js").read_text(encoding="utf-8")
    for name in [
        "Direção Estratégica", "Orçamento e Finanças", "Investimentos e Obras",
        "Outorgas e Contratos", "Planejamento Portuário", "Governança Portuária",
        "Coordenação Institucional", "Processos e Prazos", "Riscos e Controle",
        "Desempenho Setorial", "Dados e Inovação", "Relatórios Executivos",
    ]:
        assert "'" + name + "': {" in js


def test_people_area_contains_no_personal_data():
    js = (WEB / "assets/sector-playbook.js").read_text(encoding="utf-8")
    assert 'Pessoas e Equipes' in js
    assert 'Não divulgar CPF' in js
    data = json.loads((WEB / "data/demo_public.json").read_text(encoding="utf-8"))
    assert data["metadata"]["synthetic"] is True
    assert not (WEB / "diretoria").exists()


def test_health_tracks_ui_and_avoids_claiming_integrations():
    data=json.loads((WEB/'health.json').read_text(encoding='utf-8'))
    assert data['ui_version']=='0.9.0'
    assert data['official_integrations']==0


def test_public_export_is_subset_only(tmp_path):
    from scripts.export_safe_public import export
    from zipfile import ZipFile
    path=export(tmp_path/'site.zip')
    with ZipFile(path) as z:
        names=set(z.namelist())
    assert 'index.html' in names and 'assets/sector-playbook.js' in names
    assert 'data/demo_public.json' in names
    assert not any(n.startswith('diretoria/') or n.startswith('backend/') for n in names)
