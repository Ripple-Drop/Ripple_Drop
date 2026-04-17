import json
from collections.abc import Generator
from pathlib import Path

import pytest
from app.api.deps import get_db
from app.core.config import get_settings
from app.db.base import Base
from app.models import ScenarioSession, User
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def session_factory() -> Generator[sessionmaker[Session]]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        yield testing_session_local
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def scenario_dir(tmp_path: Path) -> Generator[Path]:
    scenarios_path = tmp_path / "scenarios"
    scenarios_path.mkdir()
    (scenarios_path / "airport-smalltalk.json").write_text(
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
    yield scenarios_path


@pytest.fixture
def client(
    session_factory: sessionmaker[Session],
    scenario_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> Generator[TestClient]:
    monkeypatch.setenv("SCENARIO_DIR", str(scenario_dir))
    monkeypatch.setenv("DATABASE", "sqlite")
    monkeypatch.setenv("DATABASE_HOST", "localhost")
    monkeypatch.setenv("DATABASE_USER", "tester")
    monkeypatch.setenv("DATABASE_PASSWORD", "tester")
    monkeypatch.setenv("DATABASE_NAME", "test")
    get_settings.cache_clear()

    def override_get_db() -> Generator[Session]:
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        get_settings.cache_clear()


def test_create_session_success(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    with session_factory() as db:
        user = User(name="tester", email="tester@example.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        user_id = user.id

    response = client.post(
        "/sessions",
        json={"user_id": user_id, "scenario_id": "airport-smalltalk"},
    )

    assert response.status_code == 201
    assert response.json()["scenario_id"] == "airport-smalltalk"

    with session_factory() as db:
        saved_session = db.query(ScenarioSession).filter_by(scenario_id="airport-smalltalk").first()
        assert saved_session is not None
        assert saved_session.user_id == user_id


def test_create_session_returns_404_for_missing_scenario(
    client: TestClient,
    session_factory: sessionmaker[Session],
) -> None:
    response = client.post(
        "/sessions",
        json={"user_id": 1, "scenario_id": "missing-scenario"},
    )

    assert response.status_code == 404

    with session_factory() as db:
        saved_session = db.query(ScenarioSession).first()
        assert saved_session is None
