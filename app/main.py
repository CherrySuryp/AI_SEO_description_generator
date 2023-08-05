import asyncio

from app.gsheets.service import gsheet
from app.tasks import worker


async def main():
    while True:
        sheet_data = gsheet.read_sheet()

        for i in range(len(sheet_data)):
            row = i + 2
            if sheet_data[i][0] == 'Взять в работу':
                gsheet.update_cell(f'A{row}', 'В работе')
                worker().delay(data=sheet_data[i], row_id=row)
        print('Спать')
        await asyncio.sleep(10)

asyncio.run(main())
