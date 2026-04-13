from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    total_score = Column(Integer, nullable=False, default=0)
    current_level = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))

    scenario_sessions = relationship(
        "ScenarioSession",
        back_populates="user",
        cascade="all, delete-orphan",
    )
