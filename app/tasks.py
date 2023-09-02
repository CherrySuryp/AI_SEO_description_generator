from celery import Celery

from ai.service import ChatGPT
from gsheets.service import GSheet
from utils.service import TextUtils
from selenium_parse.service import Parser

from config import ProdSettings, redis_path

celery = Celery("app", broker=redis_path, include=["tasks"])

celery.conf.worker_pool_restarts = True
celery.conf.task_queues = {} # noqa

celery.conf.task_queues['chatgpt'] = {
    'exchange': 'chatgpt',
    'routing_key': 'chatgpt',
    'concurrency': 4
}
celery.conf.task_queues['mpstats'] = {
    'exchange': 'mpstats',
    'routing_key': 'mpstats',
    'concurrency': 1
}
celery.conf.task_default_queue = 'mpstats'


class Worker:
    """
    Основная бизнес логика программы
    """

    gsheet = GSheet()
    chatgpt = ChatGPT()
    text_utils = TextUtils()
    settings = ProdSettings()

    @staticmethod
    @celery.task(soft_time_limit=60, time_limit=120)
    def parse_mpstats_keywords(wb_sku: int, row_id: int):
        keywords = None
        try:
            keywords = Parser().parse_mpstats(wb_sku)
        except Exception as e:
            print(e)
        keywords = Worker.text_utils.transform_dict_keys_to_str(keywords) if keywords else None

        # Запись результата в таблицу
        Worker.gsheet.update_status(row_id, "Ключи собраны")
        Worker.gsheet.update_cell(cell_id=f"F{row_id}", content=keywords)

    @staticmethod
    @celery.task(rate_limit=f"{settings.RPM_LIMIT}/m", soft_time_limit=60, time_limit=120)
    def chatgpt_task(data: list, row_id: int) -> None:
        result = Worker.chatgpt.send_request(TextUtils.row_to_ai_prompt(data))  # отправляем запрос в ChatGPT
        used_keywords = Worker.text_utils.count_keywords(result, data)  # проверяем вхождение ключевых запросов в текст

        # Записываем результат в таблицу
        Worker.gsheet.update_status(row_id, "Завершено")
        Worker.gsheet.update_cell(f"G{row_id}", result)
        Worker.gsheet.update_cell(f"H{row_id}", used_keywords)
