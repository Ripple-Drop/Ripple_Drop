from datetime import datetime

import pytest
from app.db.base import Base
from app.models.evaluation import Evaluation
from app.models.scenario import ScenarioSession
from app.models.user import User
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
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


def test_evaluation_defaults_and_session_relationship(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario_session = ScenarioSession(user_id=user.id, scenario_id="airport-smalltalk")
    db_session.add(scenario_session)
    db_session.commit()
    db_session.refresh(scenario_session)

    evaluation = Evaluation(session_id=scenario_session.id)
    db_session.add(evaluation)
    db_session.commit()
    db_session.refresh(evaluation)

    queried_evaluation = (
        db_session.query(Evaluation).filter_by(session_id=scenario_session.id).first()
    )

    assert queried_evaluation is not None
    assert queried_evaluation.fluency_score == 0
    assert queried_evaluation.relevance_score == 0
    assert queried_evaluation.continuity_score == 0
    assert queried_evaluation.politeness_score == 0
    assert queried_evaluation.total_score == 0
    assert queried_evaluation.feedback == ""
    assert isinstance(queried_evaluation.created_at, datetime)
    assert queried_evaluation.session.id == scenario_session.id


def test_evaluation_is_one_to_one_per_session(db_session):
    user = User(name="tester", email="tester@example.com")
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    scenario_session = ScenarioSession(user_id=user.id, scenario_id="airport-smalltalk")
    db_session.add(scenario_session)
    db_session.commit()
    db_session.refresh(scenario_session)

    first_evaluation = Evaluation(session_id=scenario_session.id)
    second_evaluation = Evaluation(session_id=scenario_session.id)

    db_session.add(first_evaluation)
    db_session.commit()

    db_session.add(second_evaluation)
    with pytest.raises(IntegrityError):
        db_session.commit()
