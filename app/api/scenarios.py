from fastapi import APIRouter, HTTPException, status

from app.schemas.scenario_schemas import ScenarioDefinition, ScenarioListItem
from app.services import ScenarioLoader, ScenarioNotFoundError, ScenarioValidationError

router = APIRouter(prefix="/scenarios", tags=["scenarios"])


@router.get("", response_model=list[ScenarioListItem])
def list_scenarios() -> list[ScenarioListItem]:
    """
    로더에서 시나리오 목록 가져오기
    """
    loader = ScenarioLoader()
    try:
        scenarios = loader.list_scenarios()
    except ScenarioValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return [ScenarioListItem.from_definition(scenario) for scenario in scenarios]


@router.get("/{scenario_id}", response_model=ScenarioDefinition)
def get_scenario(scenario_id: str) -> ScenarioDefinition:
    """
    특정 시나리오 조회
    """
    loader = ScenarioLoader()
    try:
        return loader.get_scenario(scenario_id)
    except ScenarioNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    except ScenarioValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
