from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    scenario_id = Column(String(100), nullable=False)
    stage_level = Column(Integer, nullable=False, default=0)
    started_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    ended_at = Column(DateTime(timezone=True), nullable=True)
    total_score = Column(Integer, nullable=False, default=0)
    success = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="scenarios")
    message_logs = relationship(
        "MessageLog",
        back_populates="scenario",
        cascade="all, delete-orphan",
    )
