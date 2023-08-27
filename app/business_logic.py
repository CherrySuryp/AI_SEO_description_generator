import asyncio

from ssl import SSLEOFError

import sentry_sdk

from gsheets.service import GSheet
from config import ProdSettings
from tasks import Worker
from googleapiclient.errors import HttpError  # noqa

from datetime import datetime


class TaskService:
    def __init__(self):
        self.settings = ProdSettings()
        self.gsheet = GSheet()
        self.send_task = Worker()

    async def fetcher_worker(self) -> None:
        """
        Опрос таблицы каждые N секунд и отправка новых задач в очередь
        :return:
        """
        print(f"{datetime.now().replace(microsecond=0)} Program has started")

        while True:
            try:
                sheet_data = self.gsheet.read_sheet()  # чтение таблицы

                for i in range(len(sheet_data)):
                    """
                    Если находится строчка со статусом "Взять в работу"
                    и заполненными полями, то задача отправляется в очередь
                    """
                    if sheet_data[i][0] == "Взять в работу" and sheet_data[i][1:5]:
                        row_id = i + 2

                        # обновляем статус
                        self.gsheet.update_status(row_id=row_id, new_status="В работе")

                        # отправляем задачу в очередь
                        self.send_task.worker.delay(data=sheet_data[i], row_id=row_id)

                        print(
                            f"{datetime.now().replace(microsecond=0)} Sent task from row {row_id} to queue"
                        )
                # интервал между опросами таблицы
                await asyncio.sleep(self.settings.REFRESH_INTERVAL)

            except HttpError or IndexError or SSLEOFError as e:
                sentry_sdk.capture_exception(e)
                await asyncio.sleep(self.settings.REFRESH_INTERVAL / 2)
