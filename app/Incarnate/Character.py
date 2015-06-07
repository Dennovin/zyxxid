import yaml

class Character(object):
    @classmethod
    def load_from_file(cls, filename):
        with open(filename) as fh:
            content = fh.read()
            obj_dict = yaml.load(content)

            character = cls()
            for k, v in obj_dict.items():
                setattr(character, k, v)

            return character
