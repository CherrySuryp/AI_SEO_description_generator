import asyncio
import re
from datetime import datetime

import sentry_sdk
from celery import chain

from gsheets.service import GSheet
from config import ProdSettings
from tasks import Worker

from googleapiclient.errors import HttpError  # noqa


class TaskService:
    def __init__(self):
        self.settings = ProdSettings()
        self.gsheet = GSheet()
        self.send_task = Worker()

    async def fetcher_worker(self) -> None:
        """
        Опрос таблицы каждые N секунд и отправка новых задач в очередь
        """
        print(f"{datetime.now().replace(microsecond=0)} Program has started")

        while True:
            try:
                sheet_data = self.gsheet.read_sheet()  # чтение таблицы

                for i in range(len(sheet_data)):
                    """
                    Если находится строчка со статусом "Взять в работу" или "Сгенерировать описание",
                    то задача отправляется в очередь
                    """
                    row_id = i + 2

                    if sheet_data[i][0] == "Собрать ключи":
                        wb_sku = int(re.search(r'\d+', sheet_data[i][1]).group())

                        # Отправляем задачу на сборку ключевых запросов по SKU карточки товара
                        self.gsheet.update_status(row_id=row_id, new_status="Ключи в сборке")
                        queue = chain(
                            self.send_task.parse_wb_item_name.si(wb_sku, row_id) |
                            self.send_task.parse_wb_item_params.si(wb_sku, row_id) |
                            self.send_task.parse_mpstats_keywords.si(wb_sku, row_id)
                        )
                        queue.apply_async(queue="mpstats")

# ----------------------------------------------------------------------------------------------------------------------

                    elif sheet_data[i][0] == "Сгенерировать описание":
                        # Отправляем задачу в ChatGPT на генерацию описания по заданным в таблице параметрам
                        self.gsheet.update_status(row_id=row_id, new_status="Генерация")

                        # отправляем задачу в очередь
                        self.send_task.chatgpt_task.apply_async((sheet_data[i], row_id), queue="chatgpt")
                        print(f"{datetime.now().replace(microsecond=0)} Sent task from row {row_id} to queue")

                await asyncio.sleep(self.settings.REFRESH_INTERVAL)  # интервал между опросами таблицы

            except Exception as ex:
                sentry_sdk.capture_exception(ex)
                await asyncio.sleep(self.settings.REFRESH_INTERVAL / 2)
