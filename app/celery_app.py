from celery import Celery
import sys
sys.path.append('..')

celery = Celery(
    'app',
    broker='redis://redis:6379/0',
    include=['tasks']
)
