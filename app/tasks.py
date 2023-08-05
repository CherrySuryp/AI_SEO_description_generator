from app.ai.service import chatgpt
from app.celery_app import celery
from app.gsheets.service import gsheet


@celery.task
def worker(data: list, row_id: int):
    prompt = gsheet.row_to_ai_prompt(data)
    req = chatgpt.send_request(prompt)

    gsheet.update_cell(f"A{row_id}", 'Завершено')
    gsheet.update_cell(f"E{row_id}", req)