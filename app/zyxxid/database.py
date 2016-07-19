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
    def from_riak_obj(cls, riak_obj):
        obj = cls()
        obj.__dict__ = riak_obj.data
        return obj

    @classmethod
    def fetch(cls, key):
        return cls.from_riak_obj(cls.bucket().get(key))

    @classmethod
    def query(cls, index, value):
        return cls.bucket().get_index(index + "_bin", value)

    @classmethod
    def list_index(cls, index):
        return cls.bucket().get_index(index + "_bin", chr(0), chr(255), return_terms=True).results

    @classmethod
    def all(cls):
        objs = []
        for keys in cls.bucket().stream_keys():
            objs.extend([cls.from_riak_obj(i) for i in cls.bucket().multiget(keys)])

        return objs

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
