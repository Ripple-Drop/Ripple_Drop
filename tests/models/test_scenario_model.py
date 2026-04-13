from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.scenario import Scenario
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


def test_scenario_defaults_and_user_relationship(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario = Scenario(user_id=user.id, scenario_id="airport-smalltalk")
    db_session.add(scenario)
    db_session.commit()
    db_session.refresh(scenario)

    queried_scenario = db_session.query(Scenario).filter_by(scenario_id="airport-smalltalk").first()

    assert queried_scenario is not None
    assert queried_scenario.stage_level == 0
    assert queried_scenario.total_score == 0
    assert queried_scenario.success is False
    assert isinstance(queried_scenario.started_at, datetime)
    assert queried_scenario.ended_at is None
    assert queried_scenario.user.id == user.id
