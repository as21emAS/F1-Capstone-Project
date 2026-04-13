from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")
    
    PROJECT_NAME: str = "F1 Predictor"
    VERSION: str = "0.1.0"
    DATABASE_URL: str
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    CURRENT_SEASON: int = 2026
    OPENWEATHER_API_KEY: Optional[str] = None
    VISUALCROSSING_API_KEY: Optional[str] = None

settings = Settings()