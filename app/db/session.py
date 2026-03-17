from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# SQLAlchemy 설정
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)  # echo=True는 SQL 쿼리를 로그로 출력.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # 세션 클래스 생성

