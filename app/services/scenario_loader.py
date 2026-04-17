import json
import logging
import os
from pathlib import Path

from pydantic import ValidationError

from app.schemas import ScenarioDefinition


class ScenarioLoaderError(Exception):
    pass


class ScenarioNotFoundError(ScenarioLoaderError):
    pass


class ScenarioValidationError(ScenarioLoaderError):
    pass


class ScenarioLoader:
    scenario_dir: Path

    def __init__(self, scenario_dir: Path | None = None) -> None:
        if scenario_dir is None:
            self.scenario_dir = self._resolve_scenario_dir()
        else:
            self.scenario_dir = scenario_dir

    @staticmethod
    def _resolve_scenario_dir() -> Path:
        scenario_dir = os.getenv("SCENARIO_DIR")
        if scenario_dir:
            return Path(scenario_dir)
        return Path(__file__).resolve().parents[2] / "scenarios"

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
