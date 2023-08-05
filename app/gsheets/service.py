from pprint import pprint

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = '../../gsheets_creds.json'


class GSheet:

    def __init__(self, sheet_name: str, sheet_range: str, gsheet_id: str, sheet_result_col: str):

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets']
        )

        self.httpAuth = credentials.authorize(httplib2.Http())
        self.sheets_service = discovery.build('sheets', 'v4', http=self.httpAuth)

        self.gsheet_id = gsheet_id
        self.sheet_name = sheet_name
        self.sheet_range = sheet_range
        self.sheet_result_col = sheet_result_col

    def read_sheet(self) -> list:
        values = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=self.gsheet_id,
            range=f'{self.sheet_name}!{self.sheet_range}',
            majorDimension='ROWS'
        ).execute()

        return values['values']

    @staticmethod
    def row_to_ai_prompt(data: list):
        content = []
        for row in range(len(data)):
            status = data[row][0]
            item_name = data[row][1]
            base_prompt = data[row][2]
            keywords = data[row][3]

            if status == 'Взять в работу':
                prompt = {
                    'row_id': row + 2,
                    'task': f'Задача: {base_prompt}. \n'
                            f'Товар: {item_name}. \n'
                            f'Ключевые слова: {keywords}'
                }
                content.append(prompt)
        return content


gsheet = GSheet(
    sheet_name='Запросы',
    sheet_range='A2:E1000',
    sheet_result_col='E',
    gsheet_id='1fm-V527jP4zBWbIMw3r83lOzEgvAprB2Qi4K32i1HCw',
)

print(gsheet.row_to_ai_prompt(gsheet.read_sheet()))
