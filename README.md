# Генератор SEO описаний для Wildberries и Ozon

Использование ChatGPT 3.5 для генерации SEO описаний
на основе указанных ключевых слов и характеристик товара.
В качестве интерфейса для взаимодействия используются Google таблицы
---
## Установка и настройка

### 1. Google таблица
Для работы необходимо создать сервисный аккаунт Google.  
О том как его создать можно посмотреть [в этом видео](https://youtu.be/caiR7WAGMVM?t=100)

1. Скопируйте таблицу - [cсылка](https://docs.google.com/spreadsheets/d/19foQkqEQusXWiEW6utm5vwCnWSGi2Ztj6M-FUJRWFL8/edit#gid=0)
2. Выдайте права доступа сервисному аккаунту Google


### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Конфигурационный файл .env
В корне проекта находится конфигурационный файл **.env.example**

```.env
MODE=DEV # Режим работы DEV/PROD

OPENAI_KEY= # API ключ для ChatGPT
RPM_LIMIT=3 # ЛИмит запросов в минуту. Для бесплатных аккаунтов лимит - 3 запросы в минуту
GPT_MODEL=gpt-3.5-turbo-16k

SENTRY_DSN= # DSN ключ для Sentry

REFRESH_INTERVAL=10 # Интервал чьения таблицы в секундах
GSHEET_ID= # ID Google таблицы
GOOGLE_CREDS= # Информация о сервисном аккаунте Google
```

## Запуск
Проект состоит из двух частей:  
1. Опрос Google таблицы на наличие новых задач
2. Обработка задач в фоновом режиме с использованием Celery

### Локальный запуск
При запуске программы локально, в файле .env необходимо установить MODE в значение DEV  

Для запуска потребуется локально установленный и запущенный Redis по адресу
```127.0.0.1:6379```(по умолчанию)
#### 1. Запуск опроса таблицы
```bash
cd app
chmod +x main.py
./main.py
```

#### 2. Запуск Celery
Запуск в отдельном терминале
```bash
cd app
celery -A tasks:celery worker --pool=prefork --concurrency=4 --loglevel=INFO
```

### Запуск в Docker-Compose
При запуске программы в docker, в файле .env необходимо установить MODE в значение PROD

```bash
docker compose build
docker compose up
```

ВАЖНО!  
При изменении конфигурации программы необходимо пересобрать контейнер
```bash
docker compose up --build
```

