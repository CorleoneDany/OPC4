"""Represents the database"""

from tinydb import TinyDB, Query
import config


class DB:
    """Represents the tournament"""

    def __init__(self):
        """Init class with attributes."""
        self.db = TinyDB(config.DB_PATH)
