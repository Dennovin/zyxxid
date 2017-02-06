import flask
import functools
import http.client
import oauth2client.client
import oauth2client.crypt
import random
import simplejson
import string

from .apps import flask_app
from .character import Character, PDF, Template, ShareLink, create_pdf
from .config import Config
from .spell import Spell

loading_messages = [
    "Splitting the party",
    "Rolling for initiative",
    "Stalling for time",
    "Adding random character flaws",
    "Folding pages in your spellbook",
    "Translating into Draconic",
    "Removing all vowels from character sheet",
    "Redoing everything in Comic Sans",
    "Defacing ancient Dwarven artifacts",
    "Punting gnomes",
    "Rolling sneak attack damage",
    "Using up all your spell slots",
    "Generating sarcastic animal companion",
    "Making you a sandwich",
    "Complaining",
    "Feigning death",
    "Killing the bard",
    "Forging titles of nobility",
    "Hi Mom!",
    "Drastically underestimating encounters",
    "Taking an extended rest",
    "Starting lengthy argument about rules",
    "Checking for traps",
    "Painting miniatures",
    "Casting Magic Missile at the darkness",
    "Adding dinosaurs to your campaign",
    "Turning campagin into fantasy football league",
    "Doing wizard things. You wouldn't understand.",
    "Elfsplaining",
    "Building dice towers",
    "Ordering more pizza",
    "Dropping rocks on everyone",
    "Generating cryptic riddles",
    "Brewing mysterious potions",
    "Spilling mysterious potions",
]

spell_list = None


def get_loading_message():
    msg = random.choice(loading_messages)
    if msg[-1].isalpha():
        msg += "..."

    return msg

def verify_token(token):
    try:
        idinfo = oauth2client.client.verify_id_token(token, Config.get("oauth2_client_id"))
        if idinfo["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            raise oauth2client.crypt.AppIdentityError("Wrong issuer.")

        return idinfo

    except oauth2client.crypt.AppIdentityError:
        return False

def login_required(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        idinfo = verify_token(flask.request.cookies.get("googletoken"))
        if not idinfo:
            return flask.make_response("", http.client.UNAUTHORIZED)

        return func(idinfo["sub"], *args, **kwargs)

    return inner_func

def json_response(data):
    response = flask.make_response(simplejson.dumps(data))
    response.headers["Content-Type"] = "text/json"

    return response

@flask_app.route("/character/<character_id>", methods=["GET"])
@login_required
def get_character(user_id, character_id):
    character = Character.fetch(character_id)
    if not character:
        return flask.make_response("", http.client.NOT_FOUND)
    if character.user_id != user_id:
            return flask.make_response("", http.client.UNAUTHORIZED)

    return json_response(character.flatten_data())

@flask_app.route("/character", methods=["POST"])
@login_required
def post_character(user_id):
    obj = flask.request.get_json()

    if obj.get("character_id"):
        character = Character.fetch(obj["character_id"])
        if character.user_id != user_id:
            return flask.make_response("", http.client.UNAUTHORIZED)
    else:
        character = Character()
        character.user_id = user_id

    character.load_data(obj)
    id = character.store()

    return json_response({"id": id})

@flask_app.route("/character/share", methods=["POST"])
def share_character():
    obj = flask.request.get_json()

    share_link = ShareLink.from_character_info(obj)
    share_link.store()

    return json_response({"link_id": share_link.id})

@flask_app.route("/shared/<link_id>", methods=["GET"])
def get_shared_character(link_id):
    share_link = ShareLink.fetch(link_id)
    character = share_link.copy_to_character()

    return json_response(character.flatten_data())

@flask_app.route("/character/<character_id>", methods=["DELETE"])
@login_required
def delete_character(user_id, character_id):
    character = Character.fetch(character_id)
    if character.user_id != user_id:
        return flask.make_response("", http.client.UNAUTHORIZED)

    character.deleted = True
    character.store()

    return json_response({"id": character._id})

@flask_app.route("/character/undelete/<character_id>", methods=["POST"])
@login_required
def undelete_character(user_id, character_id):
    character = Character.fetch(character_id)
    if character.user_id != user_id:
        return flask.make_response("", http.client.UNAUTHORIZED)

    delattr(character, "deleted")
    character.store()

    return json_response({"id": character._id})

@flask_app.route("/character", methods=["GET"])
@login_required
def list_characters(user_id):
    characters = {}
    for id in Character.query("user_id", user_id).results:
        character = Character.fetch(id)
        if hasattr(character, "deleted") and character.deleted:
            continue

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
@login_required
def submit_pdf():
    obj = flask.request.get_json()
    task = create_pdf.delay(obj, obj["template_name"])
    filename = "".join([i for i in obj["name"] if i in string.ascii_letters]) + ".pdf"

    return json_response({
        "filename": filename,
        "status_url": flask.url_for("check_pdf_status", task_id=task.task_id, filename=filename),
        "loading_message": get_loading_message(),
    })

@flask_app.route("/pdf/status/<task_id>/<filename>", methods=["GET"])
def check_pdf_status(task_id, filename):
    result = create_pdf.AsyncResult(task_id)
    if result.ready():
        data = { "ready": True, "url": flask.url_for("get_pdf", file_id=result.result, filename=filename) }
    else:
        data = { "ready": False, "loading_message": get_loading_message() }

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
def index(share_link_id=None):
    spells = getattr(flask.g, "_spells", None)
    if spells is None:
        spell_names = sorted(Spell.list_index("title"), key=lambda i: i[0])
        spell_levels = {i[1]: i[0] for i in Spell.list_index("level")}

        spell_tags = {}
        for tag, spell_id in Spell.list_index("tags"):
            spell_tags[spell_id] = spell_tags.get(spell_id, [])
            spell_tags[spell_id].append(tag)

        spells = {}
        for name, spell_id in spell_names:
            level = spell_levels[spell_id]
            spells[level] = spells.get(level, [])
            spells[level].append({"id": spell_id, "name": name, "tags": spell_tags.get(spell_id, []) })

        flask.g._spells = spells

    templates = getattr(flask.g, "_templates", None)
    if templates is None:
        templates = sorted(Template.list_templates(), key=lambda i: i.name)
        flask.g._templates = templates

    return flask.render_template("index.html.j2", spells=spells, templates=templates)
