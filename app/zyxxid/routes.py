import flask

from .apps import flask_app
from .character import PDF

@flask_app.route("/pdf/<file_id>/<filename>", methods=["GET"])
def get_pdf(file_id, filename):
    data = PDF.fetch(file_id).contents
    response = flask.make_response(data)
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    response.headers["Content-Type"] = "application/pdf"

    return response
