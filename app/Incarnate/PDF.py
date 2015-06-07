from jinja2 import Environment, PackageLoader, Template
import os
import tempfile
import subprocess

class PDF(object):
    env = Environment(loader=PackageLoader(__name__, "templates"))
    tex_dir = "/data/tex"

    @classmethod
    def write_pdf(cls, character):
        character_file = tempfile.NamedTemporaryFile(delete=True, suffix=".tex", dir=cls.tex_dir)
        pdf_filename = os.path.splitext(character_file.name)[0] + ".pdf"

        template = cls.env.get_template("character.tex.j2")
        file_contents = template.render(c=character)
        character_file.write(file_contents)

        with open(os.devnull, "w") as devnull:
            process = subprocess.Popen(["/usr/bin/xelatex", "-halt-on-error", "-interaction=batchmode", character_file.name],
                                       cwd=cls.tex_dir, stderr=devnull, stdout=devnull)

        return pdf_filename

