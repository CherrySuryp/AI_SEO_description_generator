from celery import Celery
import sys
sys.path.append('..')

celery = Celery(
    'app',
    broker='redis://localhost:6379',
    include=['tasks']
)
