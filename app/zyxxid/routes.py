import flask
import http.client
import oauth2client.client
import oauth2client.crypt
import simplejson
import string

from .apps import flask_app
from .character import Character, PDF, create_pdf
from .config import Config
from .spell import Spell

def verify_token(token):
    try:
        idinfo = oauth2client.client.verify_id_token(token, Config.get("oauth2_client_id"))
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise oauth2client.crypt.AppIdentityError("Wrong issuer.")

        return idinfo

    except oauth2client.crypt.AppIdentityError:
        return False

def json_response(data):
    response = flask.make_response(simplejson.dumps(data))
    response.headers["Content-Type"] = "text/json"

    return response

@flask_app.route("/character/<character_id>", methods=["GET"])
def get_character(character_id):
    character = Character.fetch(character_id)
    return json_response(character.flatten_data())

@flask_app.route("/character", methods=["POST"])
def post_character():
    idinfo = verify_token(flask.request.cookies.get("googletoken"))
    if not idinfo:
        return flask.make_response("", http.client.UNAUTHORIZED)

    obj = flask.request.get_json()

    if obj.get("character_id"):
        character = Character.fetch(obj["character_id"])
        if character.user_id != idinfo["sub"]:
            return flask.make_response("", http.client.UNAUTHORIZED)
    else:
        character = Character()
        character.user_id = idinfo["sub"]

    character.load_data(obj)
    id = character.store()

    return json_response({"id": id})

@flask_app.route("/character", methods=["GET"])
def list_characters():
    idinfo = verify_token(flask.request.cookies.get("googletoken"))
    if not idinfo:
        return flask.make_response("", http.client.UNAUTHORIZED)

    characters = {}
    for id in Character.query("user_id", idinfo["sub"]).results:
        characters[id] = Character.fetch(id).name

    return json_response(characters)

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

    return json_response({"filename": filename, "status_url": flask.url_for("check_pdf_status", task_id=task.task_id, filename=filename)})

@flask_app.route("/pdf/status/<task_id>/<filename>", methods=["GET"])
def check_pdf_status(task_id, filename):
    result = create_pdf.AsyncResult(task_id)
    if result.ready():
        data = { "ready": True, "url": flask.url_for("get_pdf", file_id=result.result, filename=filename) }
    else:
        data = { "ready": False }

    return json_response(data)

@flask_app.route("/spells/by-tag/<tag>", methods=["GET"])
def list_spells_by_tag(tag):
    spell_names = {i[1]: i[0] for i in Spell.list_index("title")}
    spell_levels = {i[1]: i[0] for i in Spell.list_index("level")}
    tagged_spells = Spell.query("tags", tag)

    data = [{"name": spell_names[i], "id": i, "level": spell_levels[i]} for i in tagged_spells]

    return json_response(data)

@flask_app.route("/spells", methods=["GET"])
def list_spells():
    spell_names = Spell.list_index("title")
    spell_levels = {i[1]: i[0] for i in Spell.list_index("level")}

    data = [{"name": i[0], "id": i[1], "level": spell_levels[i[1]]} for i in spell_names]

    return json_response(data)

@flask_app.route("/spell/<spell_id>", methods=["GET"])
def get_spell(spell_id):
    spell = Spell.fetch(spell_id)
    return json_response(spell.__dict__)

@flask_app.route("/", methods=["GET"])
def index():
    spell_names = sorted(Spell.list_index("title"), key=lambda i: i[0])
    spell_levels = {i[1]: i[0] for i in Spell.list_index("level")}

    spells = {}
    for name, spell_id in spell_names:
        level = spell_levels[spell_id]
        spells[level] = spells.get(level, [])
        spells[level].append({"id": spell_id, "name": name})

    return flask.render_template("index.html.j2", spells=spells)
