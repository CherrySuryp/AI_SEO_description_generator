import asyncio

from gsheets.service import GSheet
from config import settings
from tasks import Worker
from googleapiclient.errors import HttpError  # noqa

from datetime import datetime


class TaskService:
    def __init__(self):
        self.sleep_interval = settings.REFRESH_INTERVAL
        self.gsheet = GSheet()
        self.send_task = Worker()

    async def fetcher_worker(self):
        print(f"{datetime.now().replace(microsecond=0)} Program has started")
        while True:
            sheet_data = self.gsheet.read_sheet()

            if sheet_data:
                for i in range(len(sheet_data)):
                    if sheet_data[i][0] == "Взять в работу" and sheet_data[i][1:5]:
                        row_id = i + 2

                        self.send_task.worker.delay(data=sheet_data[i], row_id=row_id)
                        self.gsheet.update_cell(f"A{row_id}", "В работе")

                        print(
                            f"{datetime.now().replace(microsecond=0)} Sent task from row {row_id} to queue"
                        )

                        await asyncio.sleep(self.sleep_interval)
            else:
                await asyncio.sleep(self.sleep_interval)
