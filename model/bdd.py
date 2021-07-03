"""Represent the database."""

from tinydb import TinyDB, table
import config


class DB:
    """Represent the database."""

    table = TinyDB(config.DB_PATH).table("")

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

    @classmethod
    def drop(cls):
        """Drop the data in the object's table."""
        cls.table.drop_table(table)

    def save(self):
        """Save the object in the database."""
        document = self.serialized()
        if self.doc_id:
            self.table.update(document, doc_ids=[self.doc_id])
        else:
            self.doc_id = self.table.insert(document)

    def return_id(self):
        """Return the document's ID."""
        return self.doc_id
