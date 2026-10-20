"""Pacote orçamentário sintético; nenhuma fonte do MPOR é utilizada."""
from pathlib import Path
import json
import pytest

from scripts.generate_synthetic_budget import generate, SYNTHETIC
from scripts.prepare_budget_package import prepare
from scripts.inspect_dataset import IntakeError, inspect


def make_paths(tmp_path):
    # O gerador é limitado a local_data; testes usam subdiretório temporário
    # com o mesmo contrato e o mesmo formato, sem arquivos oficiais.
    import csv
    from scripts.inspect_dataset import CONTRACTS
    config=json.loads(CONTRACTS.read_text(encoding='utf-8'))
    paths={}
    for kind, rows in SYNTHETIC.items():
        path=tmp_path/f'{kind}.csv'
        fields=list(config['datasets'][kind]['fields'])
        with path.open('w',encoding='utf-8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields,delimiter=';',extrasaction='ignore')
            writer.writeheader()
            for row in rows:
                writer.writerow({**row,'data_corte':'2026-10-19'})
        paths[kind]=path
    return paths


def run(paths, tmp_path, **kwargs):
    config=dict(classification='interno',cutoff='2026-10-19',
                authorization_ref='TESTE-SINTETICO',output_dir=tmp_path/'report')
    config.update(kwargs)
    return prepare(paths,**config)


def test_four_dataset_package_without_raw_records(tmp_path):
    report=run(make_paths(tmp_path),tmp_path)
    obj=json.loads(Path(report['report_path']).read_text(encoding='utf-8'))
    assert len(obj['datasets'])==4
    assert {x['contract_id'] for x in obj['datasets']}=={'loa','execucao','rap','pagamentos'}
    assert obj['publishable'] is False and obj['reconciliation_performed'] is False
    assert obj['official_values_computed'] is False
    assert all(len(x['file_sha256'])==64 for x in obj['datasets'])
    assert 'DOC-DEMO' not in json.dumps(obj)
    assert '100000.00' not in json.dumps(obj)


def test_missing_payment_data_rejected_without_partial_report(tmp_path):
    paths=make_paths(tmp_path)
    paths.pop('pagamentos')
    with pytest.raises(IntakeError,match='quatro|pagamentos|pacote orçamentário'):
        run(paths,tmp_path)
    assert not (tmp_path/'report').exists()


def test_bad_payment_type_rejected_without_partial_report(tmp_path):
    paths=make_paths(tmp_path)
    p=paths['pagamentos']
    p.write_text(p.read_text().replace('LOA','DESCONHECIDO'),encoding='utf-8')
    with pytest.raises(IntakeError,match='tipo_origem'):
        run(paths,tmp_path)
    assert not (tmp_path/'report').exists()


def test_date_cutoff_conflict_fails_all_or_nothing(tmp_path):
    paths=make_paths(tmp_path)
    p=paths['rap']
    p.write_text(p.read_text().replace('2026-10-19','2026-10-18'),encoding='utf-8')
    with pytest.raises(IntakeError,match='data_corte'):
        run(paths,tmp_path)
    assert not (tmp_path/'report').exists()


def test_missing_auth_rejected_and_no_report(tmp_path):
    with pytest.raises(IntakeError,match='autorização'):
        run(make_paths(tmp_path),tmp_path,authorization_ref='')
    assert not (tmp_path/'report').exists()


def test_output_outside_local_data_if_inside_repo_rejected(tmp_path):
    from scripts.inspect_dataset import ROOT
    with pytest.raises(IntakeError,match='local_data'):
        run(make_paths(tmp_path),tmp_path,output_dir=ROOT/'web'/'reports')


def test_generated_samples_local_data_only():
    from scripts.inspect_dataset import ROOT
    with pytest.raises(IntakeError,match='local_data'):
        generate(ROOT/'web'/'samples')


def test_payments_contract_can_be_checked_in_isolation(tmp_path):
    paths=make_paths(tmp_path)
    res=inspect(paths['pagamentos'],'pagamentos','interno','2026-10-19',
                'TESTE-SINTETICO',tmp_path/'manifest')
    assert res['status']=='pendente_homologacao' and res['rows']==1
