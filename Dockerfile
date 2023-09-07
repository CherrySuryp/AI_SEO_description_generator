FROM python:3.11

# Установите необходимые зависимости для Chrome и Selenium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium

# Скачайте ChromeDriver и поместите его в каталог /usr/bin
RUN wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O /tmp/chromedriver_latest_release \
    && wget https://chromedriver.storage.googleapis.com/$(cat /tmp/chromedriver_latest_release)/chromedriver_linux64.zip -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin \
    && chmod +x /usr/bin/chromedriver

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "-u", "./app/main.py"]
