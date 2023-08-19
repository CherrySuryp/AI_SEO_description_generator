import sys

sys.path.append("..")

import openai  # noqa
from app.config import settings  # noqa

openai.api_key = settings.OPENAI_KEY


class ChatGPT:
    """
    :param rpm: Requests per minute. The default value is taken from the .env file.
     Check your available RPM at https://platform.openai.com/docs/guides/rate-limits/overview
    :param model: GPT Model (e.g. gpt-3.5-turbo). The default value is taken from the .env file.
     You can check available models at https://platform.openai.com/docs/models/overview
    """

    def __init__(self, rpm: int = settings.RPM_LIMIT, model: str = settings.GPT_MODEL):
        self.rpm = rpm
        self.model = model

    def send_request(self, prompt: str) -> str:
        req = (
            openai.ChatCompletion.create(
                model=self.model, messages=[{"role": "user", "content": prompt}]
            )
            .choices[0]
            .message.content
        )
        return req


chatgpt = ChatGPT()
