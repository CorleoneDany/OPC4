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
        # demander la création ou le chargement des joueurs via la liste en bdd
        print("Entrez les informations du tournoi ci dessous : ")
        tournament_data = self.get_tournament_data()
        self.set_context("tournament_data", tournament_data)
        self.update({"name": "player_menu"})

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
    def display(self, tournament_player_list):
        if tournament_player_list is None:
            print("Aucun joueur selectionné dans le tournoi.")
        else:
            print("Voici les joeurs déjà présents dans le tournoi :")
            for player in tournament_player_list:
                print(f"{player.id} : {player.alias}")
        self.print_choices()
        self.get_choice()

    def get_choice(self):
        choice = input("Entrez le numéro de l'option choisie : ")
        if choice == "1":
            command = "ask_player_creation"
        elif choice == "2":
            command = "select_player"
        else:
            command = "wrong_command"
        self.update({"name": command})

    def print_choices(self):
        print("Vous êtes dans le menu des joueurs, que voulez-vous faire ?")
        print("Option 1 : Créer un joueur")
        print("Option 2 : Sélectionner un joueur")


class SelectPlayerView(MotherView):
    def display(self, players):
        for index in players:
            print("Ci-dessous la liste des joeurs déjà enregistrés en base :")
            print(f"{index.doc_id} : {index.alias()}")
        self.get_choice()

    def get_choice(self):
        choice = input("Entrez le numéro du joueur choisi : ")
        return choice


class CreatePlayersView(MotherView):
    def display(self, number_of_players=8):
        for index in range(number_of_players):
            print("Entrez l'information du joueur ci dessous : ")
            player = self.ask_player_data()
            self.set_context(f"player{index}", player)
        self.update("create_players")
        self.update("create_matchs")

    def ask_player_data(self):
        return {
            "first_name": input("Entrez le prénom du joueur : "),
            "last_name": input("Entrez le nom de famille du joueur : "),
            "date_of_birth": self.ask_player_date_of_birth(),
            "sex": input("Entrez le sexe du joueur (h/f) : "),
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
    def __init__(self, observer, matches):
        super().__init__(observer)
        self.matches = matches

    def display(self):
        print("Voici les matchs qu'il vous est possible de sélectionner : ")
        for id, match in enumerate(self.matches):
            print(f"Match n°{id} : {match.alias}")
        print(
            "Choisissez le chiffre du match à modifier, "
            "si vous voulez passer au prochain matchup n'entrez aucune valeur : "
        )
        choice = self.get_choice()
        self.set_context("chosen_match", self.matches[choice])
        self.update("modify_match")

    def get_choice(self):
        return int(input())


class ModifyMatchView(MotherView):
    def __init__(self, observer, match):
        super().__init__(observer)
        self.match = match

    def display(self):
        print(
            f"Vous avez sélectionné le match {self.match.alias}, nous vous invitons à "
            f"renseigner le vainqueur de ce dernier, Joueur 1 "
            f"({self.match.player_1.alias}) ou Joueur 2 ({self.match.player_2.alias})"
            "par son chiffre, dans le cas d'un match nul laisser la valeur à vide : \n"
        )
        self.set_context("chosen_winner", self.get_choice())

    def get_choice(self):
        return int(input())
