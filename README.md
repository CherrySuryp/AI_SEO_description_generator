# Генератор SEO описаний для Wildberries и Ozon

Использование ChatGPT 3.5 для генерации SEO описаний на основе указанных ключевых слов и характеристик товара.  
В качестве интерфейса для взаимодействия используются Google таблицы
---
## Установка и настройка

### 1. Google таблица
Для работы необходимо создать сервисный аккаунт Google.  
О том как его создать можно посмотреть [в этом видео](https://youtu.be/caiR7WAGMVM?t=100)

1. Скопируйте таблицу - [cсылка](https://docs.google.com/spreadsheets/d/19foQkqEQusXWiEW6utm5vwCnWSGi2Ztj6M-FUJRWFL8/edit#gid=0)
2. Выдайте права доступа сервисному аккаунту Google

---

### 2. Установка виртуального окружения
```bash
python -m venv venv
```
**Активация venv для Windows:**
```bash
\venv\Scripts\activate.bat
```
**Активация для Linux**
```bash
source venv/bin/activate
```
---
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Конфигурационный файл .env
В корне проекта находится конфигурационный файл **".env.example"**,
его необходимо переименовать в **".env"**
```.env
# DEV - Для локального запуска
# PROD - для запуска в Docker
MODE=DEV

OPENAI_KEY= # API ключ для ChatGPT
RPM_LIMIT=3 # Лимит запросов в минуту. Лимит для бесплатных аккаунтов - 3 запроса в минуту
GPT_MODEL=gpt-3.5-turbo-16k

USE_SENTRY=FALSE # TRUE | FALSE. Если не хотите использовать Sentry для логирования, то оставьте FALSE
SENTRY_DSN='' # DSN ключ для Sentry

REFRESH_INTERVAL=10 # Интервал чтения таблицы в секундах
GSHEET_ID= # ID Google таблицы
GOOGLE_CREDS= # Информация о сервисном аккаунте Google
```
---
## Запуск
Проект состоит из двух частей:  
1. Опрос Google таблицы
2. Обработка новых задач в фоновом режиме с использованием Celery

### Локальный запуск
При запуске программы локально, в файле **".env"** необходимо установить MODE в значение DEV  

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
При запуске программы в docker, в файле **".env"** необходимо установить MODE в значение PROD

```bash
docker compose build
docker compose up
```

**ВАЖНО!**  
Каждый раз при изменении конфигурации программы необходимо пересобирать контейнер
```bash
docker compose up --build
```
---

# Использование
Для того чтобы начать работу, необходимо:
1. Запустить программу
2. Занести задачи в Google таблицу
3. Сменить статус на "взять в работу"
![Задача](https://github.com/CherrySuryp/AI_SEO_description_generator/blob/master/images/sheet.png)
