from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_PATH: str

    class Config:
        env_file = ".env"


class DBSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = ".env"

    @property
    def dsn(self):
        return f"posgressql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


def get_settings() -> Settings:
    return Settings()

def get_db_settings() -> DBSettings:
    return DBSettings()