from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.messagelog import MessageLog
from app.models.scenario import ScenarioSession
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


def test_message_log_defaults_and_session_relationship(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario_session = ScenarioSession(user_id=user.id, scenario_id="airport-smalltalk")
    db_session.add(scenario_session)
    db_session.commit()
    db_session.refresh(scenario_session)

    message_log = MessageLog(
        session_id=scenario_session.id,
        speaker="ai",
        content="Hello, nice to meet you.",
    )
    db_session.add(message_log)
    db_session.commit()
    db_session.refresh(message_log)

    queried_log = db_session.query(MessageLog).filter_by(speaker="ai").first()

    assert queried_log is not None
    assert queried_log.sequence == 0
    assert isinstance(queried_log.created_at, datetime)
    assert queried_log.session.id == scenario_session.id


def test_message_log_rejects_invalid_speaker(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario_session = ScenarioSession(user_id=user.id, scenario_id="airport-smalltalk")
    db_session.add(scenario_session)
    db_session.commit()
    db_session.refresh(scenario_session)

    invalid_message_log = MessageLog(
        session_id=scenario_session.id,
        speaker="guest",
        content="invalid speaker",
    )
    db_session.add(invalid_message_log)

    with pytest.raises(IntegrityError):
        db_session.commit()
