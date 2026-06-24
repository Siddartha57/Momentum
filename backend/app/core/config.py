from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Momentum"
    environment: str = "development"
    secret_key: str = "change-this-secret"
    access_token_expire_minutes: int = 1440
    database_url: str = "sqlite:///./momentum.db"
    frontend_url: str = "http://localhost:5173"
    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str = "no-reply@momentum.local"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
