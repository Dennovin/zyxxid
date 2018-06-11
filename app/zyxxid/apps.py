import celery
import flask
import flask_caching
import jinja2
import logging
import logging.handlers
import os

from .config import Config

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(Config.get("template_dir")))

result_backend = "cache+memcached://{}/".format(";".join(Config.get("memcached_servers")))
celery_app = celery.Celery("zyxxid", broker=Config.get("celery_broker"), backend=result_backend)

celery_app.CELERY_DEFAULT_QUEUE = "default"
celery_app.CELERY_IGNORE_RESULT = False

flask_app = flask.Flask(__name__)
flask_app.jinja_env = jinja_env
flask_cache = flask_caching.Cache(flask_app, config={"CACHE_TYPE": "simple"})

log_file = os.path.join(Config.get("log_dir"), "zyxxid.log")
handler = logging.handlers.TimedRotatingFileHandler(log_file, when="midnight")
logger = logging.getLogger()
logger.addHandler(handler)
