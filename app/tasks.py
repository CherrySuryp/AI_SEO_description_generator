from celery import Celery

from ai.service import ChatGPT
from gsheets.service import GSheet
from utils.service import TextUtils

from config import settings, redis_path

import sys

sys.path.append("..")


celery = Celery("app", broker=redis_path, include=["tasks"])


class Worker:
    gsheet = GSheet()
    chatgpt = ChatGPT()
    text_utils = TextUtils()

    @staticmethod
    @celery.task(rate_limit=f"{settings.RPM_LIMIT}/m")
    def worker(data: list, row_id: int) -> None:
        result = Worker.chatgpt.send_request(TextUtils.row_to_ai_prompt(data))
        used_keywords = Worker.text_utils.count_keywords(result, data)

        Worker.gsheet.update_cell(f"A{row_id}", "Завершено")
        Worker.gsheet.update_cell(f"F{row_id}", result)
        Worker.gsheet.update_cell(f"G{row_id}", used_keywords)
