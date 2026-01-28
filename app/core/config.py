from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # JWT / Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Optional: use later if you want different behaviours
    ENV: str = "dev"

    model_config = SettingsConfigDict(
        env_file=".env",          # load from .env if present
        env_file_encoding="utf-8",
        extra="ignore",           # ignore unknown env vars
    )


settings = Settings()
