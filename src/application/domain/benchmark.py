from datetime import datetime

from sqlalchemy import Index
from sqlalchemy.orm import relationship

from src.infrastructure.utils.extensions import Column, db


class LLM(db.Model):
    __tablename__ = "llms"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False, unique=True, index=True)
    version = Column(db.String)
    created_at = Column(db.DateTime, default=datetime.utcnow)
    updated_at = Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # noqa
    results = relationship("LLMBenchmarkResult", back_populates="llm")


class Metric(db.Model):
    __tablename__ = "metrics"

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False, unique=True, index=True)
    description = Column(db.String)
    unit = Column(db.String)
    created_at = Column(db.DateTime, default=datetime.utcnow)
    min_value = Column(db.Float, nullable=True)
    max_value = Column(db.Float, nullable=True)
    results = relationship("LLMBenchmarkResult", back_populates="metric")


class LLMBenchmarkResult(db.Model):
    __tablename__ = "llm_benchmark_results"

    id = Column(db.Integer, primary_key=True)
    created = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    llm_id = Column(db.Integer, db.ForeignKey("llms.id"), nullable=False, index=True) # noqa
    metric_id = Column(
        db.Integer, db.ForeignKey("metrics.id"), nullable=False, index=True
    )
    value = Column(db.Float, nullable=False)

    llm = relationship("LLM", back_populates="results")
    metric = relationship("Metric", back_populates="results")

    __table_args__ = (Index("ix_llm_metric", "llm_id", "metric_id"),)
