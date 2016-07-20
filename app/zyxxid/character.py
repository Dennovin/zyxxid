from datetime import datetime
import glob
import os
import subprocess
import tempfile
import yaml

from . import database
from .apps import celery_app, jinja_env

class Character(database.RiakStorable):
    _indexes = ["user_id"]

    def load_data(self, data):
        for k, v in data.items():
            key_parts = k.split(".")
            section = self.__dict__
            for part in key_parts[:-1]:
                if not part in section:
                    section[part] = {}
                section = section[part]

            section[key_parts[-1]] = v

    def flatten_data(self, data=None):
        if data is None:
            data = self.__dict__

        flattened_data = {}
        for k, v in data.items():
            if isinstance(v, dict):
                flattened_data.update({k + "." + sk: sv for sk, sv in self.flatten_data(v).items()})
            else:
                flattened_data[k] = v

        return flattened_data

    @classmethod
    def load_from_file(cls, filename):
        with open(filename) as fh:
            content = fh.read()
            obj_dict = yaml.load(content)

            character = cls()
            for k, v in obj_dict.items():
                setattr(character, k, v)

            return character

    def save_to_file(self, filename):
        with open(filename, "w") as fh:
            yaml.dump(self, fh)


class PDF(database.RiakStorableFile):
    output_dir = "/data/output"

    @classmethod
    def create(cls, character):
        with open(os.devnull, "w") as devnull, tempfile.NamedTemporaryFile(suffix=".tex", dir=cls.output_dir, delete=False) as tex_file:
            pdf_filename = os.path.splitext(tex_file.name)[0] + ".pdf"

            template = jinja_env.get_template("character.tex.j2")
            file_contents = template.render(c=character)
            tex_file.write(file_contents.encode("utf-8"))

            process = subprocess.Popen(["/usr/bin/xelatex", "-halt-on-error", "-interaction=batchmode", tex_file.name],
                                       cwd=cls.output_dir, stderr=devnull, stdout=devnull)

        process.wait(timeout=10)
        if process.returncode:
            print("fail")

        obj = cls.store_from_file(os.path.join(cls.output_dir, pdf_filename))

        for fn in glob.glob(os.path.join(cls.output_dir, os.path.splitext(pdf_filename)[0]) + ".*"):
            os.unlink(fn)

        return obj.id


@celery_app.task
def create_pdf(character):
    return PDF.create(character)
