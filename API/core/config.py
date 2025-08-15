from pydantic_settings import BaseSettings
from pydantic import computed_field

class Settings(BaseSettings):
    # These are the variables Pydantic will read from your .env file
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_SERVER: str = "db"
    API_V1_STR: str = "/api/v1"

    # This is a "computed field". It will be generated automatically
    # after the fields above have been loaded from the .env file.
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        # Optional: Tell pydantic to ignore extra vars from the .env file
        # extra = 'ignore' 

settings = Settings()