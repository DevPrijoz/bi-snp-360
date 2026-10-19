"""BI SNP 360° — API piloto. Requer OIDC real para todas as operações internas."""
from __future__ import annotations
from datetime import date, timedelta
from typing import Annotated, Literal
from uuid import uuid4
from contextlib import asynccontextmanager
import csv
import io
import json
import os

from fastapi import Depends, FastAPI, HTTPException, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import AuditEvent, Record, get_db, init_db, utc_now
from .security import Principal, get_principal, authorize_record, require

MODULE_IDS = frozenset(['direcao','orcamento','investimentos','outorgas','planejamento','governanca','coordenacao','processos','riscos','desempenho','inovacao','relatorios'])
UNIT_CODES = frozenset(['SNP','GAB','DGMP','DNOP','CGPP','CGGP','CGITD','CGM','CGAP','CGAUT'])
STATUS = frozenset(['pendente','em_andamento','concluido','suspenso'])
RISK = frozenset(['regular','atencao','critico','dados_pendentes'])


def startup_schema():
    # Cuidado: produção requer migrações transacionais, backup e homologação de TI.
    if os.environ.get('SNP_AUTO_CREATE_SCHEMA', '0') == '1':
        init_db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_schema()
    yield


app = FastAPI(title='BI SNP 360° - API Institucional', version='0.2.0', lifespan=lifespan, docs_url='/api/docs', redoc_url=None)


class RecordCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    external_key: str | None = Field(default=None, max_length=160)
    module: str
    title: str = Field(min_length=5, max_length=240)
    object_goal: str = Field(min_length=3, max_length=3000)
    unit_code: str
    information_unit: str
    execution_responsible: str = Field(min_length=2, max_length=200)
    decision_authority: str = Field(default='', max_length=200)
    status: Literal['pendente','em_andamento','concluido','suspenso'] = 'pendente'
    risk: Literal['regular','atencao','critico','dados_pendentes'] = 'dados_pendentes'
    due_date: date | None = None
    next_action: str = Field(min_length=3, max_length=3000)
    decision_required: str = Field(default='', max_length=3000)
    source_id: str = Field(min_length=2, max_length=36)
    source_record_id: str = Field(min_length=2, max_length=200)
    data_cutoff: date
    evidence_url: HttpUrl | None = None
    classification: Literal['publico','interno','restrito'] = 'interno'

    @field_validator('module')
    @classmethod
    def valid_module(cls, value):
        if value not in MODULE_IDS: raise ValueError('Módulo desconhecido')
        return value

    @field_validator('unit_code','information_unit')
    @classmethod
    def valid_unit(cls, value):
        if value not in UNIT_CODES: raise ValueError('Unidade não cadastrada (validar SIORG)')
        return value


class RecordView(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    external_key: str | None
    module: str
    title: str
    unit_code: str
    information_unit: str
    execution_responsible: str
    status: str
    risk: str
    due_date: date | None
    next_action: str
    decision_required: str
    source_id: str
    source_record_id: str
    data_cutoff: date
    classification: str
    validation_state: str
    published: bool
    closure_state: str


class PublicRecord(BaseModel):
    """DTO de transparência não inclui responsável pessoal, documentos nem dados internos."""
    model_config = ConfigDict(from_attributes=True)
    id: str
    module: str
    title: str
    unit_code: str
    status: str
    risk: str
    source_id: str
    data_cutoff: date


class Homologation(BaseModel):
    evidence_url: HttpUrl
    note: str = Field(min_length=8, max_length=500)


class ClosureRequest(BaseModel):
    action_taken: str = Field(min_length=8, max_length=2000)
    evidence_url: HttpUrl


class ClosureApproval(BaseModel):
    note: str = Field(min_length=8, max_length=500)


class RecordPatch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    status: Literal['pendente','em_andamento','suspenso'] | None = None
    risk: Literal['regular','atencao','critico','dados_pendentes'] | None = None
    due_date: date | None = None
    next_action: str | None = Field(default=None, min_length=3, max_length=3000)
    decision_required: str | None = Field(default=None, max_length=3000)


def audit(db: Session, record: Record, actor: str, action: str, detail: str = ''):
    db.add(AuditEvent(record_id=record.id, actor=actor, action=action, details=detail[:500]))


def get_existing(db: Session, record_id: str) -> Record:
    record = db.get(Record, record_id)
    if not record: raise HTTPException(404, 'Registro não encontrado.')
    return record


def require_unit(user: Principal, unit: str):
    if unit not in user.unit_codes and 'records:write:all' not in user.permissions:
        raise HTTPException(403, 'Unidade não autorizada.')


@app.get('/healthz')
def healthz():
    return {'status':'ok','api':'snp360','version':'0.2.0','demo_data_enabled':False}


@app.get('/api/v1/public/records', response_model=list[PublicRecord])
def public_records(db: Annotated[Session, Depends(get_db)]):
    # Consulta de transparência exige 3 condições E não revela dados pessoais/evidências.
    records = db.scalars(select(Record).where(Record.classification=='publico', Record.validation_state=='homologado', Record.published==True)).all()
    return records


@app.get('/api/v1/me')
def me(user: Annotated[Principal, Depends(get_principal)]):
    return user


@app.get('/api/v1/records', response_model=list[RecordView])
def list_records(user: Annotated[Principal, Depends(get_principal)], db: Annotated[Session, Depends(get_db)], module: str | None=None, unit_code: str | None=None):
    require('records:read',user)
    q=select(Record)
    if module:
        if module not in MODULE_IDS: raise HTTPException(422,'Módulo inválido.')
        q=q.where(Record.module==module)
    if unit_code: q=q.where(Record.unit_code==unit_code)
    if 'records:read:all' not in user.permissions:
        q=q.where(Record.unit_code.in_(user.unit_codes or ['--none--']))
    if 'records:restricted:read' not in user.permissions:
        q=q.where(Record.classification!='restrito')
    return db.scalars(q.limit(1000)).all()


@app.get('/api/v1/records/{record_id}', response_model=RecordView)
def get_record(record_id:str, user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record)
    return record


@app.post('/api/v1/records',response_model=RecordView,status_code=201)
def create_record(body:RecordCreate,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    require('records:write',user)
    require_unit(user,body.unit_code)
    if body.classification=='restrito' and 'records:restricted:write' not in user.permissions:
        raise HTTPException(403,'Escrita restrita não autorizada.')
    record=Record(**{**body.model_dump(exclude={'evidence_url'}), 'evidence_url':str(body.evidence_url) if body.evidence_url else None},id=str(uuid4()),created_by=user.sub,validation_state='pendente',published=False,closure_state='open')
    db.add(record); audit(db,record,user.sub,'created')
    try: db.commit()
    except IntegrityError as err:
        db.rollback();raise HTTPException(409,'Identificador externo já cadastrado.') from err
    db.refresh(record)
    return record


@app.patch('/api/v1/records/{record_id}',response_model=RecordView)
def patch_record(record_id:str,body:RecordPatch,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record,'write')
    if record.closure_state=='approved':raise HTTPException(409,'Registro encerrado requer reabertura formal.')
    changes=body.model_dump(exclude_unset=True)
    if not changes:raise HTTPException(422,'Nenhuma alteração informada.')
    for key,value in changes.items():setattr(record,key,value)
    record.validation_state='pendente';record.published=False
    audit(db,record,user.sub,'updated',','.join(changes.keys()))
    db.commit();db.refresh(record)
    return record


@app.post('/api/v1/records/{record_id}/homologate',response_model=RecordView)
def homologate(record_id:str,body:Homologation,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record,'homologate')
    if record.created_by==user.sub:raise HTTPException(409,'Segregação de funções: autor não pode homologar o próprio registro.')
    record.validation_state='homologado';record.validated_by=user.sub;record.validated_at=utc_now();record.evidence_url=str(body.evidence_url)
    audit(db,record,user.sub,'homologated',body.note)
    db.commit();db.refresh(record)
    return record


@app.post('/api/v1/records/{record_id}/publish',response_model=RecordView)
def publish(record_id:str,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record,'publish')
    if record.classification!='publico' or record.validation_state!='homologado':raise HTTPException(409,'Só é possível publicar registros públicos homologados.')
    record.published=True;audit(db,record,user.sub,'published');db.commit();db.refresh(record)
    return record


@app.post('/api/v1/records/{record_id}/closure-request',response_model=RecordView)
def closure_request(record_id:str,body:ClosureRequest,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record,'write')
    if record.closure_state!='open':raise HTTPException(409,'Há encerramento em trâmite ou homologado.')
    record.closure_state='requested';record.closure_action=body.action_taken;record.closure_evidence_url=str(body.evidence_url)
    record.validation_state='pendente';record.published=False
    audit(db,record,user.sub,'closure_requested','evidência informada')
    db.commit();db.refresh(record)
    return record


@app.post('/api/v1/records/{record_id}/closure-approve',response_model=RecordView)
def closure_approve(record_id:str,body:ClosureApproval,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record,'homologate')
    if record.closure_state!='requested' or not record.closure_evidence_url or not record.closure_action:raise HTTPException(409,'Sem providência e evidência, não há encerramento.')
    if record.created_by==user.sub:raise HTTPException(409,'Segregação de funções: autor não pode homologar encerramento.')
    record.closure_state='approved';record.status='concluido';record.closure_approved_by=user.sub
    record.validation_state='homologado';record.validated_by=user.sub;record.validated_at=utc_now()
    audit(db,record,user.sub,'closure_approved',body.note)
    db.commit();db.refresh(record)
    return record


def calculate_signal(record:Record, cutoff:date) -> str:
    if record.validation_state!='homologado':return 'dados_pendentes'
    # Regra conservadora do piloto; ambiente real exige vigência por fonte homologada.
    if record.data_cutoff and (cutoff-record.data_cutoff).days > 60:return 'dados_pendentes'
    if record.closure_state=='approved':return 'regular'
    if record.risk=='critico' or (record.status!='concluido' and record.due_date and record.due_date < cutoff):return 'critico'
    if record.risk=='atencao' or (record.status!='concluido' and record.due_date and record.due_date <= cutoff+timedelta(days=7)):return 'atencao'
    return 'regular' if record.risk=='regular' else 'dados_pendentes'


@app.get('/api/v1/alerts')
def alerts(user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    records=list_records(user,db)
    cutoff=date.today()
    return [{'id':r.id,'unit_code':r.unit_code,'signal':calculate_signal(r,cutoff),'due_date':r.due_date} for r in records]


IMPORT_FIELDS=['external_key','module','title','object_goal','unit_code','information_unit','execution_responsible','status','risk','due_date','next_action','source_id','source_record_id','data_cutoff','classification']
@app.post('/api/v1/import/csv')
async def import_csv(user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)],file:UploadFile=File(...),dry_run:bool=Form(True)):
    require('data:import',user)
    if not file.filename or not file.filename.lower().endswith('.csv'):raise HTTPException(422,'Somente CSV com extensão .csv.')
    blob=await file.read(2_000_001)
    if len(blob)>2_000_000:raise HTTPException(413,'Limite máximo de 2 MB.')
    try:
        data=blob.decode('utf-8-sig')
        reader=csv.DictReader(io.StringIO(data),delimiter=';')
        if not reader.fieldnames or not all(f in reader.fieldnames for f in IMPORT_FIELDS):raise ValueError('Colunas obrigatórias ausentes')
        prepared=[]
        for n,row in enumerate(reader,2):
            if n>1001:raise ValueError('Importação limitada a 1.000 linhas')
            if not row.get('external_key'):raise ValueError(f'Linha {n}: external_key obrigatório')
            parsed=RecordCreate.model_validate({**{k:row.get(k) or None for k in IMPORT_FIELDS},'decision_required':row.get('decision_required') or '', 'decision_authority':row.get('decision_authority') or ''})
            require_unit(user,parsed.unit_code)
            if parsed.classification=='restrito' and 'records:restricted:write' not in user.permissions:raise HTTPException(403,'Importação restrita não autorizada.')
            prepared.append(parsed)
        keys=[r.external_key for r in prepared]
        if len(keys)!=len(set(keys)):raise ValueError('Há chaves externas duplicadas no próprio arquivo')
        if keys and db.scalars(select(Record.external_key).where(Record.external_key.in_(keys))).first():raise HTTPException(409,'Chave externa já existe: importação recusada, sem substituição automática.')
        if not dry_run:
            for item in prepared:
                obj=Record(**{**item.model_dump(exclude={'evidence_url'}),'evidence_url':str(item.evidence_url) if item.evidence_url else None},id=str(uuid4()),created_by=user.sub,validation_state='pendente',published=False,closure_state='open')
                db.add(obj);audit(db,obj,user.sub,'imported')
            db.commit()
        return {'dry_run':dry_run,'valid_rows':len(prepared),'inserted':0 if dry_run else len(prepared),'message':'Sem substituição ou publicação automática; homologação necessária.'}
    except (UnicodeError,ValueError) as err:
        db.rollback();raise HTTPException(422,str(err)) from err
    except IntegrityError as err:
        db.rollback();raise HTTPException(409,'Duplicidade na importação.') from err


@app.get('/api/v1/audit/{record_id}')
def audit_history(record_id:str,user:Annotated[Principal,Depends(get_principal)],db:Annotated[Session,Depends(get_db)]):
    record=get_existing(db,record_id)
    authorize_record(user,record)
    require('audit:read',user)
    events=db.scalars(select(AuditEvent).where(AuditEvent.record_id==record_id).order_by(AuditEvent.created_at)).all()
    return [{'action':e.action,'actor':e.actor,'at':e.created_at,'details':e.details} for e in events]
