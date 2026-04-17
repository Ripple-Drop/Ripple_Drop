from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_scenario_loader
from app.schemas.scenario_schemas import ScenarioListItem
from app.services import ScenarioLoader, ScenarioValidationError

router = APIRouter(prefix="/scenarios", tags=["scenarios"])

# 시나리오 목록 읽기
@router.get("", response_model=list[ScenarioListItem])
def list_scenarios(
    loader: Annotated[ScenarioLoader, Depends(get_scenario_loader)],
) -> list[ScenarioListItem]:
    try:
        scenarios = loader.list_scenarios()
    except ScenarioValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return [ScenarioListItem.from_definition(scenario) for scenario in scenarios]
