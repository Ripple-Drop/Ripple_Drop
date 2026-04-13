from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.evaluation import Evaluation
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


def test_evaluation_defaults_and_scenario_relationship(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario = Scenario(user_id=user.id, scenario_id="airport-smalltalk")
    db_session.add(scenario)
    db_session.commit()
    db_session.refresh(scenario)

    evaluation = Evaluation(scenario_id=scenario.id)
    db_session.add(evaluation)
    db_session.commit()
    db_session.refresh(evaluation)

    queried_evaluation = db_session.query(Evaluation).filter_by(scenario_id=scenario.id).first()

    assert queried_evaluation is not None
    assert queried_evaluation.fluency_score == 0
    assert queried_evaluation.relevance_score == 0
    assert queried_evaluation.continuity_score == 0
    assert queried_evaluation.politeness_score == 0
    assert queried_evaluation.total_score == 0
    assert queried_evaluation.feedback == ""
    assert isinstance(queried_evaluation.created_at, datetime)
    assert queried_evaluation.scenario.id == scenario.id
