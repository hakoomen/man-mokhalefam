from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    ALLOWED_CHANNEL_IDS: list[str]
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
