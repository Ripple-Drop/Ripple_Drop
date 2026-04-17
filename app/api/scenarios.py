from fastapi import APIRouter, HTTPException, status

from app.schemas.scenario_schemas import ScenarioListItem
from app.services import ScenarioLoader, ScenarioValidationError

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
