from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class MessageLog(Base):
    __tablename__ = "message_logs"
    __table_args__ = (
        CheckConstraint(
            "speaker IN ('user', 'ai', 'system')",
            name="ck_message_logs_speaker",
        ),
    )

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("scenario_sessions.id"), nullable=False, index=True)
    speaker = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    sequence = Column(Integer, nullable=False, default=0)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    session = relationship("ScenarioSession", back_populates="message_logs")
