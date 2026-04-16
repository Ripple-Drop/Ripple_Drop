from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parents[2])

    DATABASE: str
    DATABASE_HOST: str
    DATABASE_PORT: int = 3306
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    SCENARIO_DIR: Path | None = None

    def model_post_init(self, __context: object) -> None:
        if self.SCENARIO_DIR is None:
            self.SCENARIO_DIR = self.BASE_DIR / "scenarios"

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DATABASE}://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    # 기타 설정 추가 가능
    model_config = SettingsConfigDict(
        env_file="envs/.env.dev", # 환경 변수 파일 경로 설정
        env_file_encoding="utf-8", # 환경 변수 파일 인코딩 설정
        case_sensitive=True,  # 환경 변수 이름 대소문자 구분 여부 설정
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
