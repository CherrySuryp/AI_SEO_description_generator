import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

dir_path = os.path.dirname(os.path.realpath(__file__))


class ProdSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(dir_path, "../.env"), env_file_encoding="utf-8")

    MODE: Literal["DEV", "PROD"]
    USE_SENTRY: Literal["TRUE", "FALSE"]
    SENTRY_DSN: str

    MPSTATS_LOGIN: str
    MPSTATS_PASS: str

    WB_TOKEN: str

    OPENAI_KEY: str
    RPM_LIMIT: int
    GPT_MODEL: str

    REFRESH_INTERVAL: int
    GSHEET_ID: str
    GOOGLE_CREDS: str


settings = ProdSettings()

if ProdSettings().MODE == "PROD":
    redis_path = "redis://redis_ai_seo:6379/0"

else:
    redis_path = "redis://127.0.0.1:6379/0"
