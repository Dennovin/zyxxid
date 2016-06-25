import flask
import yaml

from .apps import flask_app
from .character import Character, PDF, create_pdf

@flask_app.route("/character/<character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.fetch(character_id)
    response = flask.make_response(yaml.dump(character))
    response.headers["Content-Type"] = "text/yaml"

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
    create_pdf(character)

    return flask.make_response("", httplib.ACCEPTED)
