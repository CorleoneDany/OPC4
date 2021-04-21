"""Represents the view."""

import datetime


class MotherView:
    def __init__(self, observer):
        self.observer = observer

    def wrong_command(self):
        print("Mauvaise commande entrée.")

    def notify(self, command):
        self.observer.update(command)

    def display(self):
        pass

    def ask_for_date(self, year_text, month_text, day_text):
        year = int(input(year_text))
        month = int(input(month_text))
        day = int(input(day_text))
        return datetime.date(year, month, day)


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
        self.notify(command)


class CreateTournamentView(MotherView):
    def display(self):
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


class CreatePlayerView(MotherView):
    def display(self):
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


class CreatedPlayerView(MotherView):
    def __init__(self, player_list):
        self.player_list = player_list

    def display(self):
        print(f"Joueur {self.player_list[-1].player_alias} créé.")


class CreateMatchView(MotherView):
    def __init__(self, match):
        self.match = match

    def display(self, match):
        print(
            f"Le match n°{self.match.match_id} opposant {match.player_1.alias}"
            f" et {match.player_2.alias} vient d'être créé."
        )


class ShowMatches(MotherView):
    def __init__(self, matches):
        self.matches = matches

    def display(self):
        for match in self.matches:
            print(
                f"Match n°{match.match_id} : {match.player_1_alias}"
                f" contre {match.player_2_alias}."
            )


class ChooseMatch(MotherView):
    def display(self):
        return int(
            input(
                "Choisissez le chiffre du match à modifier, "
                "si vous voulez passer au prochain matchup n'entrez aucune valeur : "
            )
        )


class InputMatchWinner(MotherView):
    def __init__(self, match):
        self.match = match

    def display(self):
        choice = int(
            input(
                f"Rentrez le gagnant, Joueur 1 ({self.match.player_1.alias}) ou Joueur 2"
                f" ({self.match.player_2.alias}) par son chiffre, dans le cas d'un match"
                " nul laisser la valeur à vide : "
            )
        )
        return choice
