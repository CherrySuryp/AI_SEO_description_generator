from pydantic import BaseModel, ConfigDict


class SExcel(BaseModel):
    model_config = ConfigDict(strict=False)

    item_name: str
    prompt: str
    keywords: str
    result: str
