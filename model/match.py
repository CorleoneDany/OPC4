"""Represents the matchs / rounds"""


class Match:
    """Represents the matchs / rounds"""

    def __init__(self, player_1_id, player_2_id):
        """Init class with attributes."""
        self.match_id = int
        self.player_1_id = player_1_id
        self.player_2_id = player_2_id
        self.winner_id = None

    def save(self):
        pass

    def get(self):
        pass

    def all(self):
        pass
