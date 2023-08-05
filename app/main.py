import asyncio
import openai

from app.config import settings
from app.excel.service import Excel
from app.ai.service import ChatGPT

openai.api_key = settings.OPENAI_KEY

df = Excel()
chatgpt = ChatGPT()