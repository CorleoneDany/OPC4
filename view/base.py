"""Represents the view."""
import os


class MotherView:
    """Represent the mother view."""

    def __init__(self, observer):
        """Init the view with its variables."""
        self.observer = observer

    def wrong_command(self):
        """Print a message if the commanf doesn't exist."""
        print("Mauvaise commande entrée.")

    def execute(self, command):
        """Execute the asked command by the controller."""
        return self.observer.execute(command)

    def set_context(self, key, value):
        """Add information in the controller's context."""
        self.observer.context[key] = value

    def get_context(self, key):
        """Get information from the controller's context."""
        try:
            return self.observer.context[key]
        except KeyError:
            raise KeyError(f"La clé {key} n'existe pas dans le contexte du controlleur")

    def display(self):
        """Print information to the screen."""
        pass

    def ask_for_date(self, year_text, month_text, day_text):
        """Ask a date with the following format day/month/year."""
        year = input(year_text)
        month = input(month_text)
        day = input(day_text)
        return f"{day}/{month}/{year}"

    def ask_for_choice(self):
        """Ask for the user's input."""
        return input()

    def clear(self):
        """Clear the console."""
        os.system("cls" if os.name == "nt" else "clear")


class MainMenu(MotherView):
    """Represent the main menu's view."""

    def __init__(self, observer, tournaments):
        """Init the view with its variables."""
        super().__init__(observer)
        self.tournaments = tournaments

    def display(self):
        """Print the main menu."""
        if self.tournaments:
            print("Bienvenue sur Centre Echecs, que voulez-vous faire ?")
            print("Option 1 : Créer un tournoi")
            print("Option 2 : Reprendre un tournoi")
            self.get_choice()
        else:
            print(
                "Bienvenue sur Centre Echecs\n"
                "Aucun tournoi enregistré en base, envoi vers la création de tournoi"
            )
            self.execute({"name": "create_tournament"})

    def get_choice(self):
        """Get user's input."""
        choice = input("Entrez le numéro de l'option choisie : ")
        if choice == "1":
            command = "create_tournament"
        elif choice == "2":
            command = "retrieve_tournament"
        else:
            command = "wrong_command"
        self.execute({"name": command})


class CreateTournamentView(MotherView):
    """Represent the tournament's creation menu."""

    def display(self):
        """Print the tournament's creation view."""
        print("Entrez les informations du tournoi ci dessous : ")
        tournament_data = self.get_tournament_data()
        self.set_context("tournament_data", tournament_data)

    def get_tournament_data(self):
        """Ask tournament's data."""
        return {
            "name": input("Entrez un nom de tournoi : "),
            "location": input("Entrez la ville où se déroulera le tournoi : "),
            "start_date": self.ask_beginning_date(),
            "ending_date": self.ask_ending_date(),
            "desc": input("Entrez une description pour le tournoi : "),
        }

    def ask_beginning_date(self):
        """Ask tournament's beginning date."""
        return super().ask_for_date(
            "Entrez l'année de début sous ce format yyyy : ",
            "Entrez le mois de début sous ce format mm : ",
            "Entrez le jour du début sous ce format dd : ",
        )

    def ask_ending_date(self):
        """Ask tournament's ending date."""
        return super().ask_for_date(
            "Entrez l'année de fin sous ce format yyyy : ",
            "Entrez le mois de fin sous ce format mm : ",
            "Entrez le jour du fin sous ce format dd : ",
        )

    def display_player_menu(self):
        """Go to player's menu view."""
        self.execute({"name": "player_menu"})


class RetrieveTournamentView(MotherView):
    """Represent the loading view of a tournament."""

    def display(self, tournaments):
        """Display the tournament loading's view."""
        if tournaments:
            print("Voici tous les tournois en base de données :")
            for tournament in tournaments:
                print(f"{tournament.doc_id} : {tournament.name}")
            print("Sélectionnez le tournoi désiré en utilisant son chiffre :")
            self.set_context("chosen_tournament", int(input()))
        else:
            print(
                "Aucun tournoi enregistré en base de données, retour à la "
                "création du tournoi."
            )
            self.execute({"name": "create_tournament"})


class PlayerMenuView(MotherView):
    """Represent the player menu's view."""

    def __init__(self, observer, players):
        """Init the view with its variables."""
        super().__init__(observer)
        self.players = players

    def display(self):
        """Print the player's menu's view."""
        if not self.players:
            print("Aucun joueur selectionné dans le tournoi.")
        else:
            print("Voici les joeurs déjà présents dans le tournoi :")
            for player in self.players:
                print(f"{player.doc_id} : {player.alias}")
        self.print_choices()
        self.get_choice()

    def get_choice(self):
        """Get user's input."""
        choice = input("Entrez le numéro de l'option choisie : ")
        if choice == "1":
            command = "ask_player_creation"
        elif choice == "2":
            command = "select_player"
        else:
            command = "wrong_command"
        self.execute({"name": command})

    def print_choices(self):
        """Print the option that can be chosen by the user."""
        print("Vous êtes dans le menu des joueurs, que voulez-vous faire ?")
        print("Option 1 : Créer un joueur")
        print("Option 2 : Sélectionner un joueur")


class SelectPlayerView(MotherView):
    """Represent the player's selection view."""

    def __init__(self, observer, players, tournament_players):
        """Init the view with its variables."""
        super().__init__(observer)
        self.players = players
        self.tournament_players = tournament_players

    def display(self):
        """Print the players's selection's menu."""
        print("Ci-dessous la liste des joeurs déjà enregistrés en base :")
        while len(self.tournament_players) < 8:
            for index in self.players:
                # si un joueur est déjà selectionné dans le tournoi le préciser
                print(f"{index.doc_id} : {index.alias}")
            player = self.get_choice()
            self.set_context("chosen_player", player)
            self.execute({"name": "add_player"})
            choice = input("Sélectionner un autre joueur ? Y/N : ")
            if choice == "N":
                self.execute({"name": "player_menu"})

        print("8 joueurs ont été séléctionnés, les matchs vont être créés.")
        self.execute({"name": "create_matchs"})

    def get_choice(self):
        """Get the user's choice."""
        choice = None
        while choice is None:
            try:
                choice = int(input("Entrez le numéro du joueur choisi : "))
            except ValueError:
                pass
        return choice


class CreatePlayerView(MotherView):
    """Represent the player's creation view."""

    def display(self):
        """Print the player's creation's menu."""
        print("Entrez l'information du joueur ci dessous : ")
        player = self.ask_player_data()
        self.set_context("player_to_create", player)
        if self.get_choice() == "N":
            self.execute({"name": "player_menu"})

    def ask_player_data(self):
        """Ask for player's data."""
        return {
            "first_name": input("Entrez le prénom du joueur : "),
            "last_name": input("Entrez le nom de famille du joueur : "),
            "date_of_birth": self.ask_player_date_of_birth(),
            "sex": input("Entrez le sexe du joueur (h/f) : "),
            "rank": input("Entrez le rang du joueur : "),
        }

    def ask_player_date_of_birth(self):
        """Ask for player's date of birth."""
        return super().ask_for_date(
            "Entrez l'année de naissance du joueur : ",
            "Entrez le mois de naissance du joueur : ",
            "Entrez le jour de naissance du joueur : ",
        )

    def get_choice(self):
        """Ask if the user want to create another player."""
        return input("Créer un autre joueur ? Y/N : ")

    def show_created_player(self, player):
        """Print the created player."""
        print(f"Joueur {player.alias} créé.")


class CreateMatchView(MotherView):
    """Represent the match's creation's view."""

    def __init__(self, observer, matches):
        """Init the view with its variables."""
        super().__init__(observer)
        self.matches = matches

    def display(self):
        """Print the last created matches."""
        for match in self.matches:
            if match.winner_alias is None:
                print(
                    f"Le match n°{match.doc_id} opposant {match.player_1.alias}"
                    f" et {match.player_2.alias} à été créé."
                )
        self.execute({"name": "choose_match"})


class ChooseMatchView(MotherView):
    """Represent the menu to choose a match."""

    def __init__(self, observer, matches):
        """Init the view with its variables."""
        super().__init__(observer)
        self.matches = matches

    def display(self):
        """Print all the matches that can be modified."""
        print("Voici les matchs qu'il vous est possible de sélectionner : ")
        for match in self.matches:
            if match.winner_alias is None:
                print(f"Match n°{match.doc_id} : {match.alias}")
        print("Choisissez le chiffre du match à modifier : ")
        self.set_context("chosen_match", self.get_choice())
        self.execute({"name": "modify_match"})

    def get_choice(self):
        """Get the user's choice."""
        return int(input())


class ModifyMatchView(MotherView):
    """Represent the menu to modify a match."""

    def __init__(self, observer, match):
        """Init the view with its variables."""
        super().__init__(observer)
        self.match = match

    def display(self):
        """Print a menu to modify a selected match."""
        print(
            f"Vous avez sélectionné le match {self.match.alias}, nous vous invitons à "
            f"renseigner le vainqueur de ce dernier, Joueur 1 "
            f"({self.match.player_1.alias}) ou Joueur 2 ({self.match.player_2.alias})"
            "par son chiffre, dans le cas d'un match nul laisser la valeur à vide : \n"
        )
        self.set_context("chosen_winner", self.get_choice())

    def get_choice(self):
        """Get the user's choice."""
        return int(input())

    def change_match(self):
        """Change the selected match."""
        self.execute({"name": "choose_match"})


class EndTournamentView(MotherView):
    """Represent the tournament's ending view."""

    def __init__(self, observer, players):
        """Init the view with its variables."""
        super().__init__(observer)
        self.players = players

    def display(self):
        """Print the last view of the finished tournament with the results."""
        print("Le tournoi est terminé, voici les résultats des joueurs : ")
        for index, player in enumerate(self.players):
            print(f"{index} : {player.alias} avec {player.score}")
