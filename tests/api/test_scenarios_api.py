from fastapi.testclient import TestClient

from app.api import scenarios as scenarios_api
from app.schemas import ScenarioDefinition
from app.services import ScenarioNotFoundError, ScenarioValidationError
from main import app


def _build_scenario(*, scenario_id: str, title: str, difficulty: str) -> ScenarioDefinition:
    return ScenarioDefinition(
        id=scenario_id,
        title=title,
        description=f"{title} description.",
        persona_name=f"{title} Persona",
        persona_description=f"{title} persona description.",
        system_prompt=f"{title} prompt.",
        difficulty=difficulty,
        time_limit_seconds=120,
        opening_message=f"{title} opening message.",
    )


def test_list_scenarios_returns_list_items(monkeypatch):
    scenarios = [
        _build_scenario(scenario_id="airport-smalltalk", title="Airport Small Talk", difficulty="easy"),
        _build_scenario(scenario_id="cafe-chat", title="Cafe Chat", difficulty="medium"),
    ]

    class StubScenarioLoader:
        def list_scenarios(self) -> list[ScenarioDefinition]:
            return scenarios

    monkeypatch.setattr(scenarios_api, "ScenarioLoader", StubScenarioLoader)

    client = TestClient(app)
    response = client.get("/scenarios")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "airport-smalltalk",
            "title": "Airport Small Talk",
            "description": "Airport Small Talk description.",
            "difficulty": "easy",
            "time_limit_seconds": 120,
        },
        {
            "id": "cafe-chat",
            "title": "Cafe Chat",
            "description": "Cafe Chat description.",
            "difficulty": "medium",
            "time_limit_seconds": 120,
        },
    ]


def test_list_scenarios_returns_500_when_loader_validation_fails(monkeypatch):
    class StubScenarioLoader:
        def list_scenarios(self) -> list[ScenarioDefinition]:
            raise ScenarioValidationError("broken scenario data")

    monkeypatch.setattr(scenarios_api, "ScenarioLoader", StubScenarioLoader)

    client = TestClient(app)
    response = client.get("/scenarios")

    assert response.status_code == 500
    assert response.json() == {"detail": "broken scenario data"}


def test_get_scenario_returns_definition(monkeypatch):
    scenario = _build_scenario(
        scenario_id="airport-smalltalk",
        title="Airport Small Talk",
        difficulty="easy",
    )

    class StubScenarioLoader:
        def get_scenario(self, scenario_id: str) -> ScenarioDefinition:
            assert scenario_id == "airport-smalltalk"
            return scenario

    monkeypatch.setattr(scenarios_api, "ScenarioLoader", StubScenarioLoader)

    client = TestClient(app)
    response = client.get("/scenarios/airport-smalltalk")

    assert response.status_code == 200
    assert response.json() == {
        "id": "airport-smalltalk",
        "title": "Airport Small Talk",
        "description": "Airport Small Talk description.",
        "persona_name": "Airport Small Talk Persona",
        "persona_description": "Airport Small Talk persona description.",
        "system_prompt": "Airport Small Talk prompt.",
        "difficulty": "easy",
        "time_limit_seconds": 120,
        "opening_message": "Airport Small Talk opening message.",
    }


def test_get_scenario_returns_404_when_not_found(monkeypatch):
    class StubScenarioLoader:
        def get_scenario(self, scenario_id: str) -> ScenarioDefinition:
            raise ScenarioNotFoundError(f"Scenario not found: {scenario_id}")

    monkeypatch.setattr(scenarios_api, "ScenarioLoader", StubScenarioLoader)

    client = TestClient(app)
    response = client.get("/scenarios/missing-scenario")

    assert response.status_code == 404
    assert response.json() == {"detail": "Scenario not found: missing-scenario"}


def test_get_scenario_returns_500_when_validation_fails(monkeypatch):
    class StubScenarioLoader:
        def get_scenario(self, scenario_id: str) -> ScenarioDefinition:
            raise ScenarioValidationError(f"Failed to load scenario: {scenario_id}.json")

    monkeypatch.setattr(scenarios_api, "ScenarioLoader", StubScenarioLoader)

    client = TestClient(app)
    response = client.get("/scenarios/broken-scenario")

    assert response.status_code == 500
    assert response.json() == {"detail": "Failed to load scenario: broken-scenario.json"}
