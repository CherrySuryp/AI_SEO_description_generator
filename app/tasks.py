from ai.service import chatgpt
from celery_app import celery
from gsheets.service import gsheet

from config import settings


@celery.task(rate_limit=f'{settings.RPM_LIMIT}/m')
def worker(data: list, row_id: int):
    prompt = gsheet.row_to_ai_prompt(data)
    req = chatgpt.send_request(prompt)

    gsheet.update_cell(f"A{row_id}", 'Завершено')
    gsheet.update_cell(f"E{row_id}", req)
