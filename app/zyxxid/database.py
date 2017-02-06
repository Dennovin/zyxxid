import gzip
import riak
import uuid
import yaml

from .config import Config

client = riak.RiakClient(**Config.get("riak"))


class RiakStorable(object):
    _indexes = []

    def __str__(self):
        if hasattr(self, "_id"):
            return "<{} {}>".format(self.__class__.__name__, self.id)
        else:
            return "<unsaved {} object>".format(self.__class__.__name__)

    def __repr__(self):
        return self.__str__()

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
                if isinstance(getattr(self, idx), list):
                    for val in getattr(self, idx):
                        key.add_index(idx + "_bin", val)
                else:
                    key.add_index(idx + "_bin", getattr(self, idx))

        key.store()
        return self.id

    @classmethod
    def from_dict(cls, data):
        obj = cls()
        obj.__dict__ = data
        return obj

    @classmethod
    def from_riak_obj(cls, riak_obj):
        return cls.from_dict(riak_obj.data)

    @classmethod
    def fetch(cls, key):
        return cls.from_riak_obj(cls.bucket().get(key))

    @classmethod
    def fetch_multi(cls, keys):
        for obj in cls.bucket().multiget(keys):
            yield cls.from_riak_obj(obj)

    @classmethod
    def query(cls, index, value):
        return cls.bucket().get_index(index + "_bin", value)

    @classmethod
    def list_index(cls, index):
        return cls.bucket().get_index(index + "_bin", chr(0), chr(255), return_terms=True).results

    @classmethod
    def all(cls):
        for keys in cls.bucket().stream_keys():
            yield from cls.fetch_multi(keys)

    def export(self, fh):
        yaml.dump(self.__dict__, fh, encoding="utf-8", explicit_start=True)

    @classmethod
    def export_all(cls, filename):
        with gzip.open(filename, "wb") as fh:
            for obj in cls.all():
                obj.export(fh)

    @classmethod
    def import_all(cls, filename):
        with gzip.open(filename, "rb") as fh:
            for data in yaml.load_all(fh):
                cls.from_dict(data).store()


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
