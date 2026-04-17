from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ScenarioDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    persona_name: str
    persona_description: str
    system_prompt: str
    difficulty: Literal["easy", "medium", "hard"]
    time_limit_seconds: int = Field(gt=0)
    opening_message: str

    @field_validator(
        "id",
        "title",
        "description",
        "persona_name",
        "persona_description",
        "system_prompt",
        "opening_message",
    )
    # 빈 문자열 검증
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("value must not be blank")
        return value
