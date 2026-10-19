from pathlib import Path
from scripts.release_guard import check_release, ROOT, SECRET_MARKERS


def test_release_guard_clean_repository():
    assert check_release() == []


def test_detect_secret_pattern():
    assert SECRET_MARKERS[0].search('-----BEGIN ' + 'PRIVATE KEY-----')


def test_web_dataset_marked_synthetic():
    text=(ROOT/'web/data/demo_public.json').read_text(encoding='utf-8')
    assert '"synthetic": true' in text
    assert '"environment": "DEMONSTRACA' in text
