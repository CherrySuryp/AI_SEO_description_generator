import json

import pandas as pd
from pandas import DataFrame
from pydantic import ValidationError 
from app.scemas import SExcel
from typing import Optional


class Excel:
    @classmethod
    def read_excel(cls, file_path: str, sel_rows: Optional[list] = None) -> DataFrame:
        df = pd.read_excel(file_path).fillna('')
        if sel_rows:
            df = df[sel_rows]
        return df.replace(r'\n', '', regex=True)

    @classmethod
    def write_excel(cls):
        ...

    @classmethod
    def excel_to_dict_by_rows(cls, df: DataFrame) -> list:
        content = []
        for i in range(len(df)):
            try:
                row = SExcel.model_validate(df.loc[i].to_dict()).model_dump()
                if not row['result']:
                    content.append(row)
            except ValidationError:
                pass
        return content


data_frame = Excel.read_excel('excel.xlsx')
data_frame = Excel.excel_to_dict_by_rows(data_frame)

with open('pandas.json', 'w', encoding='utf8') as f:
    json.dump(data_frame, f, ensure_ascii=False, indent=2)
