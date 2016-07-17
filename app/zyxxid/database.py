import riak
import uuid

from .config import Config

client = riak.RiakClient(**Config.get("riak"))


class RiakStorable(object):
    _indexes = []

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
        for idx in self._indexes:
            if hasattr(self, idx):
                key.add_index(idx + "_bin", getattr(self, idx))

        key.store()
        return self.id

    @classmethod
    def fetch(cls, key):
        obj = cls()
        obj.__dict__ = cls.bucket().get(key).data
        return obj

    @classmethod
    def query(cls, index, value):
        return cls.bucket().get_index(index + "_bin", value)

class RiakStorableFile(RiakStorable):
    def store(self):
        key = self.bucket().new(self.id, data=self.contents)
        key.store()
        return self.id

    @classmethod
    def store_from_file(cls, filename):
        obj = cls()
        key = cls.bucket().new_from_file(obj.id, filename)
        key.store()
        return obj

    @classmethod
    def fetch(cls, key):
        obj = cls()
        obj.contents = cls.bucket().get(key).encoded_data
        return obj
