import sentry_sdk
from celery import Celery

from ai.service import ChatGPT
from gsheets.service import GSheet
from utils.service import TextUtils
from selenium_parse.service import Parser

from config import ProdSettings, redis_path

celery = Celery("app", broker=redis_path, include=["tasks"])

celery.conf.worker_pool_restarts = True
celery.conf.broker_connection_retry_on_startup = True

celery.conf.task_queues = {}  # noqa

celery.conf.task_queues["chatgpt"] = {"exchange": "chatgpt", "routing_key": "chatgpt", "concurrency": 4}
celery.conf.task_queues["mpstats"] = {"exchange": "mpstats", "routing_key": "mpstats", "concurrency": 1}
celery.conf.task_default_queue = "mpstats"

celery.conf.result_expires = 60


class Worker:
    """
    Основная бизнес логика программы
    """

    gsheet = GSheet()
    chatgpt = ChatGPT()
    text_utils = TextUtils()
    settings = ProdSettings()

    @staticmethod
    @celery.task(soft_time_limit=120, time_limit=180)
    def parse_wb_item_name(wb_sku: int, row_id: int):
        try:
            item_name = Parser().get_wb_item_name(wb_sku)
            Worker.gsheet.update_cell(content=item_name, row_id=f"E{row_id}")
        except Exception as e:
            sentry_sdk.capture_exception(e)

    @staticmethod
    @celery.task(soft_time_limit=120, time_limit=180)
    def parse_wb_item_params(wb_sku: int, row_id: int):
        try:
            item_params = Parser().get_wb_item_params(wb_sku)
            item_params = TextUtils().exclude_dim_info(item_params)
            Worker.gsheet.update_cell(content=str(item_params), row_id=f"F{row_id}")
        except Exception as e:
            sentry_sdk.capture_exception(e)

    @staticmethod
    @celery.task(soft_time_limit=120, time_limit=180)
    def parse_wb_item_desc(wb_sku: int, row_id: int):
        try:
            item_desc = Parser().get_wb_item_desc(wb_sku)
            Worker.gsheet.update_cell(content=str(item_desc), row_id=f"G{row_id}")
        except Exception as e:
            sentry_sdk.capture_exception(e)

    @staticmethod
    @celery.task(soft_time_limit=120, time_limit=180)
    def parse_mpstats_keywords_by_sku(auto_mode: str, wb_sku: int, row_id: int):
        keywords = None
        try:
            keywords = Parser().parse_mpstats_by_sku(wb_sku)
        except Exception as e:
            sentry_sdk.capture_exception(e)

        keywords = Worker.text_utils.transform_dict_keys_to_str(keywords) if keywords else None
        Worker.gsheet.update_cell(row_id=f"H{row_id}", content=keywords)

        if auto_mode == "Ручной":
            Worker.gsheet.update_status("Завершено", row_id)
        else:
            Worker.gsheet.update_status("Сгенерировать описание", row_id)

    @staticmethod
    @celery.task(soft_time_limit=120, time_limit=180)
    def parse_mpstats_keywords_by_item_name(auto_mode: str, item_name: str, row_id: int):
        keywords = None
        try:
            keywords = Parser().parse_mpstats_by_name(item_name)
        except Exception as e:
            sentry_sdk.capture_exception(e)

        keywords = Worker.text_utils.transform_dict_keys_to_str(keywords) if keywords else None
        Worker.gsheet.update_cell(row_id=f"H{row_id}", content=keywords)

        if auto_mode == "Авто":
            Worker.gsheet.update_status("Сгенерировать описание", row_id)
        else:
            Worker.gsheet.update_status("Завершено", row_id)

    @staticmethod
    @celery.task(rate_limit=f"{settings.RPM_LIMIT}/m", soft_time_limit=120, time_limit=180)
    def chatgpt_task(prompt: str, row_id: int) -> None:
        try:
            result = Worker.chatgpt.send_request(prompt)  # отправляем запрос в ChatGPT

            # Записываем результат в таблицу
            Worker.gsheet.update_status("Завершено", row_id)
            Worker.gsheet.update_cell(result, f"J{row_id}")
        except Exception as e:
            sentry_sdk.capture_exception(e)
