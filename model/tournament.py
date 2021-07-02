"""Represents the tournament."""

from tinydb import TinyDB

from .bdd import DB
from .match import Match
from .player import Player
import config


class Tournament(DB):
    """Represents the tournament."""

    table = TinyDB(config.DB_PATH).table("tournament")

    def __init__(
        self,
        name,
        location,
        start_date,
        ending_date,
        desc,
        doc_id=None,
        players=[],
        matchs=[],
        first_team=[],
        second_team=[],
    ):
        """Init class with attributes."""
        self.doc_id = doc_id
        self.name = name
        self.location = location
        self.players = players
        self.matchs = matchs
        self.start_date = start_date
        self.ending_date = ending_date
        self.desc = desc
        self.first_team = first_team
        self.second_team = second_team

    def serialized(self):
        """Return the serialized object."""
        return {
            "name": self.name,
            "location": self.location,
            "players": self.get_players_ids(),
            "matchs": self.get_matchs_ids(),
            "start_date": self.start_date,
            "ending_date": self.ending_date,
            "desc": self.desc,
            "first_team": self.get_first_team_ids(),
            "second_team": self.get_second_team_ids(),
        }

    @classmethod
    def deserialized(cls, document):
        """Return the deserialized object."""
        tournament = Tournament(**document)
        tournament.doc_id = document.doc_id
        return tournament

    @property
    def current_turn(self):
        """Return the alias of the player."""
        return self.turn[-1] if self.turns else None

    def create_first_turn(self):
        """Create the first matchs."""
        sorted_players = sorted(self.players, key=lambda player: player.rank)
        self.first_team = sorted_players[0:4]
        self.second_team = sorted_players[4:8]

        for index in range(len(self.first_team)):
            match = Match(self.first_team[index], self.second_team[index])
            match.save()
            self.matchs.append(match)

    def create_next_turn(self):
        """Create the next matchs."""
        sorted_first_team = sorted(self.first_team, key=lambda player: player.score)
        sorted_second_team = sorted(self.second_team, key=lambda player: player.score)

        for index in range(len(sorted_first_team)):
            match = Match(sorted_first_team[index], sorted_second_team[index])
            match.save()
            self.matchs.append(match)

    def create_turn(self):
        """Create the first turn or the next one based on the state of the turns."""
        if not self.matchs:
            self.create_first_turn()
        else:
            self.create_next_turn()

    def get_match(self, doc_id):
        """Return an existing match with its ID."""
        for match in self.matchs:
            if match.doc_id == doc_id:
                return match

    def get_player(self, doc_id):
        """Return an existing player with its ID."""
        for player in self.players:
            if player.doc_id == doc_id:
                return player

    def get_matchs_ids(self):
        """Return the list of all the IDs of the tournament's matchs."""
        matchs_ids = []
        for match in self.matchs:
            matchs_ids.append(match.return_id())
        return matchs_ids

    def get_players_ids(self):
        """Return the list of all the IDs of the tournament's players."""
        players_ids = []
        for player in self.players:
            players_ids.append(player.return_id())
        return players_ids

    def get_first_team_ids(self):
        player_ids = []
        for player in self.first_team:
            player_ids.append(player.return_id())
        return player_ids

    def get_second_team_ids(self):
        player_ids = []
        for player in self.second_team:
            player_ids.append(player.return_id())
        return player_ids

    def turn_finished(self):
        """Verify if all the matchs in this turn have a winner."""
        for match in self.matchs:
            if match.winner_alias is None:
                answer = False
            else:
                answer = True
        return answer

    def is_finished(self):
        """Verify if the tournament is finished."""
        if len(self.matchs) >= 16:
            if self.turn_finished:
                return True

    def get_players_by_score(self):
        """Return the tournament's player sorted by score."""
        return sorted(self.players, key=lambda player: player.score)

    @classmethod
    def get(cls, doc_id):
        """Return the tournament from it's ID from the DB."""
        tournament = cls.table.get(doc_id=doc_id)
        players = Player.get_many_players(tournament["players"])
        tournament["players"] = players

        players = Player.get_many_players(tournament["first_team"])
        tournament["first_team"] = players

        players = Player.get_many_players(tournament["second_team"])
        tournament["second_team"] = players

        matchs = Match.get_many_matchs(tournament["matchs"], tournament["players"])
        tournament["matchs"] = matchs
        return cls.deserialized(tournament)

        # Les get des matchs ne fonctionnent toujours pas, trouver un moyen
        # de get les matchs via une liste
