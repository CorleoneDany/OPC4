"""Represents the database"""

from tinydb import TinyDB, Query
import config


class DB:
    """Represents the database"""

    table = TinyDB(config.DB_PATH)

    @classmethod
    def get(cls, doc_id):
        document = cls.table.get(doc_id=doc_id)
        return cls.deserialized(document)

    @classmethod
    def list(cls):
        return [cls.deserialized(document) for document in cls.table.all()]

    def serialized(self):
        pass

    @classmethod
    def deserialized(self):
        pass

    def save(self):
        document = self.serialized()
        if self.doc_id:
            self.table.update(document, doc_ids=[self.doc_id])
        else:
            self.doc_id = self.table.insert(document)
