import json
import logging
from pathlib import Path

from pydantic import ValidationError

from app.core.config import get_settings
from app.schemas import ScenarioDefinition


class ScenarioLoaderError(Exception):
    pass


class ScenarioNotFoundError(ScenarioLoaderError):
    pass


class ScenarioValidationError(ScenarioLoaderError):
    pass


class ScenarioLoader:
    def __init__(self, scenario_dir: Path | None = None) -> None:
        self.scenario_dir = scenario_dir or get_settings().SCENARIO_DIR

    def list_scenarios(self) -> list[ScenarioDefinition]:
        return [self._load(path) for path in sorted(self.scenario_dir.glob("*.json"))]

    def get_scenario(self, scenario_id: str) -> ScenarioDefinition:
        path = self.scenario_dir / f"{scenario_id}.json"
        if not path.exists():
            logging.warning("Scenario not found: %s", scenario_id)
            raise ScenarioNotFoundError(f"Scenario not found: {scenario_id}")
        return self._load(path)

    def _load(self, path: Path) -> ScenarioDefinition:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return ScenarioDefinition.model_validate(data)
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            logging.exception("Failed to load scenario: %s", path)
            raise ScenarioValidationError(f"Failed to load scenario: {path.name}") from exc
