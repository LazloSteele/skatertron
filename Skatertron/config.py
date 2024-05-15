from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    database_url: str = "postgresql+asyncpg://postgres:Birdl%40nd1@localhost:5432/test"
    echo_sql: bool = True
    test: bool = True
    project_name: str = "Skatertron"
    oauth_token_secret: str = "my_dev_secret"
    debug_logs: bool = False


settings = Settings()
