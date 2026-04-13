from datetime import datetime

import pytest
from app.db.base import Base
from app.models.scenario import ScenarioSession
from app.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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


def test_scenario_session_defaults_and_user_relationship(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario_session = ScenarioSession(
        user_id=user.id,
        scenario_id="airport-smalltalk",
    )
    db_session.add(scenario_session)
    db_session.commit()
    db_session.refresh(scenario_session)

    queried_session = (
        db_session.query(ScenarioSession).filter_by(scenario_id="airport-smalltalk").first()
    )

    assert queried_session is not None
    assert queried_session.stage_level == 0
    assert queried_session.total_score == 0
    assert queried_session.success is False
    assert isinstance(queried_session.started_at, datetime)
    assert queried_session.ended_at is None
    assert queried_session.user.id == user.id
