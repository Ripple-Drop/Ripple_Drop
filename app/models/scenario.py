from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class ScenarioSession(Base):
    __tablename__ = "scenario_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    scenario_id = Column(String(100), nullable=False, index=True)
    stage_level = Column(Integer, nullable=False, default=0)
    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    ended_at = Column(DateTime(timezone=True), nullable=True)
    total_score = Column(Integer, nullable=False, default=0)
    success = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="scenario_sessions")
    message_logs = relationship(
        "MessageLog",
        back_populates="session",
        cascade="all, delete-orphan",
    )
    evaluation = relationship(
        "Evaluation",
        back_populates="session",
        cascade="all, delete-orphan",
        uselist=False,
    )
