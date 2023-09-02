FROM python:3.11

RUN pip install poetry
COPY . .
RUN poetry install --no-dev

CMD ["python", "-u", "./app/main.py"]