from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    pass

    class Config:
        env_prefix = "BD_"


class Settings(BaseSettings):
    db: DBConfig


def get_settings():
    return Settings(db=DBConfig())