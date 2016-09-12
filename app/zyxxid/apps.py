import celery
import flask
import jinja2
import pylibmc

from .config import Config

jinja_env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, "templates"))

result_backend = "cache+memcached://{}/".format(";".join(Config.get("memcached_servers")))
celery_app = celery.Celery("zyxxid", broker=Config.get("celery_broker"), backend=result_backend)

celery_app.CELERY_DEFAULT_QUEUE = "default"
celery_app.CELERY_IGNORE_RESULT = False

flask_app = flask.Flask(__name__)
flask_app.jinja_env = jinja_env

memcached_client = pylibmc.Client(Config.get("memcached_servers"), binary=True, behaviors={"tcp_nodelay": True, "ketama": True})
