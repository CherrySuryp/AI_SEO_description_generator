import asyncio

from gsheets.service import gsheet
from tasks import worker


async def main():
    while True:
        sheet_data = gsheet.read_sheet()
        for i in range(len(sheet_data)):
            row_id = i + 2
            if sheet_data[i][0] == 'Взять в работу':
                gsheet.update_cell(f'A{row_id}', 'В работе')
                worker(data=sheet_data[i], row_id=row_id).apply_async()
        print('Waiting....')
        await asyncio.sleep(10)

asyncio.run(main())
