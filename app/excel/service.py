import json

import pandas as pd
from pandas import DataFrame
from pydantic import ValidationError
from app.excel.scemas import SExcel
from typing import Optional


class Excel:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_excel(self, sel_rows: Optional[list] = None) -> DataFrame:
        df = pd.read_excel(self.file_path).fillna('').replace(r'\n', '', regex=True)
        if sel_rows:
            df = df[sel_rows]
        return df

    def write_excel(self):
        ...

    @staticmethod
    def excel_to_ai_prompt(df: DataFrame) -> list:
        content = []
        for i in range(len(df)):
            try:
                row = SExcel.model_validate(df.loc[i].to_dict()).model_dump()
                item_name = row['item_name']
                base_prompt = row['prompt']
                keywords = row['keywords']

                if not row['result']:
                    prompt = (f'Задача: {base_prompt}. \n'
                              f'Товар: {item_name}. \n'
                              f'Ключевые слова: {keywords}')
                    content.append(prompt)
            except ValidationError:
                pass

        return content
