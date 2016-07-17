import flask
import http.client
import simplejson
import string

from .apps import flask_app
from .character import Character, PDF, create_pdf

@flask_app.route("/character/<character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.fetch(character_id)
    response = flask.make_response(simplejson.dumps(character))
    response.headers["Content-Type"] = "text/json"

    return response

@flask_app.route("/character", methods=["POST"])
def post_character():
    character = Character()
    obj = flask.request.get_json()
    flask_app.logger.warning(obj)

    for k, v in obj.items():
        setattr(character, k, v)

    id = character.store()

    response = flask.make_response(simplejson.dumps({"id": id}))
    response.headers["Content-Type"] = "text/json"

    return response

@flask_app.route("/pdf/<file_id>/<filename>", methods=["GET"])
def get_pdf(file_id, filename):
    data = PDF.fetch(file_id).contents
    response = flask.make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    response.headers["Content-Type"] = "application/pdf"

    return response

@flask_app.route("/pdf", methods=["POST"])
def submit_pdf():
    character = Character.fetch(flask.request.form["character_id"])
    task = create_pdf.delay(character)
    filename = "".join([i for i in character.name if i in string.ascii_letters]) + ".pdf"

    return flask.redirect(flask.url_for("check_pdf_status", task_id=task.task_id, filename=filename))

@flask_app.route("/pdf/status/<task_id>/<filename>", methods=["GET"])
def check_pdf_status(task_id, filename):
    result = create_pdf.AsyncResult(task_id)
    if result.ready():
        return flask.redirect(flask.url_for("get_pdf", file_id=result.result, filename=filename))
    else:
        response = flask.make_response("", http.client.ACCEPTED)
        response.headers["Retry-After"] = 1
        return response
