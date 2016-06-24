import riak
import uuid

from .config import Config

client = riak.RiakClient(**Config.get("riak"))


class RiakStorable(object):
    @classmethod
    def bucket(cls):
        if not hasattr(cls, "_bucket"):
            cls._bucket = client.bucket(cls.__name__)

        return cls._bucket

    @property
    def id(self):
        if not hasattr(self, "_id"):
            self._id = uuid.uuid4().hex

        return self._id

    def store(self):
        key = self.bucket().new(self.id, data=self.__dict__)
        key.store()
        return self.id

    @classmethod
    def fetch(cls, key):
        obj = cls()
        obj.__dict__ = cls.bucket().get(key).data
        return obj
