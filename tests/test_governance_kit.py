"""Cobertura dos sete fluxos e proteção contra aprovações fictícias."""
import csv
import json
from pathlib import Path
import pytest
from scripts.governance_kit import GovernanceError, check_handover, workstreams, write_kit, assert_safe_target


def test_seven_workstreams_and_valid_dependencies():
    rows = workstreams()
    assert [x['id'] for x in rows] == [f'P{i:02d}' for i in range(1, 8)]
    assert [r['priority'] for r in rows].count('alta') == 4


def test_generated_kit_has_eight_files_and_no_real_data(tmp_path):
    paths = write_kit(tmp_path)
    assert len(paths) == 8
    with (tmp_path/'matriz_acompanhamento.csv').open(encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f, delimiter=';'))
    assert len(rows) == 7 and all(x['situacao']=='nao_iniciado' for x in rows)
    content = (tmp_path/'solicitacao_P01.md').read_text()
    assert 'a preencher no SEI' in content and 'Não enviar bases internas' in content


def test_cannot_write_governance_kit_in_public_web():
    from scripts.governance_kit import ROOT
    with pytest.raises(GovernanceError,match='local_data'):
        write_kit(ROOT/'web'/'governanca')


def valid():
    return {'workstream_id':'P01','status':'recebido_para_analise','classification':'interno',
            'authorization_reference':'PROCESSO-AUTORIZADO','dictionary_reference':'DICIONARIO-2026',
            'owner_role':'GESTOR-ORCAMENTARIO','cutoff_date':'2026-10-23','official_approval':True}


def test_handover_never_approves_or_publishes_even_when_complete():
    x=check_handover(valid())
    assert x['fields_missing']==[] and x['complete_for_human_review'] is True
    assert x['automatic_approval'] is False and x['publishable'] is False


def test_missing_handover_metadata_blocks_review():
    v=valid();v['dictionary_reference']=''
    x=check_handover(v)
    assert x['complete_for_human_review'] is False
    assert x['fields_missing']==['dictionary_reference']

@pytest.mark.parametrize('key,value',[
    ('status','homologado'),('classification','ultrassecreto'),('workstream_id','P99'),
    ('authorization_reference','Bearer token=XYZ'),('cutoff_date','2026-02-30'),
    ('official_approval','true')])
def test_unauthorized_or_malformed_handover_rejected(key,value):
    v=valid();v[key]=value
    with pytest.raises(GovernanceError):
        check_handover(v)


def test_unknown_metadata_key_rejected():
    v=valid();v['secret']='abc'
    with pytest.raises(GovernanceError):check_handover(v)
