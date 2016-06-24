import os
import yaml

class Config(object):
    settings = None
    parsed = False
    config_file = "/data/etc/zyxxid.yaml"

    @classmethod
    def get(cls, item, default=None):
        if not cls.parsed:
            cls.parse()

        return cls.settings.get(item, default)

    @classmethod
    def parse(cls):
        with open(cls.config_file, "r") as fh:
            contents = fh.read()
            cls.settings = yaml.load(contents)
            cls.parsed = True
