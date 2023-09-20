import re
import asyncio
from datetime import datetime

import sentry_sdk
from celery import chain

from gsheets.service import GSheet
from utils.service import TextUtils
from config import ProdSettings
from tasks import Worker


class TaskService:
    def __init__(self):
        self.settings = ProdSettings()
        self.send_task = Worker()
        self.gsheet = GSheet()
        self.utils = TextUtils()

    async def fetcher_worker(self) -> None:
        """
        Опрос таблицы каждые N секунд и отправка новых задач в очередь
        """
        print(f"{datetime.now().replace(microsecond=0)}: Program has started")

        while True:
            try:
                sheet_data = self.gsheet.read_sheet()  # чтение таблицы

                for i in range(len(sheet_data)):
                    row_id = i + 2
                    task_status: str = sheet_data[i][0]
                    work_mode: str = sheet_data[i][1]
                    auto_mode: str = sheet_data[i][2]

                    if task_status == "Собрать ключи":
                        """
                        Сборка данных
                        """
                        if work_mode == "По названию товара":
                            item_name = sheet_data[i][4]
                            print(f"{datetime.now().replace(microsecond=0)}: Sent task from row {row_id} to queue")
                            self.gsheet.update_status("В работе", row_id)
                            (
                                self.send_task.parse_mpstats_keywords_by_item_name
                                .apply_async((auto_mode, item_name, row_id), queue="mpstats")
                            )

                        elif work_mode == "Со сборкой ключей V1.0":
                            wb_sku = int(re.search(r"\d+", sheet_data[i][3]).group()) if sheet_data[i][3] else None
                            print(f"{datetime.now().replace(microsecond=0)}: Sent task from row {row_id} to queue")
                            self.gsheet.update_status("В работе", row_id)
                            queue = chain(
                                self.send_task.parse_wb_item_name.si(wb_sku, row_id)  # Название товара
                                | self.send_task.parse_wb_item_params.si(wb_sku, row_id)  # Характеристики товара
                                # Ключевые слова
                                | self.send_task.parse_mpstats_keywords_by_sku.si(auto_mode, wb_sku, row_id)
                            )
                            queue.apply_async(queue="mpstats")

                        elif work_mode == "Со сборкой ключей V1.2":
                            wb_sku = int(re.search(r"\d+", sheet_data[i][3]).group()) if sheet_data[i][3] else None
                            print(f"{datetime.now().replace(microsecond=0)}: Sent task from row {row_id} to queue")
                            self.gsheet.update_status("В работе", row_id)
                            queue = chain(
                                self.send_task.parse_wb_item_name.si(wb_sku, row_id)  # Название товара
                                | self.send_task.parse_wb_item_params.si(wb_sku, row_id)  # Характеристики товара
                                | self.send_task.parse_wb_item_desc.si(wb_sku, row_id)  # Описание товара
                                # Ключевые слова
                                | self.send_task.parse_mpstats_keywords_by_sku.si(auto_mode, wb_sku, row_id)
                            )
                            queue.apply_async(queue="mpstats")

                    if task_status == "Сгенерировать описание":
                        """
                        Генерация описания
                        """
                        prompt = self.utils.row_to_ai_prompt(sheet_data[i])
                        print(f"{datetime.now().replace(microsecond=0)}: Sent task from row {row_id} to queue")
                        self.gsheet.update_status("В работе", row_id)
                        self.send_task.chatgpt_task.apply_async((prompt, row_id), queue="chatgpt")

                await asyncio.sleep(self.settings.REFRESH_INTERVAL)  # интервал между опросами таблицы

            except Exception as ex:
                print(ex)
                sentry_sdk.capture_exception(ex)
                await asyncio.sleep(self.settings.REFRESH_INTERVAL / 2)
