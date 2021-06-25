"""Represents the database"""

from tinydb import TinyDB, Query
import config


class DB:
    """Represent the database."""

    table = TinyDB(config.DB_PATH)

    @classmethod
    def get(cls, doc_id):
        """Get the object with its ID from the DB."""
        document = cls.table.get(doc_id=doc_id)
        return cls.deserialized(document)

    @classmethod
    def list(cls):
        """Print all the object in the table."""
        return [cls.deserialized(document) for document in cls.table.all()]

    def serialized(self):
        """Return the serialized object."""
        pass

    @classmethod
    def deserialized(self):
        """Return the deserialized object."""
        pass

    def save(self):
        """Save the object in the database."""
        document = self.serialized()
        if self.doc_id:
            self.table.execute(document, doc_ids=[self.doc_id])
        else:
            self.doc_id = self.table.insert(document)
