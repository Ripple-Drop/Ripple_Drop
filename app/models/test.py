# 테스트 ORM 모델. 실제 프로젝트에서는 삭제.

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    message: Mapped[str] = mapped_column(String(255))
