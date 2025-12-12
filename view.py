from tabulate import tabulate
import datetime
import re
import questionary
import os
from questionary import Choice, Separator


class CancelAction(Exception):
    pass


class MainView:

    def welcome_message(self):
        print("\n" + "*" * 30)
        print("CHESS MANAGER".center(30))
        print("*" * 30 + "\n")

    def finish_message(self):
        print("--- See you soon! ---")

    def error(self, message):
        print(f"\n❌ ERROR : {message}")

    def success(self, message):
        print(f"\n✅ SUCCESS : {message}")

    def clean_console(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def prompt_continue(self):
        input("\nPress Enter to continue...")

    def display_menu(self):
        choice = questionary.select(
            "Main Menu - Select an option:",
            choices=[
                Choice("Player Management", value="1"),
                Choice("Tournament Management", value="2"),
                Choice("Reports", value="3"),
                Separator(),
                Choice("Exit", value="4")
            ]
        ).ask()
        return choice

    def display_success_and_refresh(self, message):
        self.success(message)
        self.prompt_continue()
        self.clean_console()


class PlayersView():

    @staticmethod
    def display_players_sub_menu():
        print("\n--- PLAYERS MENU ---")

        menu_choices = [
            Choice("Create new player", value="1"),
            Choice("Update player info", value="2"),
            Choice("Display player details", value="3"),
            Choice("Display all players", value="4"),
            Choice("Delete player", value="5"),
            Separator(),
            Choice("Return to main menu", value="6")
        ]

        response = questionary.select(
            "What do you want to do?",
            choices=menu_choices
        ).ask()

        return response

    @staticmethod
    def get_new_player_inputs():
        print("\n--- Add a new player ---")

        name = InputView.get_valid_name("Last Name: ")
        surname = InputView.get_valid_name("First Name: ")
        birth_date = InputView.get_valid_date("Birth Date (YYYY-MM-DD): ")
        ine = InputView.get_valid_ine("INE (AB12345): ")

        return {
            "name": name,
            "surname": surname,
            "birth_date": birth_date,
            "ine": ine
        }

    @staticmethod
    def update_player_inputs(player):
        print(f"\n--- Update Player {player.name} {player.surname} ---")

        surname = InputView.get_valid_name(
            f"Last Name ({player.surname}): ",
            default=player.surname
        )

        name = InputView.get_valid_name(
            f"First Name ({player.name}): ",
            default=player.name
        )

        birth_date = InputView.get_valid_date(
            f"Birth Date ({player.birth_date}): ",
            default=player.birth_date
        )

        ine = InputView.get_valid_ine(
            f"INE ({player.ine}): ",
            default=player.ine
        )

        return {
            "name": name,
            "surname": surname,
            "birth_date": birth_date,
            "ine": ine
        }

    @staticmethod
    def select_player(players_list):
        choices = []
        for player in players_list:
            display_name = f"{player.name} {player.surname} ({player.ine}) 👤"
            choices.append(Choice(display_name, value=player))

        choices.append(Separator())
        choices.append(Choice("Return ❌", value="RETURN"))

        return questionary.select(
            "Select a player:",
            choices=choices
        ).ask()

    @staticmethod
    def display_player_info(player):
        print("\n--- PLAYER DETAILS ---")
        data = [
            ["INE", player.ine],
            ["Last Name", player.surname],
            ["First Name", player.name],
            ["Birth Date", player.birth_date]
        ]
        print(tabulate(data, tablefmt="fancy_grid"))

        input("\nPress Enter to return...")

    @staticmethod
    def display_all_players(all_players):
        # Transform player objects in dictonnary
        table_data = [player.to_dict() for player in all_players]
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

        input("Press any button to return")


class TournamentView():
    def __init__(self):
        self.main_view = MainView()

    def display_tournaments_sub_menu(self):
        print("\n--- TOURNAMENTS MENU ---")

        menu_choices = [
            Choice("Create new tournament", value="1"),
            Choice("Start or continue tournament", value="2"),
            Choice("Update tournament info", value="3"),
            Choice("Display tournament details", value="4"),
            Choice("Display all tournaments", value="5"),
            Choice("Delete tournament", value="6"),
            questionary.Separator(),
            Choice("Return to main menu", value="7")
        ]

        response = questionary.select(
            "What do you want to do?",
            choices=menu_choices
        ).ask()

        return response

    def get_tournament_inputs(self):
        print("\n--- Create a new tournament ---")

        name = InputView.get_valid_name("Tournament Name: ")
        city = InputView.get_valid_name("City: ")
        start_date = InputView.get_valid_date("Start Date (YYYY-MM-DD): ")
        end_date = InputView.get_valid_date("End Date (YYYY-MM-DD): ")
        total_round = InputView.get_valid_int("Total round (default = 4): ", 4)
        description = input("Description: ")

        return {
            "name": name,
            "city": city,
            "total_round": total_round,
            "description": description,
            "start_date": start_date,
            "end_date": end_date
        }

    def update_tournament_inputs(self, tournament):
        print(f"\n--- Update Tournament {tournament.name} ---")

        name = InputView.get_valid_name(
            f"Name ({tournament.name}): ",
            default=tournament.name
        )

        city = InputView.get_valid_name(
            f"City ({tournament.city}): ",
            default=tournament.city
        )

        start_date = InputView.get_valid_date(
            f"Start Date ({tournament.start_date}): ",
            default=tournament.start_date
        )

        end_date = InputView.get_valid_date(
            f"End date ({tournament.end_date}): ",
            default=tournament.end_date
        )

        total_round = InputView.get_valid_int(
            f"Total Round ({tournament.total_round}): ",
            default=tournament.total_round
        )

        description = InputView.get_valid_name(
            f"Description ({tournament.description}): ",
            default=tournament.description
        )

        return {
            "name": name,
            "city": city,
            "total_round": total_round,
            "description": description,
            "start_date": start_date,
            "end_date": end_date
        }

    def print_players_table(self, players_list):
        if not players_list:
            print("   🚫 No players registered yet.")
        else:
            table_data = [player.to_dict() for player in players_list]
            print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

    def display_tournament_info(self, tournament, standings=None):
        self.main_view.clean_console()
        print("\n--- TOURNAMENT DETAILS ---")

        general_data = [
            ["Name", tournament.name],
            ["City", tournament.city],
            ["Round", f"{tournament.current_round} / {tournament.total_round}"],
            ["Start Date", tournament.start_date],
            ["End Date", tournament.end_date],
            ["Total Rounds", tournament.total_round],
            ["Finish", "Finished" if tournament.finish else "In Progress"],
            ["Description", tournament.description]
        ]

        print(tabulate(general_data, tablefmt="fancy_grid"))

        # Tabulate for current standings
        if standings:
            print(f"\n📈 CURRENT STANDINGS (Round {tournament.current_round})")
            table_data = []
            for i, player in enumerate(standings):
                full_name = f"{player['surname']} {player['name']}"
                score = player['score']
                rank = i + 1
                table_data.append([rank, full_name, score])

            headers = ["Rank", "Player", "Score"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

        # Tabulate for registred players
        len_players = len(tournament.players)
        print(f"\n -- REGISTERED PLAYERS ({len_players}) ---")

        if len_players == 0:
            print("   No players registered yet.")
        else:
            headers = ["Name", "Surname", "ID"]

            players = [[p.name, p.surname, p.ine] for p in tournament.players]

            print(tabulate(players, headers=headers, tablefmt="fancy_grid"))

        input("\nPress Enter to return...")
        self.main_view.clean_console()

    def display_all_tournament(self, all_tournaments):
        self.main_view.clean_console()
        table_data = [
            {
                "ID": data.id,
                "Name": data.name,
                "City": data.city,
                "Players": len(data.players),
                "Resume": data.description[0:15] if data.description else ""
            } for data in all_tournaments
        ]

        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

        input("Press any button to return")
        self.main_view.clean_console()

    def select_tournament(self, all_tournaments):
        choices = []

        for tournament in all_tournaments:
            round_time = f"{tournament.current_round}/{tournament.total_round}"
            label = f"{tournament.name} ({tournament.city})"

            display_name = f"{label:<35} | Round {round_time} 🏆"

            choices.append(Choice(display_name, value=tournament))

        choices.append(Choice("🔙 Return to Main Menu", value="None"))

        # 4. Prompt the user
        return questionary.select(
            "Select a tournament",
            choices=choices
        ).ask()

    def get_players_to_delete(self, players_list):
        if not players_list:
            print("⚠️ List is empty.")
            return []

        choices = [
            Choice(f"{p.name} {p.surname}", value=p)
            for p in players_list
        ]

        return questionary.checkbox(
            "Select players to remove :",
            choices=choices,
            instruction="(Space to select, Enter to confirm)"
        ).ask()

    def display_manage_menu(self):
        print("\n--- MANAGE TOURNAMENT PLAYERS ---")

        menu_choices = [
            Choice("Add players", value="add"),
            Choice("Remove players", value="remove"),
            Separator(),
            Choice("Confirm & Start", value="confirm"),
            Choice("Return", value="back")
        ]

        response = questionary.select(
            "What do you want to do?",
            choices=menu_choices
        ).ask()

        return response

    def select_players_to_add(self, available_players, total_round):
        if not available_players:
            print("⚠️ No more players available to add.")
            return []

        choices = [
            Choice(f"{p.name} {p.surname} ({p.ine})", value=p)
            for p in available_players
        ]

        min_required = total_round + 1

        return questionary.checkbox(
            f"Select players (Min {min_required} required for {total_round} rounds):",
            choices=choices,
            instruction="(Space to select, Enter to confirm)"
        ).ask()


class RoundView():
    def continue_tournament(current_round):
        choices = [
            "Continue",
            "Stop"
        ]
        answer = questionary.select(
            f"Continue to round_{current_round+1}",
            choices=choices,
        ).ask()

        if answer == choices[0]:
            return "yes"
        else:
            return "2"

    def current_standings(players_list, current_round):
        print(f"\n--- 🥇 Current Standings round {current_round} ---")
        table_data = []

        for i, player in enumerate(players_list):
            full_name = f"{player['surname']} {player['name']}"
            score = player['score']
            rank = i + 1

            table_data.append([rank, full_name, score])

        headers = ["Rank", "Player", "Score"]
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


class MatchView():
    @staticmethod
    def display_match(match_data):
        player1 = match_data[0]
        player2 = match_data[1]

        # Exempt player
        if player2 is None:
            questionary.print(f" {player1['name']} is exempt for this round.")
            questionary.print("   They automatically win 1 point.")
            return 1.0, 0.0

        # Standard Match
        print(f"\n---  MATCH: {player1['name']} vs {player2['name']} ---")

        choices = [
            f"{player1['name']} wins",
            f"{player2['name']} wins",
            "Draw"
        ]

        answer = questionary.select(
            f"What is the result of {player1['name']} VS {player2['name']}?",
            choices=choices,
        ).ask()

        if answer == choices[0]:
            return 1.0, 0.0
        elif answer == choices[1]:
            return 0.0, 1.0
        else:
            return 0.5, 0.5


class ReportView:
    def display_report_sub_menu(self):
        print("\n--- REPORTS MENU ---")

        report_choices = [
            Choice("List all players (alphabetical order)", value="1"),
            Choice("List all tournaments", value="2"),
            Choice("Display tournament details", value="3"),
            Choice("Display players in a specific tournament", value="4"),
            Choice("Display rounds and matches", value="5"),
            questionary.Separator(),
            Choice("Return to main menu", value="6")
        ]

        response = questionary.select(
            "What do you want to view?",
            choices=report_choices
        ).ask()

        return response

    def display_players_in_tournament(self, tournament_name, player_list):
        print(f"Players list for {tournament_name} Tournament ")
        print(tabulate(player_list, headers="keys", tablefmt="fancy_grid"))
        input("Press any button to return")

    def display_round_matches(self, clean_rounds_data):
        header = ["Player 1", "Pts", "", "Pts", "Player 2"]

        for round_info in clean_rounds_data:
            print(f"\n--- {round_info['name']} ---")

            matches = round_info['matches']

            if matches:
                print(tabulate(matches, headers=header, tablefmt="fancy_grid"))
            else:
                print("   No matches.")

        input("\nPress any button to return")


class InputView:

    @staticmethod
    def check_cancel(user_input):
        if user_input.strip().lower() == "return":
            raise CancelAction()

    @staticmethod
    def get_valid_date(prompt, default=None):
        full_prompt = f"{prompt} ('return' to cancel): "

        while True:
            date_str = input(full_prompt).strip()

            InputView.check_cancel(date_str)

            if not date_str:
                if default is not None:
                    return default
                print("Error: This field cannot be empty.")
                continue

            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                return date.isoformat()
            except ValueError:
                print("Error: Invalid date format. Please use YYYY-MM-DD.")

    @staticmethod
    def get_valid_int(prompt, default=None):
        full_prompt = f"{prompt} ('return' to cancel): "

        while True:
            value = input(full_prompt).strip()

            InputView.check_cancel(value)

            if not value:
                return default
            try:
                return int(value)
            except ValueError:
                print("Error: Please enter a valid number.")

    @staticmethod
    def get_valid_name(prompt, default=None):
        full_prompt = f"{prompt} ('return' to cancel): "

        while True:
            user_input = input(full_prompt).strip()

            InputView.check_cancel(user_input)

            if not user_input:
                if default is not None:
                    return default
                print("Error: This field cannot be empty.")
                continue

            if user_input.isalpha():
                return user_input
            else:
                print("Error: Name must contain only letters.")

    @staticmethod
    def get_valid_ine(prompt, default=None):
        full_prompt = f"{prompt} ('return' to cancel): "

        while True:
            raw_input = input(full_prompt).strip()

            InputView.check_cancel(raw_input)

            ine_input = raw_input.upper()

            if not ine_input:
                if default is not None:
                    return default
            elif re.match(r"^[A-Z]{2}[0-9]{5}$", ine_input):
                return ine_input
            else:
                print("Invalid format. Example: AB12345")
