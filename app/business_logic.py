import asyncio
from gsheets.service import gsheet
from config import settings
from tasks import worker


class BusinessLogic:
    def __init__(
            self,
            sleep_interval: int = settings.SLEEP_INTERVAL
    ):
        self.sleep_interval = sleep_interval

    async def fetcher_worker(self):
        while True:
            sheet_data = gsheet.read_sheet()

            for i in range(len(sheet_data)):
                row_id = i + 2
                if sheet_data[i][0] == 'Взять в работу':
                    print(f'Sent task from row {row_id} to queue')
                    gsheet.update_cell(f'A{row_id}', 'В работе')
                    worker.delay(data=sheet_data[i], row_id=row_id)

                await asyncio.sleep(self.sleep_interval)
