from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PATH: str

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
