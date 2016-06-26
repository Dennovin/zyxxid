import celery
import flask

from .config import Config

celery_app = celery.Celery("zyxxid", broker=Config.get("celery_broker"), backend=Config.get("celery_result_backend"))

celery_app.CELERY_DEFAULT_QUEUE = "default"
celery_app.CELERY_IGNORE_RESULT = False

flask_app = flask.Flask(__name__)
