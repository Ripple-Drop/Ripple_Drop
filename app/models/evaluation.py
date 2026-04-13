from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey("scenario_sessions.id"),
        nullable=False,
        unique=True,
        index=True,
    )
    fluency_score = Column(Integer, nullable=False, default=0)
    relevance_score = Column(Integer, nullable=False, default=0)
    continuity_score = Column(Integer, nullable=False, default=0)
    politeness_score = Column(Integer, nullable=False, default=0)
    total_score = Column(Integer, nullable=False, default=0)
    feedback = Column(Text, nullable=False, default="")
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    session = relationship("ScenarioSession", back_populates="evaluation")
