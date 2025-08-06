from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(".env"), env_file_encoding="utf-8")

    GOOGLE_API_KEY: str


# mypy doesn't understand that this call doesn't actually require arguments
Config = Settings()  # type:ignore[call-arg]
