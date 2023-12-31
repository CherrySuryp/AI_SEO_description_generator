import json
from typing import List
import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError  # noqa

import sys

sys.path.append("..")

from app.config import ProdSettings  # noqa


class GSheet:
    """
    Layer that works with Google Sheets
    :param sheet_name - Enter Google sheet name. Default = "Запросы"
    :param sheet_range - Default = "A2:E1000"
    """

    def __init__(
        self,
        sheet_name: str = "Запросы",
        sheet_range: str = "A2:J1000",
    ):
        self.settings = ProdSettings()  # Настройки

        self.gsheet_id = self.settings.GSHEET_ID  # ID таблицы
        self.sheet_name = sheet_name  # Название рабочего листа
        self.sheet_range = sheet_range  # Область, с которой работает программа

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            json.loads(self.settings.GOOGLE_CREDS),
            ["https://www.googleapis.com/auth/spreadsheets"],
        )

        # Инстанс, который работает с таблицей
        self.service = (
            discovery.build("sheets", "v4", http=credentials.authorize(httplib2.Http())).spreadsheets().values()  # noqa
        )

    def read_sheet(self) -> List[List]:
        """
        Чтение таблицы
        :return:
        """
        values = self.service.get(
            spreadsheetId=self.gsheet_id,
            range=f"{self.sheet_name}!{self.sheet_range}",
            majorDimension="ROWS",
        ).execute()
        return values["values"]

    def update_cell(self, content: str, row_id: str) -> None:
        """
        Обновление информации в таблице
        :param row_id: ID клетки
        :param content: Информация, которую нужно вставить
        :return:
        """
        self.service.update(
            spreadsheetId=self.gsheet_id,
            range=f"{self.sheet_name}!{row_id}",
            valueInputOption="USER_ENTERED",
            body={"majorDimension": "ROWS", "values": [[content]]},
        ).execute()

    def update_status(self, new_status: str, row_id: int) -> None:
        """
        Обновление статуса в таблице
        :param new_status: Новый статус
        :param row_id: Номер строки
        :return:
        """
        self.update_cell(new_status, f"A{row_id}")
