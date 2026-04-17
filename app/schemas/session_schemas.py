from pydantic import BaseModel, ConfigDict


class SessionCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int
    scenario_id: str


class SessionCreateResponse(BaseModel):
    session_id: int
    scenario_id: str
