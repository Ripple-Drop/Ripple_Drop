import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api.deps import get_db
from app.db.base import Base
from app.models import ScenarioSession, User
from app.core.config import get_settings
from main import app


def test_create_session_success(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    scenario_dir = tmp_path / "scenarios"
    scenario_dir.mkdir()
    (scenario_dir / "airport-smalltalk.json").write_text(
        json.dumps(
            {
                "id": "airport-smalltalk",
                "title": "Airport Small Talk",
                "description": "Practice a short airport conversation.",
                "persona_name": "Friendly Traveler",
                "persona_description": "Warm and open to conversation.",
                "system_prompt": "You are a friendly traveler at the gate.",
                "difficulty": "easy",
                "time_limit_seconds": 180,
                "opening_message": "Hi, is this seat taken?",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("SCENARIO_DIR", str(scenario_dir))
    get_settings.cache_clear()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    db = TestingSessionLocal()
    user = User(name="tester", email="tester@example.com")
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    client = TestClient(app)
    response = client.post(
        "/sessions",
        json={"user_id": user.id, "scenario_id": "airport-smalltalk"},
    )

    assert response.status_code == 201
    assert response.json()["scenario_id"] == "airport-smalltalk"

    db = TestingSessionLocal()
    saved_session = db.query(ScenarioSession).filter_by(scenario_id="airport-smalltalk").first()
    assert saved_session is not None
    assert saved_session.user_id == user.id
    db.close()

    app.dependency_overrides.clear()
    get_settings.cache_clear()


def test_create_session_returns_404_for_missing_scenario(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    scenario_dir = tmp_path / "scenarios"
    scenario_dir.mkdir()

    monkeypatch.setenv("SCENARIO_DIR", str(scenario_dir))
    get_settings.cache_clear()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    response = client.post(
        "/sessions",
        json={"user_id": 1, "scenario_id": "missing-scenario"},
    )

    assert response.status_code == 404

    db = TestingSessionLocal()
    saved_session = db.query(ScenarioSession).first()
    assert saved_session is None
    db.close()

    app.dependency_overrides.clear()
    get_settings.cache_clear()
