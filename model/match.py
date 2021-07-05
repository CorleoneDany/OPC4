"""Represents the matchs / rounds."""

from tinydb import TinyDB


from .bdd import DB
import config


class Match(DB):
    """Represent the matchs / rounds."""

    table = TinyDB(config.DB_PATH).table("match")

    def __init__(
        self,
        player_1,
        player_2,
        doc_id=None,
        winner_alias=None,
    ):
        """Init class with attributes."""
        self.doc_id = doc_id
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner_alias = winner_alias

    @property
    def alias(self):
        """Return the match's alias."""
        return f"{self.player_1.alias} contre {self.player_2.alias}"

    def serialized(self):
        """Return the serialized object."""
        return {
            "player_1": self.player_1.doc_id,
            "player_2": self.player_2.doc_id,
            "winner_alias": self.winner_alias,
        }

    @classmethod
    def deserialized(cls, document):
        """Return the deserialized object."""
        match = Match(**document)
        match.doc_id = document.doc_id
        return match

    @classmethod
    def get_many_matchs(cls, matchs_id, players):
        """Get many matches from a list of ids."""
        matchs = []
        for match_id in matchs_id:
            matchs.append(cls.get(match_id, players))
        return matchs

    @classmethod
    def get(cls, doc_id, players):
        """Get a match with its id."""
        match = cls.table.get(doc_id=doc_id)
        for player in players:
            if match["player_1"] == player.doc_id:
                match["player_1"] = player
            if match["player_2"] == player.doc_id:
                match["player_2"] = player

        return cls.deserialized(match)

    def finish(self, winner):
        """Update the score."""
        if winner == 1:
            self.player_1.score += 1
            self.winner_alias = self.player_1.alias
        elif winner == 2:
            self.player_2.score += 1
            self.winner_alias = self.player_2.alias
        elif winner == 0:
            self.player_1.score += 0.5
            self.player_2.score += 0.5
            self.winner_alias = "Match nul"
        self.save()
