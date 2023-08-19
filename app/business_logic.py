import asyncio
import logging

from gsheets.service import GSheet
from config import settings
from tasks import Worker
from googleapiclient.errors import HttpError  # noqa


class TaskService:
    def __init__(self):
        self.sleep_interval = settings.REFRESH_INTERVAL
        self.gsheet = GSheet()
        self.worker = Worker()

    async def fetcher_worker(self):
        while True:
            sheet_data = self.gsheet.read_sheet()

            if not sheet_data:
                await asyncio.sleep(self.sleep_interval)
                pass

            for i in range(len(sheet_data)):
                row_id = i + 2
                if sheet_data[i][0] == "Взять в работу" and sheet_data[i][1:5]:
                    self.worker.write_response_to_gsheet.delay(
                        data=sheet_data[i], row_id=row_id
                    )
                    self.gsheet.update_cell(f"A{row_id}", "В работе")
                    print(f"Sent task from row {row_id} to queue")

                    await asyncio.sleep(self.sleep_interval)
