from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path, PosixPath


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    KEYS_DIR: PosixPath = Path(__file__).resolve().parent / "keys"

    @property
    def PUBLIC_KEY(self):
        with open(self.KEYS_DIR / "public.pem", "rb") as f:
            PUBLIC_KEY = f.read()
        return PUBLIC_KEY

    @property
    def PRIVATE_KEY(self):
        with open(self.KEYS_DIR / "private.pem", "rb") as f:
            PRIVATE_KEY = f.read()
        return PRIVATE_KEY

    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()