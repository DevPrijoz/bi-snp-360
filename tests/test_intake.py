"""Testes de ingestão sem disponibilização dos dados de origem."""
from pathlib import Path
import csv
import json
import pytest
from scripts.inspect_dataset import inspect, IntakeError


def csv_input(path: Path, records=None):
    fields = ['identificador_linha','exercicio','uo','acao','plano_orcamentario','fonte','dotacao_atualizada','data_corte']
    records = records or [dict(zip(fields, ['1','2026','68101','1234','0001','1000','100.00','2026-10-19']))]
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerows(records)
    return path


def do_inspect(tmp_path, records=None, **changes):
    path = csv_input(tmp_path/'base.csv', records)
    kwargs = dict(contract_name='loa', classification='interno', cutoff='2026-10-19', authorization_ref='TESTE-SINTETICO', output_dir=tmp_path/'manifests')
    kwargs.update(changes)
    return inspect(path, **kwargs)


def test_manifest_no_rows_or_names(tmp_path):
    outcome=do_inspect(tmp_path)
    document=json.loads(Path(outcome['manifest_path']).read_text())
    assert document['rows']==1
    assert len(document['file_sha256'])==64
    assert document['publishable'] is False
    assert document['validation_state']=='pendente_homologacao'
    assert not any('identificador_linha' in str(v) for v in document.values() if isinstance(v, str))


def test_reject_missing_authorization(tmp_path):
    with pytest.raises(IntakeError,match='autorização'):
        do_inspect(tmp_path, authorization_ref='')


def test_reject_duplicated_primary_key(tmp_path):
    rows=[dict(identificador_linha='1',exercicio='2026',uo='68101',acao='1234',plano_orcamentario='0001',fonte='1000',dotacao_atualizada='2.00',data_corte='2026-10-19') for _ in range(2)]
    with pytest.raises(IntakeError,match='duplicada'):
        do_inspect(tmp_path,rows)


def test_reject_bad_date(tmp_path):
    with pytest.raises(IntakeError,match='data_corte'):
        do_inspect(tmp_path,cutoff='2026-10-20')


def test_reject_empty_amount(tmp_path):
    row=dict(identificador_linha='1',exercicio='2026',uo='68101',acao='1234',plano_orcamentario='0001',fonte='1000',dotacao_atualizada='',data_corte='2026-10-19')
    with pytest.raises(IntakeError,match='dotacao_atualizada'):
        do_inspect(tmp_path,[row])


def test_reject_wrong_local_manifest_path(tmp_path):
    root=Path(__file__).resolve().parents[1]
    with pytest.raises(IntakeError,match='local_data'):
        do_inspect(tmp_path,output_dir=root/'web'/'data')
