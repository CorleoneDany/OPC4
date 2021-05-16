"""Represents the view."""

import datetime


class MotherView:
    def __init__(self, observer):
        self.observer = observer

    def wrong_command(self):
        print("Mauvaise commande entrée.")

    def update(self, command):
        return self.observer.execute(command)

    def set_context(self, key, value):
        self.observer.context[key] = value

    def get_context(self, key):
        try:
            return self.observer.context[key]
        except KeyError:
            raise KeyError(f"La clé {key} n'existe pas dans le contexte du controlleur")

    def display(self):
        pass

    def ask_for_date(self, year_text, month_text, day_text):
        year = int(input(year_text))
        month = int(input(month_text))
        day = int(input(day_text))
        return datetime.date(year, month, day)

    def ask_for_choice(self):
        return input()


class MainMenu(MotherView):
    def display(self):
        print("Bienvenue sur Centre Echecs, que voulez-vous faire ?")
        print("Option 1 : Créer un tournoi")
        print("Option 2 : Reprendre un tournoi")
        self.get_choice()

    def get_choice(self):
        choice = input("Entrez le numéro de l'option choisie : ")
        if choice == "1":
            command = "create_tournament"
        elif choice == "2":
            command = "retrieve_tournament"
        else:
            command = "wrong_command"
        self.update({"name": command})


class CreateTournamentView(MotherView):
    def display(self):
        print("Entrez les informations du tournoi ci dessous : ")
        tournament_data = self.get_tournament_data()
        self.set_context("tournament_data", tournament_data)
        self.update({"name": "ask_player_creation"})

    def get_tournament_data(self):
        return {
            "name": input("Entrez un nom de tournoi : "),
            "location": input("Entrez la ville où se déroulera le tournoi : "),
            "start_date": self.ask_beginning_date(),
            "ending_date": self.ask_ending_date(),
            "desc": input("Entrez une description pour le tournoi : "),
        }

    def ask_beginning_date(self):
        return super().ask_for_date(
            "Entrez l'année de début sous ce format yyyy : ",
            "Entrez le mois de début sous ce format mm : ",
            "Entrez le jour du début sous ce format dd : ",
        )

    def ask_ending_date(self):
        return super().ask_for_date(
            "Entrez l'année de fin sous ce format yyyy : ",
            "Entrez le mois de fin sous ce format mm : ",
            "Entrez le jour du fin sous ce format dd : ",
        )


class RetrieveTournamentView(MotherView):
    def display(self):
        print("Option en cours de développement.")


class PlayerMenuView(MotherView):
    def display(self):
        print("Vous êtes sur la page des joueurs, que voulez-vous faire ?")
        print("Option 1 : Créer un joueur")
        print("Option 2 : Voir la liste des joueurs")
        self.get_choice()

    def get_choice(self):
        choice = input("Entrez le numéro de l'option choisie : ")
        if choice == "1":
            command = "ask_player_creation"
        elif choice == "2":
            command = "display_players"
        else:
            command = "wrong_command"
        self.update({"name": command})


class CreatePlayersView(MotherView):
    def display(self, number_of_players=8):
        for players_needed in range(number_of_players):
            print("Entrez l'information du joueur ci dessous : ")
            player = self.ask_player_data()
            self.set_context(f"player{players_needed}", player)
            self.update("create_player")
            self.show_created_player(player)
        self.update("create_matchs")

    def ask_player_data(self):
        return {
            "first_name": input("Entrez le prénom du joueur : "),
            "last_name": input("Entrez le nom de famille du joueur : "),
            "date_of_birth": self.ask_player_date_of_birth(),
            "sex": input("Entrez le sexe du joueur : "),
            "rank": input("Entrez le rang du joueur : "),
        }

    def ask_player_date_of_birth(self):
        return super().ask_for_date(
            "Entrez l'année de naissance du joueur : ",
            "Entrez le mois de naissance du joueur : ",
            "Entrez le jour de naissance du joueur : ",
        )

    def show_created_player(self, player):
        print(f"Joueur {player.alias} créé.")


class CreateMatchView(MotherView):
    def __init__(self, observer, matches):
        super().__init__(observer)
        self.matches = matches

    def display(self):
        for match in self.matches:
            print(
                f"Le match n°{self.match.match_id} opposant {match.player_1.alias}"
                f" et {match.player_2.alias} à été créé."
            )


class ShowMatches(MotherView):
    def __init__(self, observer, matches):
        super().__init__(observer)
        self.matches = matches

    def display(self):
        for match in self.matches:
            print(
                f"Match n°{match.match_id} : {match.player_1_alias}"
                f" contre {match.player_2_alias}."
            )


class ChooseMatchView(MotherView):
    def display(self):
        print(
            "Choisissez le chiffre du match à modifier, "
            "si vous voulez passer au prochain matchup n'entrez aucune valeur : "
        )
        self.get_choice()


class InputMatchWinner(MotherView):
    def __init__(self, observer, match):
        super().__init__(observer)
        self.match = match

    def display(self):
        print(
            f"Rentrez le gagnant, Joueur 1 ({self.match.player_1.alias}) ou Joueur 2"
            f" ({self.match.player_2.alias}) par son chiffre, dans le cas d'un match"
            " nul laisser la valeur à vide : "
        )
        self.get_choice()
