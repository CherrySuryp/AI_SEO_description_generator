import json

import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

import sys

sys.path.append("..")

from app.config import settings  # noqa

CREDENTIALS_FILE = json.loads(settings.GOOGLE_CREDS)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    CREDENTIALS_FILE, ["https://www.googleapis.com/auth/spreadsheets"]
)


class GSheet:
    """
    Layer that works with Google Sheets
    :param spreadsheet_id - Copy it from Google sheet link
    :param sheet_name - Enter Google sheet name
    :param sheet_range - e.g. "A1:E100"
    :param sheet_result_col - Enter a column name that will be used to store results
    """

    def __init__(
        self,
        sheet_name: str = "Запросы",
        sheet_range: str = "A2:E1000",
        sheet_result_col: str = "E",
        spreadsheet_id: str = settings.GSHEET_ID,
    ):
        http_auth = credentials.authorize(httplib2.Http())
        self.service = (
            discovery.build("sheets", "v4", http=http_auth).spreadsheets().values()
        )

        self.SPREADSHEET_ID = spreadsheet_id
        self.sheet_name = sheet_name
        self.sheet_range = sheet_range
        self.sheet_result_col = sheet_result_col

    def read_sheet(self) -> list:
        values = self.service.get(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f"{self.sheet_name}!{self.sheet_range}",
            majorDimension="ROWS",
        ).execute()

        return values["values"]

    def update_cell(self, cell_id: str, content: str) -> None:
        self.service.update(
            spreadsheetId=self.SPREADSHEET_ID,
            range=f"{self.sheet_name}!{cell_id}",
            valueInputOption="USER_ENTERED",
            body={"majorDimension": "ROWS", "values": [[content]]},
        ).execute()


gsheet = GSheet()
