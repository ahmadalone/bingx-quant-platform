from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BINGX_API_KEY: str = ""
    BINGX_API_SECRET: str = ""
    BINGX_TESTNET: bool = True
    DB_URL: str = "sqlite+aiosqlite:///trading.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()