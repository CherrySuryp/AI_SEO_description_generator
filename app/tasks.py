from celery import Celery

from ai.service import ChatGPT
from gsheets.service import GSheet
from utils.service import TextUtils
from selenium_parse.service import Parser

from config import ProdSettings, redis_path

import sys

sys.path.append("..")

celery = Celery("app", broker=redis_path, include=["tasks"])


class Worker:
    """
    Основная бизнес логика программы
    """

    gsheet = GSheet()
    chatgpt = ChatGPT()
    text_utils = TextUtils()
    parser = Parser()
    settings = ProdSettings()

    @staticmethod
    @celery.task()
    def parse_mpstats_keywords(wb_sku: int, row_id: int):
        keywords = Worker.parser.parse_mpstats(wb_sku)
        keywords = Worker.text_utils.transform_dict_keys_to_str(keywords)
        Worker.gsheet.update_status("Ключи собраны")
        Worker.gsheet.update_cell(cell_id=f"F{row_id}", content=keywords)

    @staticmethod
    @celery.task(rate_limit=f"{settings.RPM_LIMIT}/m")
    def chatgpt_task(data: list, row_id: int) -> None:
        result = Worker.chatgpt.send_request(TextUtils.row_to_ai_prompt(data))  # отправляем запрос в ChatGPT
        used_keywords = Worker.text_utils.count_keywords(result, data)  # проверяем вхождение ключевых запросов в текст

        # Записываем результат в таблицу
        Worker.gsheet.update_status("Завершено")
        Worker.gsheet.update_cell(f"G{row_id}", result)
        Worker.gsheet.update_cell(f"H{row_id}", used_keywords)
