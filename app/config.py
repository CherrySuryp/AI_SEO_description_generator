import os

from pydantic_settings import BaseSettings, SettingsConfigDict

dir_path = os.path.dirname(os.path.realpath(__file__))


class ProdSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(dir_path, '../.env'), env_file_encoding='utf-8')

    OPENAI_KEY: str
    RPM_LIMIT: int
    GPT_MODEL: str
    SLEEP_INTERVAL: int
    GSHEET_ID: str
    GOOGLE_CREDS: str


settings = ProdSettings()
