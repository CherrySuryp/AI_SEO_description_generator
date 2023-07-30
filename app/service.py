import json

import pandas as pd
from pandas import DataFrame
from pydantic import ValidationError
from typing import Optional


class Excel:
    @classmethod
    def read_excel(cls, file_path: str, sel_rows: Optional[list] = None) -> DataFrame:
        df = pd.read_excel(file_path).fillna(" ")
        if sel_rows:
            return df[sel_rows]
        return df

    @classmethod
    def write_excel(cls):
        ...


data_frame = Excel.read_excel('excel.xlsx')
print(data_frame.to_dict())
