import json

import pandas as pd
from pandas import DataFrame
from pydantic import ValidationError
from app.excel.scemas import SExcel
from typing import Optional


class Excel:

    def __init__(
            self,
            file_path: str = '../excels/excel.xlsx',
            result_file_path: str = '../excels/result.xlsx'
    ):
        self.file_path = file_path
        self.result_file_path = result_file_path

    def read_excel(self, sel_rows: Optional[list] = None) -> DataFrame:
        df = pd.read_excel(self.file_path, sheet_name='todo').fillna('').replace(r'\n', '', regex=True)
        if sel_rows:
            df = df[sel_rows]
        return df

    def write_excel(self, df: DataFrame) -> None:
        df.to_excel(self.result_file_path, sheet_name='result')

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

    @staticmethod
    def ai_result_to_df(df: DataFrame, ai_result: list) -> DataFrame:
        content = []
        for i in range(len(df)):
            row = SExcel.model_validate(df.loc[i].to_dict()).model_dump()
            row['result'] = ai_result[i]
            content.append(row)
        return pd.json_normalize(content)
