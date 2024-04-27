from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    ALLOWED_CHANNEL_IDS: list[str]
    DATABASE_URL: str
    IS_SQLALCHEMY_LOG_ENABLED: bool = False

    model_config = SettingsConfigDict()


settings = Settings()
