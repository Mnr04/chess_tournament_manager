from tabulate import tabulate
import datetime
import re
import questionary
from questionary import Choice, Separator
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()


class MainView:
    @staticmethod
    def welcome_message():
        console.print(Panel.fit("♟️  Chess Manager",  style="bold blue"))

    @staticmethod
    def finish_message():
        print("--- See you next time ---")

    @staticmethod
    def error(message):
        console.print(f"❌ [bold red]{message}[/bold red]")

    @staticmethod
    def success(message):

        console.print(f"✅ [bold green]{message}[/bold green]")

    @staticmethod
    def clean_console():
        console.clear()

    @staticmethod
    def display_menu():
        choice = questionary.select(
            "Select an option:",
            choices=[
                Choice("Players 👤", value="1"),
                Choice("Tournaments 🏆", value="2"),
                Choice("Reports 📖", value="3"),
                questionary.Separator(),
                Choice("Quit ❌", value="4")
            ]
        ).ask()
        return choice


class PlayersView():

    @staticmethod
    def display_players_sub_menu():
        response = questionary.select(
            "Players Menu - Select an option:",
            choices=[
                Choice("Create Player 👤", value="1"),
                Choice("Update Player 🛠️", value="2"),
                Choice("View Player 👁️", value="3"),
                Choice("View All Players 📋", value="4"),
                Choice("Remove Player 🗑️", value="5"),
                questionary.Separator(),
                Choice("Return 🔙", value="6")
            ]
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
        content = Text()
        content.append(f"🆔 ID: {player.id}\n")
        content.append(f"👤 Name: {player.surname.upper()} {player.name}\n")
        content.append(f"🎂 Birth Date: {player.birth_date}\n")
        content.append(f"📜 INE: {player.ine}")

        console.print(Panel(
            content,
            title="Player Info",
            expand=False,
            border_style="blue"
        ))

        questionary.press_any_key_to_continue().ask()

    @staticmethod
    def display_all_players(all_players):
        # Transform player objects in dictonnary
        table_data = [player.to_dict() for player in all_players]
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

        input("Press any button to return")


class TournamentView():

    @staticmethod
    def display_tournaments_sub_menu():
        response = questionary.select(
            "Tournaments Menu - Select an option:",
            choices=[
                Choice("Create Tournament ➕", value="1"),
                Choice("Start Tournament 🚀", value="2"),
                Choice("Update Tournament 🛠️", value="3"),
                Choice("View Tournament Detail 👁️", value="4"),
                Choice("View All Tournaments 📋", value="5"),
                Choice("Remove Tournament 🗑️", value="6"),
                questionary.Separator(),
                Choice("Return 🔙", value="7")
            ]
        ).ask()

        return response

    @staticmethod
    def get_tournament_inputs():
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

    @staticmethod
    def update_tournament_inputs(tournament):
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

    @staticmethod
    def print_players_table(players_list):
        if not players_list:
            print("   🚫 No players registered yet.")
        else:
            table_data = [player.to_dict() for player in players_list]
            print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))

    @staticmethod
    def display_tournament_info(tournament):
        MainView.clean_console()
        print("\n--- TOURNAMENT DETAILS ---")

        general_data = [
            ["Name", tournament.name],
            ["City", tournament.city],
            ["Start Date", tournament.start_date],
            ["End Date", tournament.end_date],
            ["Total Rounds", tournament.total_round],
            ["Finish", "Finished" if tournament.finish else "In Progress"],
            ["Description", tournament.description]
        ]

        print(tabulate(general_data, tablefmt="fancy_grid"))

        len_players = len(tournament.players)
        print(f"\n -- REGISTERED PLAYERS ({len_players}) ---")

        if len_players == 0:
            print("   No players registered yet.")
        else:
            headers = ["Name", "Surname", "ID"]

            players = [[p.name, p.surname, p.id] for p in tournament.players]

            print(tabulate(players, headers=headers, tablefmt="fancy_grid"))

        input("\nPress Enter to return...")
        MainView.clean_console()

    @staticmethod
    def display_all_tournament(all_tournaments):
        MainView.clean_console()
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
        MainView.clean_console()

    @staticmethod
    def select_tournament(all_tournaments):
        choices = []

        for tournament in all_tournaments:
            round_time = f"{tournament.actual_round}/{tournament.total_round}"
            label = f"{tournament.name} ({tournament.city})"

            display_name = f"{label:<35} | Round {round_time} 🏆"

            choices.append(Choice(display_name, value=tournament))

        choices.append(Choice("🔙 Return to Main Menu", value="None"))

        # 4. Prompt the user
        return questionary.select(
            "Select a tournament",
            choices=choices
        ).ask()

    @staticmethod
    def get_players_to_delete(players_list):
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

    def display_manage_menu():
        return questionary.select(
            "Manage Players:",
            choices=[
                Choice("➕ Add Players", value="add"),
                Choice("➖ Remove Players", value="remove"),
                Choice("✅ Confirm & Start", value="confirm"),
                Choice("🔙 Back", value="back")
            ],
        ).ask()

    def select_players_to_add(available_players):
        if not available_players:
            print("⚠️ No more players available to add.")
            return []

        choices = [
            Choice(f"{p.name} {p.surname} ({p.id})", value=p)
            for p in available_players
        ]

        return questionary.checkbox(
            "Select players to add to the tournament:",
            choices=choices,
            instruction="(Space to select, Enter to confirm)"
        ).ask()


class RoundView():
    def display_continue_tournament(actual_round):
        choices = [
            "Continue",
            "Stop"
        ]
        answer = questionary.select(
            f"Continue to round_{actual_round+1}",
            choices=choices,
        ).ask()

        if answer == choices[0]:
            return "yes"
        else:
            return "2"


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
        print(f"\n--- ⚔️  MATCH: {player1['name']} vs {player2['name']} ---")

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


class RepportView:
    @staticmethod
    def display_repport_sub_menu():
        response = questionary.select(
            "Reports Menu - Select an option:",
            choices=[
                Choice("List of all players 👥", value="1"),
                Choice("List of all tournaments 🏆", value="2"),
                Choice("Tournament Details  📅", value="3"),
                Choice("Tournament Players  ♟️", value="4"),
                Choice("Tournament Rounds & Matches ⚔️", value="5"),
                questionary.Separator(),
                Choice("Return to Main Menu 🔙", value="6")
            ]
        ).ask()

        return response

    def display_players_in_tournament(tournament_name, player_list):
        print(f"Players list for {tournament_name} Tournament 🏆")
        print(tabulate(player_list, headers="keys", tablefmt="fancy_grid"))

        input("Press any button to return")

    @staticmethod
    def display_round_matches(clean_rounds_data):
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
    def get_valid_date(prompt, default=None):
        while True:
            date_str = input(prompt).strip()

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
        while True:
            value = input(prompt)
            if not value:
                return default
            try:
                return int(value)
            except ValueError:
                print("Error: Please enter a valid number.")

    @staticmethod
    def get_valid_name(prompt, default=None):
        while True:
            user_input = input(prompt).strip()
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
        while True:
            ine_input = input(prompt).strip().upper()
            if not ine_input:
                if default is not None:
                    return default
            elif re.match(r"^[A-Z]{2}[0-9]{5}$", ine_input):
                return ine_input
            else:
                print("Invalid Format exemple : AB12345 ")
