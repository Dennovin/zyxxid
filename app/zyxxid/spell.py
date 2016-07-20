import re

from . import database

class Spell(database.RiakStorable):
    _indexes = ["title", "level", "tags"]

    @classmethod
    def load_from_file(cls, filename):
        spell = cls()

        with open(filename) as fh:
            spell.description = ""
            spell.ritual = False

            for line in fh:
                header_line = False

                m = re.search("^title:.*\"(.*)\"", line)
                if m:
                    spell.title = m.group(1)
                    header_line = True

                m = re.search("^tags:.*\[(.*)\]", line)
                if m:
                    spell.tags = [i.strip() for i in m.group(1).split(",")]
                    if "cantrip" in spell.tags:
                        spell.level = 0
                    else:
                        for tag in spell.tags:
                            if tag.startswith("level") and tag[-1].isdigit():
                                spell.level = int(tag[-1])
                    header_line = True

                m = re.search("^\*\*(.*)\*\*", line)
                if m and not hasattr(spell, "school"):
                    spell.school = m.group(1)
                    if spell.school.endswith("(ritual)"):
                        spell.school = spell.school.replace("(ritual)", "").strip()
                        spell.ritual = True

                    header_line = True

                m = re.search("^\*\*Casting Time\*\*:\s*(.*)$", line)
                if m:
                    spell.casttime = m.group(1)
                    header_line = True

                m = re.search("^\*\*Range\*\*:\s*(.*)$", line)
                if m:
                    spell.range = m.group(1)
                    header_line = True

                m = re.search("^\*\*Components\*\*:\s*(.*)$", line)
                if m:
                    spell.components = m.group(1)
                    header_line = True

                m = re.search("^\*\*Duration\*\*:\s*(.*)$", line)
                if m:
                    spell.duration = m.group(1)
                    header_line = True

                if header_line:
                    spell.description = ""
                else:
                    spell.description += line + "\n"

        return spell
