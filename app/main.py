import json

import asyncio
import openai

from app.config import settings
from app.excel.service import Excel
from app.ai.service import ChatGPT

from pandas import json_normalize

openai.api_key = settings.OPENAI_KEY

df = Excel('excel.xlsx')
df_excel = df.read_excel()

chatgpt = ChatGPT()

if __name__ == '__main__':
    response = asyncio.run(chatgpt.send_requests(df.excel_to_ai_prompt(df_excel)))
    df_excel = df.ai_result_to_df(df_excel, response)
    df.write_excel(df_excel)

