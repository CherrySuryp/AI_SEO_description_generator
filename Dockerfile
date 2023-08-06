FROM python:3.11.4
LABEL authors="markarkhipychev"

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "./app/run.py"]