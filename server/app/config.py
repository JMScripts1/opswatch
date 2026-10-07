from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./opswatch.db"
    agent_token: str = "dev-token"
    webhook_url: str = ""
    report_hour: int = 8


settings = Settings()
