import openai
from config import settings
import json

openai.api_key = settings.OPENAI_KEY

req = 'Напиши мне описание беспроводных наушников от 4000 до 5000 символов.' \
      'Важно не изменять ключевые слова и использовать их "как есть"' \
      ' Ключевые слова:' \
      ' наушники беспроводные, черные наушники,,' \
      ' безпроводные, наушники беспроводные большие черные наушники черные,' \
      ' беспроводные наушники,' \
      ' черныенушники,' \
      ' беспроводные для телефона черные блютуз'

chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": req}]
)

chat_completion = chat_completion.choices

with open('ai_result.json', 'w', encoding='utf-8') as f:
    json.dump(chat_completion, f, ensure_ascii=False, indent=2)
