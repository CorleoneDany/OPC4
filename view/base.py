"""Represents the view."""

import datetime


class Base:
    """Represents the view."""

    def __init__(self):
        pass

    def display_menu(self):
        print("Bienvenue sur Centre Echecs, que voulez-vous faire ?")
        print("Option 1 : Créer un tournoi")
        print("Option 2 : Reprendre un tournoi")
        choice = input("Entrez le numéro de l'option choisie : ")
        return int(choice)

    def ask_tournament_data(self):
        return {
            "name": input("Entrez un nom de tournoi : "),
            "location": input("Entrez la ville où se déroulera le tournoi : "),
            "begin_date": self.ask_beginning_date(),
            "end_date": self.ask_ending_date(),
            "desc": input("Entrez une description pour le tournoi : "),
        }

    def ask_beginning_date(self):
        return self.ask_for_date(
            "Entrez l'année de début sous ce format yyyy : ",
            "Entrez le mois de début sous ce format mm : ",
            "Entrez le jour du début sous ce format dd : ",
        )

    def ask_ending_date(self):
        return self.ask_for_date(
            "Entrez l'année de fin sous ce format yyyy : ",
            "Entrez le mois de fin sous ce format mm : ",
            "Entrez le jour du fin sous ce format dd : ",
        )

    def ask_player_data(self):
        return {
            "first_name": input("Rentrez le prénom du joeur : "),
            "last_name": input("Rentrez le nom de famille du joeur : "),
            "date_of_birth": self.ask_player_date_of_birth(),
            "sex": input("Rentrez le sexe du joueur : "),
            "rank": input("Rentrez le rang du joueur : "),
        }

    def ask_player_date_of_birth(self):
        return self.ask_for_date(
            "Rentrez l'année de naissance du joueur : ",
            "Rentrez le mois de naissance du joueur : ",
            "Rentrez le jour de naissance du joueur : ",
        )

    def ask_for_date(self, year_text, month_text, day_text):
        year = int(input(year_text))
        month = int(input(month_text))
        day = int(input(day_text))
        return datetime.date(year, month, day)
