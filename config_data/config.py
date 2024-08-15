from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings


if not find_dotenv():
    exit("Environment variables are not loaded because the file is missing .env")
else:
    load_dotenv()


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_pass: str
    db_name: str
    bot_token: str
    kinopoisk_dev_token: str
    admin_id: int
    img_path: str

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        # postgresql+asyncpg://postgres:postgres@localhost:5432/postgres
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"


settings = Settings()
