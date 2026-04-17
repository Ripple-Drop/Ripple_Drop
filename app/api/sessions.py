from typing import Annotated, cast

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import ScenarioSession
from app.schemas import SessionCreateRequest, SessionCreateResponse
from app.services import ScenarioLoader, ScenarioNotFoundError, ScenarioValidationError

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionCreateResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    request: SessionCreateRequest,
    db: Annotated[Session, Depends(get_db)],
) -> SessionCreateResponse:
    """
    scenario_id를 검증한 뒤 ScenarioSession 생성
    session_id, scenario_id 반환
    """
    loader = ScenarioLoader()
    try:
        loader.get_scenario(request.scenario_id)
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

    session = ScenarioSession(
        user_id=request.user_id,
        scenario_id=request.scenario_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    return SessionCreateResponse(
        session_id=cast(int, session.id),
        scenario_id=cast(str, session.scenario_id),
    )
