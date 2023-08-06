import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = '/home/markarkhipychev/PycharmProjects/AI_SEO_description_generator/app/gsheets/creds.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets']
)


class GSheet:

    def __init__(self, sheet_name: str, sheet_range: str, gsheet_id: str, sheet_result_col: str):
        self.httpAuth = credentials.authorize(httplib2.Http())
        self.service = discovery.build('sheets', 'v4', http=self.httpAuth).spreadsheets().values()

        self.SPREADSHEET_ID = gsheet_id
        self.sheet_name = sheet_name
        self.sheet_range = sheet_range
        self.sheet_result_col = sheet_result_col

    def read_sheet(self) -> list:
        values = self.service.get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f'{self.sheet_name}!{self.sheet_range}',
            majorDimension='ROWS'
        ).execute()

        return values['values']

    def update_cell(self, cell_id: str, content: str):
        self.service.update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f'{self.sheet_name}!{cell_id}',
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': [[content]]
            }
        ).execute()

    @staticmethod
    def row_to_ai_prompt(data: list) -> str:
        item_name = data[1]
        base_prompt = data[2]
        keywords = data[3]
        prompt = (f'Задача: {base_prompt}. \n'
                  f' Товар: {item_name}. \n'
                  f' Ключевые слова: {keywords}')

        return prompt


gsheet = GSheet(
    sheet_name='Запросы',
    sheet_range='A2:E1000',
    sheet_result_col='E',
    gsheet_id='1fm-V527jP4zBWbIMw3r83lOzEgvAprB2Qi4K32i1HCw',
)
