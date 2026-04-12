import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

from app.db.base import Base
from app.models.user import User

TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

def test_db_user_creation(db_session):
    user = User(
        name="테스트",
        email="test@mysql.com"
    )
    db_session.add(user)
    db_session.commit()
    queried_user = db_session.query(User).filter_by(name="테스트").first()
    assert queried_user is not None
    assert queried_user.total_score == 0
    assert queried_user.current_level == 0
    assert isinstance(queried_user.created_at, datetime)