from pydantic_settings import BaseSettings
from pydantic import computed_field, model_validator
from typing import List, Union

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str = "db"
    API_V1_STR: str = "/api/v1"

    MINIO_ENDPOINT: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_BUCKET_NAME: str
    
    CORS_ORIGINS: Union[str, List[str]] = ""

    @model_validator(mode='after')
    def assemble_cors_origins(self) -> 'Settings':
        if isinstance(self.CORS_ORIGINS, str):
            # If it's a string, split by comma and strip whitespace
            self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin]
        return self

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()