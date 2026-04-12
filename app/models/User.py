from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.db.base import Base


class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    total_score = Column(int, nullable=False, default=0)
    current_level = Column(int, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))