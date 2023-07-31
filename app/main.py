import asyncio
import json

import openai

from app.config import settings

from app.excel.service import Excel
from app.ai.service import ChatGPT

openai.api_key = settings.OPENAI_KEY

prompts = Excel('excel.xlsx').read_excel()
prompts = Excel.excel_to_ai_prompt(prompts)

response = asyncio.run(ChatGPT(60).send_requests(prompts))

with open('ai.json', 'w', encoding='utf8') as f:
    json.dump(response, f, ensure_ascii=False, indent=2)
