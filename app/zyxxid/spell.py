import re

from . import database

class Spell(database.RiakStorable):
    _indexes = ["title"]

    @classmethod
    def load_from_file(cls, filename):
        spell = cls()

        with open(filename) as fh:
            spell.description = ""

            for line in fh:
                m = re.search("^title:.*\"(.*)\"", line)
                if m:
                    spell.title = m.group(1)

                m = re.search("^tags:.*\[(.*)\]", line)
                if m:
                    spell.tags = [i.strip() for i in m.group(1).split(",")]

                m = re.search("^\*\*(.*)\*\*", line)
                if m and not hasattr(spell, "school"):
                    spell.school = m.group(1)

                m = re.search("^\*\*Casting Time\*\*:\s*(.*)$", line)
                if m:
                    spell.casttime = m.group(1)

                m = re.search("^\*\*Range\*\*:\s*(.*)$", line)
                if m:
                    spell.range = m.group(1)

                m = re.search("^\*\*Components\*\*:\s*(.*)$", line)
                if m:
                    spell.components = m.group(1)

                m = re.search("^\*\*Duration\*\*:\s*(.*)$", line)
                if m:
                    spell.duration = m.group(1)

                if re.search("^\*\*", line):
                    spell.description = ""
                elif not re.search("^\s*$", line):
                    spell.description += line.strip() + " "

        return spell
