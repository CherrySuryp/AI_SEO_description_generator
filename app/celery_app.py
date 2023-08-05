from celery import Celery

celery = Celery(
    'tasks',
    broker='memory://',
    include=['app.tasks']
)
