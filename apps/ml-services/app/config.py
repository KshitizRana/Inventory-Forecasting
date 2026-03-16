# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    pg_host: str = "localhost"
    pg_port: int = 5432
    pg_user: str = "admin"
    pg_password: str  # no default — MUST be set
    pg_database: str = "inventory"
    
    # Read-only connection for chat
    pg_readonly_url: str
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5001"
    
    # LLM
    openai_api_key: str | None = None
    google_ai_api_key: str | None = None
    groq_ai_api_key: str | None = None
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"
    
    model_config = {"env_file": ".env"}

@lru_cache
def get_settings() -> Settings:
    return Settings()