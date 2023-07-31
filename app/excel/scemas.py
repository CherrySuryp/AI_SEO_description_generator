from pydantic import BaseModel


class SExcel(BaseModel):

    item_name: str
    prompt: str
    keywords: str
    result: str
