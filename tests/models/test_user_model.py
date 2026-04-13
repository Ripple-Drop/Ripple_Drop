from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.user import User

TEST_DB_URL = "sqlite:///:memory:"

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
    user = User(name="테스트", email="test@mysql.com")
    db_session.add(user)
    db_session.commit()

    queried_user = db_session.query(User).filter_by(name="테스트").first()

    assert queried_user is not None
    assert queried_user.total_score == 0
    assert queried_user.current_level == 1
    assert isinstance(queried_user.created_at, datetime)


def test_user_email_must_be_unique(db_session):
    first_user = User(name="tester1", email="duplicate@example.com")
    second_user = User(name="tester2", email="duplicate@example.com")

    db_session.add(first_user)
    db_session.commit()

    db_session.add(second_user)
    with pytest.raises(IntegrityError):
        db_session.commit()
