from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "OMEGA Platform"
    VERSION: str = "0.1.0-alpha"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()