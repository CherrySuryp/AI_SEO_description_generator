import asyncio
import openai
from tqdm import tqdm
from app.config import settings


class ChatGPT:
    """
    :param rpm: "Requests per minute. The default value is taken from the .env file"
    """

    def __init__(self, rpm: int = settings.RPM_LIMIT):
        self.rpm = rpm

    @staticmethod
    def slice_list_to_chunks(to_slice: list, chunk_size: int) -> list:
        for piece in range(0, len(to_slice), chunk_size):
            yield to_slice[piece:piece + chunk_size]

    @staticmethod
    async def make_request(prompt: str) -> list:
        req = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[{"role": "user", "content": prompt}]
        ).choices[0].message.content

        return req

    async def send_requests(self, prompts: list) -> list:
        result = []
        request_interval = 60 / self.rpm
        chunks = self.slice_list_to_chunks(prompts, 10)

        for chunk in chunks:
            tasks = []
            for i in tqdm(chunk, desc='Asking ChatGPT to generate response', colour='GREEN'):
                task = asyncio.ensure_future(
                    self.make_request(i)
                )
                tasks.append(task)
                await asyncio.sleep(request_interval)

            result.extend(await asyncio.gather(*tasks))

        return result
