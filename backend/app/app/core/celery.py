import os

from celery import Celery
from celery.utils.log import get_task_logger

broker = os.getenv("CELERY_BROKER_URL")
backend = os.getenv("CELERY_BACKEND_URL")

celery_app = Celery("worker", broker=broker, backend=backend)
celery_log = get_task_logger(__name__)
