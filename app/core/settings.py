from pathlib import Path

from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application level configuration loaded from environment variables."""

    MODE: str = Field(default="local")
    MONGO_DB_URL: str = Field(..., description="MongoDB connection string")
    MONGO_DB_NAME: str = Field(default="n3_todo", description="MongoDB database name")
    JWT_SECRET_KEY: str = Field(..., description="Secret key used to sign JWT tokens")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    model_config = ConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        extra="ignore",
    )


settings = Settings()  # type: ignore[arg-type]
