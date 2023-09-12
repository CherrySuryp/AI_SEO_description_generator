import asyncio
import re
from datetime import datetime

import sentry_sdk
from celery import chain

from gsheets.service import GSheet
from config import ProdSettings
from tasks import Worker


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
                    row_id = i + 2
                    task_status: str = sheet_data[0]
                    work_mode: str = sheet_data[1]

                    if task_status == "Взять в работу":
                        if work_mode == "Только описание":
                            self.send_task.chatgpt_task.apply_async((sheet_data[i], row_id), queue="chatgpt")

                        elif work_mode == "Со сборкой ключей v1.0":
                            ...

                        elif work_mode == "Со сборкой ключей V1.2":
                            ...

                await asyncio.sleep(self.settings.REFRESH_INTERVAL)  # интервал между опросами таблицы
            except Exception as ex:
                sentry_sdk.capture_exception(ex)
                await asyncio.sleep(self.settings.REFRESH_INTERVAL / 2)

# if sheet_data[i][0] == "Собрать ключи":
#     """
#     Отправляет задачу на сборку информации с WB и MpStats
#     """
#
#     wb_sku = int(re.search(r"\d+", sheet_data[i][1]).group()) # Достаем sku из ссылки
#
#     self.gsheet.update_status(row_id=row_id, new_status="Ключи в сборке")
#     queue = chain(
#         self.send_task.parse_wb_item_name.si(wb_sku, row_id)  # Получение названия товара
#         | self.send_task.parse_wb_item_params.si(wb_sku, row_id)  # Получение характеристик товара
#         | self.send_task.parse_mpstats_keywords.si(wb_sku, row_id)  # Получение ключевых слов
#     )
#     queue.apply_async(queue="mpstats")
#
# # -------------------------------------------------------------------------------------------------
#
# elif sheet_data[i][0] == "Сгенерировать описание":
#     """
#     Отправляет задачу на генерацию описания в  ChatGPT
#     """
#
#     self.gsheet.update_status(row_id=row_id, new_status="Генерация")
#     self.send_task.chatgpt_task.apply_async((sheet_data[i], row_id), queue="chatgpt")
#     print(f"{datetime.now().replace(microsecond=0)} Sent task from row {row_id} to queue")
