import celery

from .config import Config

celery_app = celery.Celery("zyxxid", broker=Config.get("celery_broker"))

celery_app.CELERY_DEFAULT_QUEUE = "default"
celery_app.CELERY_RESULT_BACKEND = Config.get("celery_broker")
