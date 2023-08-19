from celery import Celery
from config import redis_path
import sys

sys.path.append("..")

celery = Celery("app", broker=redis_path, include=["tasks"])
