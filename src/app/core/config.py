from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost/splitter"
    secret_key: str = "your-secret-key-here"
    environment: str = "development"
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Allow extra fields from .env file
    model_config = {"extra": "ignore", "env_file": ".env"}


settings = Settings()
