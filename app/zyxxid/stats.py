import flask
import requests
import simplejson
import statsd
from celery.contrib.batches import Batches
from celery.signals import task_prerun, task_postrun
from datetime import datetime

from .apps import celery_app, flask_app
from .config import Config

task_start = {}
statsd_client = statsd.StatsClient(Config.get("statsd_hostname"), 8125)

@flask_app.before_request
def before_request():
    flask.g.request_start = datetime.utcnow()

@flask_app.after_request
def after_request(response):
    req_key = "flask.{}".format(flask.request.endpoint)
    statsd_client.incr(req_key + ".count")
    statsd_client.timing(req_key + ".timing", (datetime.utcnow() - flask.g.request_start).total_seconds() * 1000)
    return response

@task_prerun.connect
def before_task(signal, sender, task_id, task, args, kwargs):
    task_start[task_id] = datetime.utcnow()

@task_postrun.connect
def after_task(signal, sender, task_id, task, args, kwargs, retval, state):
    req_key = "celery.{}".format(task.name)
    statsd_client.incr(req_key + ".count")
    statsd_client.timing(req_key + ".timing", (datetime.utcnow() - task_start.pop(task_id)).total_seconds() * 1000)
