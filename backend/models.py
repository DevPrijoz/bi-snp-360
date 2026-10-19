"""Modelos persistentes e sessão de dados. SQLite é permitido SOMENTE no piloto local."""
from __future__ import annotations
from datetime import date, datetime, timezone
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
import os


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = "records"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    external_key: Mapped[str | None] = mapped_column(String(160), unique=True, nullable=True)
    module: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(240))
    object_goal: Mapped[str] = mapped_column(Text, default="")
    unit_code: Mapped[str] = mapped_column(String(32), index=True)
    information_unit: Mapped[str] = mapped_column(String(32))
    execution_responsible: Mapped[str] = mapped_column(String(200))
    decision_authority: Mapped[str] = mapped_column(String(200), default="")
    status: Mapped[str] = mapped_column(String(32), default="pendente")
    risk: Mapped[str] = mapped_column(String(32), default="dados_pendentes")
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_action: Mapped[str] = mapped_column(Text, default="")
    decision_required: Mapped[str] = mapped_column(Text, default="")
    source_id: Mapped[str] = mapped_column(String(36))
    source_record_id: Mapped[str] = mapped_column(String(200))
    data_cutoff: Mapped[date] = mapped_column(Date)
    evidence_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    classification: Mapped[str] = mapped_column(String(16), default="interno")
    validation_state: Mapped[str] = mapped_column(String(32), default="pendente")
    published: Mapped[bool] = mapped_column(Boolean, default=False)
    created_by: Mapped[str] = mapped_column(String(200))
    validated_by: Mapped[str | None] = mapped_column(String(200), nullable=True)
    validated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closure_state: Mapped[str] = mapped_column(String(16), default="open")
    closure_action: Mapped[str | None] = mapped_column(Text, nullable=True)
    closure_evidence_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    closure_approved_by: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    audit: Mapped[list["AuditEvent"]] = relationship(back_populates="record")
    __table_args__ = (Index("ix_records_visibility", "classification", "validation_state", "published"),)


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    record_id: Mapped[str] = mapped_column(ForeignKey("records.id"), index=True)
    actor: Mapped[str] = mapped_column(String(200))
    action: Mapped[str] = mapped_column(String(64))
    details: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    record: Mapped[Record] = relationship(back_populates="audit")


DB_URL = os.getenv("DATABASE_URL", "sqlite:///./data/snp360_pilot.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if DB_URL.startswith("sqlite") else {}, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db
