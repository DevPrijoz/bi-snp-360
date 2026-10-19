"""Teste de autorização por unidade, publicação, trilha e encerramento auditável."""
from __future__ import annotations
from datetime import date
from io import BytesIO
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app, calculate_signal
from backend.models import Base, Record, get_db
from backend.security import Principal, get_principal


@pytest.fixture
def harness(tmp_path):
    db_url=f"sqlite:///{tmp_path/'test.db'}"
    engine=create_engine(db_url,connect_args={'check_same_thread':False})
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine,expire_on_commit=False)
    ctx={'user':Principal(sub='analista-1',unit_codes=['GAB'],permissions=['records:read','records:write','data:import'])}
    def override_db():
        with Session() as db:yield db
    def override_user():return ctx['user']
    app.dependency_overrides[get_db]=override_db
    app.dependency_overrides[get_principal]=override_user
    with TestClient(app) as client:yield client,ctx,Session
    app.dependency_overrides.clear()
    engine.dispose()


def sample(**change):
    values={'external_key':'CASE-001','module':'processos','title':'Processo fictício para validação','object_goal':'Verificação de fluxo e controle de prazo','unit_code':'GAB','information_unit':'GAB','execution_responsible':'Equipe A','status':'pendente','risk':'atencao','due_date':'2026-12-05','next_action':'Submeter dados para validação','source_id':'SEI','source_record_id':'REGISTRO-FICTICIO-100','data_cutoff':'2026-10-19','classification':'interno'}
    values.update(change)
    return values


def set_user(ctx,sub,permissions,units=None):
    ctx['user']=Principal(sub=sub,unit_codes=units if units is not None else ['GAB'],permissions=permissions)


def test_health_and_public_default_empty(harness):
    client,_,_=harness
    assert client.get('/healthz').json()['status']=='ok'
    assert client.get('/api/v1/public/records').json()==[]


def test_create_private_default_not_published_and_audit(harness):
    client,ctx,_=harness
    created=client.post('/api/v1/records',json=sample())
    assert created.status_code==201,created.text
    ident=created.json()['id']
    assert created.json()['validation_state']=='pendente'
    assert created.json()['published'] is False
    assert client.get('/api/v1/public/records').json()==[]
    assert len(client.get('/api/v1/records').json())==1
    assert client.post(f'/api/v1/records/{ident}/publish').status_code==403
    set_user(ctx,'auditor',['records:read','audit:read'])
    audit=client.get(f'/api/v1/audit/{ident}')
    assert audit.status_code==200 and audit.json()[0]['action']=='created'


def test_access_denied_for_wrong_unit_and_restricted(harness):
    client,ctx,_=harness
    assert client.post('/api/v1/records',json=sample(unit_code='DNOP')).status_code==403
    created=client.post('/api/v1/records',json=sample()).json()
    set_user(ctx,'foreign',['records:read'],units=['DGMP'])
    assert client.get('/api/v1/records').json()==[]
    assert client.get('/api/v1/records/'+created['id']).status_code==404
    set_user(ctx,'other',['records:read','records:write'],units=['GAB'])
    assert client.post('/api/v1/records',json=sample(external_key='CASE-002',classification='restrito')).status_code==403


def test_homologation_publication_and_redacted_public_dto(harness):
    client,ctx,_=harness
    r=client.post('/api/v1/records',json=sample(classification='publico')).json()
    url=f"/api/v1/records/{r['id']}"
    assert client.post(url+'/homologate',json={'evidence_url':'https://exemplo.gov.br/evidencia','note':'Homologacao teste'}).status_code==403
    set_user(ctx,'homologador',['records:read','records:homologate','records:publish'])
    response=client.post(url+'/homologate',json={'evidence_url':'https://exemplo.gov.br/evidencia','note':'Evidência conferida no processo'})
    assert response.status_code==200,response.text
    assert client.get('/api/v1/public/records').json()==[]
    publish=client.post(url+'/publish')
    assert publish.status_code==200,publish.text
    public=client.get('/api/v1/public/records').json()
    assert len(public)==1
    assert 'execution_responsible' not in public[0]
    assert 'evidence_url' not in public[0]


def test_creator_cannot_homologate(harness):
    client,ctx,_=harness
    r=client.post('/api/v1/records',json=sample()).json()
    set_user(ctx,'analista-1',['records:read','records:homologate'])
    attempt=client.post(f"/api/v1/records/{r['id']}/homologate",json={'evidence_url':'https://exemplo.gov.br/evidencia','note':'Teste de segregação'})
    assert attempt.status_code==409


def test_closure_cannot_be_color_change(harness):
    client,ctx,_=harness
    r=client.post('/api/v1/records',json=sample()).json()
    url=f"/api/v1/records/{r['id']}"
    assert client.patch(url,json={'status':'concluido'}).status_code==422
    assert client.post(url+'/closure-request',json={'action_taken':'Realizada providência e juntada evidência','evidence_url':'https://exemplo.gov.br/doc'}).status_code==200
    assert client.post(url+'/closure-request',json={'action_taken':'Realizada providência e juntada evidência','evidence_url':'https://exemplo.gov.br/doc'}).status_code==409
    set_user(ctx,'homologador',['records:read','records:homologate'])
    response=client.post(url+'/closure-approve',json={'note':'Providência documental validada'})
    assert response.status_code==200,response.text
    assert response.json()['closure_state']=='approved'
    assert response.json()['status']=='concluido'


def test_import_dry_run_and_idempotent(harness):
    client,ctx,_=harness
    header='external_key;module;title;object_goal;unit_code;information_unit;execution_responsible;status;risk;due_date;next_action;source_id;source_record_id;data_cutoff;classification\n'
    data=header+'CASE-005;processos;Teste de importação;Objeto fictício de teste;GAB;GAB;Equipe de teste;pendente;regular;2026-12-05;Conferir documentação;SEI;REG-005;2026-10-19;interno\n'
    kw={'files':{'file':('demo.csv',data.encode('utf-8'),'text/csv')}}
    preview=client.post('/api/v1/import/csv',data={'dry_run':'true'},**kw)
    assert preview.status_code==200,preview.text
    assert preview.json()['valid_rows']==1 and preview.json()['inserted']==0
    assert client.get('/api/v1/records').json()==[]
    commit=client.post('/api/v1/import/csv',data={'dry_run':'false'},**kw)
    assert commit.status_code==200,commit.text
    assert commit.json()['inserted']==1
    again=client.post('/api/v1/import/csv',data={'dry_run':'false'},**kw)
    assert again.status_code==409


def test_signal_pending_defaults_gray():
    r=Record(validation_state='pendente',risk='critico',status='pendente')
    assert calculate_signal(r,date(2026,10,19))=='dados_pendentes'
    r.validation_state='homologado';r.due_date=date(2026,10,18)
    assert calculate_signal(r,date(2026,10,19))=='critico'


def test_stale_data_remains_gray():
    r=Record(validation_state='homologado',risk='regular',status='em_andamento',data_cutoff=date(2026,7,1),closure_state='open')
    assert calculate_signal(r,date(2026,10,19))=='dados_pendentes'
