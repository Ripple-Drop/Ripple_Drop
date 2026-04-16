import json

import pytest

from app.services import (
    ScenarioLoader,
    ScenarioNotFoundError,
    ScenarioValidationError,
)


def test_get_scenario_returns_valid_definition(tmp_path):
    scenario_path = tmp_path / "airport-smalltalk.json"
    scenario_path.write_text(
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

    loader = ScenarioLoader(tmp_path)
    scenario = loader.get_scenario("airport-smalltalk")

    assert scenario.id == "airport-smalltalk"
    assert scenario.title == "Airport Small Talk"


def test_list_scenarios_returns_sorted_definitions(tmp_path):
    first_path = tmp_path / "z-last.json"
    first_path.write_text(
        json.dumps(
            {
                "id": "z-last",
                "title": "Last Scenario",
                "description": "Last scenario description.",
                "persona_name": "Last Persona",
                "persona_description": "Last persona description.",
                "system_prompt": "Last prompt.",
                "difficulty": "easy",
                "time_limit_seconds": 120,
                "opening_message": "Last opening message.",
            }
        ),
        encoding="utf-8",
    )

    second_path = tmp_path / "a-first.json"
    second_path.write_text(
        json.dumps(
            {
                "id": "a-first",
                "title": "First Scenario",
                "description": "First scenario description.",
                "persona_name": "First Persona",
                "persona_description": "First persona description.",
                "system_prompt": "First prompt.",
                "difficulty": "medium",
                "time_limit_seconds": 90,
                "opening_message": "First opening message.",
            }
        ),
        encoding="utf-8",
    )

    loader = ScenarioLoader(tmp_path)
    scenarios = loader.list_scenarios()

    assert [scenario.id for scenario in scenarios] == ["a-first", "z-last"]


def test_get_scenario_raises_not_found_for_missing_file(tmp_path):
    loader = ScenarioLoader(tmp_path)

    with pytest.raises(ScenarioNotFoundError):
        loader.get_scenario("missing-scenario")


def test_get_scenario_raises_validation_error_for_invalid_json(tmp_path):
    scenario_path = tmp_path / "broken.json"
    scenario_path.write_text("{ invalid json", encoding="utf-8")

    loader = ScenarioLoader(tmp_path)

    with pytest.raises(ScenarioValidationError):
        loader.get_scenario("broken")


def test_get_scenario_raises_validation_error_for_invalid_schema(tmp_path):
    scenario_path = tmp_path / "broken-schema.json"
    scenario_path.write_text(
        json.dumps(
            {
                "id": "broken-schema",
                "title": "",
                "description": "desc",
                "persona_name": "persona",
                "persona_description": "persona desc",
                "system_prompt": "prompt",
                "difficulty": "easy",
                "time_limit_seconds": 0,
                "opening_message": "hello",
            }
        ),
        encoding="utf-8",
    )

    loader = ScenarioLoader(tmp_path)

    with pytest.raises(ScenarioValidationError):
        loader.get_scenario("broken-schema")
