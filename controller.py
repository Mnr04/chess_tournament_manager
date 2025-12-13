from view import (
    MainView, PlayersView, TournamentView, MatchView, RoundView,
    ReportView, CancelAction
)
from models import Player, Tournament, Round, Match
import datetime
import random


class MainController:
    def __init__(self):
        self.view = MainView()
        self.players_controller = PlayersController()
        self.tournaments_controller = TournamentController()
        self.report_controller = ReportController()

    def run(self):
        while True:
            self.view.welcome_message()
            response = self.view.display_menu()

            menu_choice = {
                "1": self.players_controller.players_sub_menu,
                "2": self.tournaments_controller.tournament_sub_menu,
                "3": self.report_controller.report_sub_menu,
            }

            if response in menu_choice:
                user_choice = menu_choice[response]
                user_choice()

            elif response == "4":
                self.view.finish_message()
                break

            else:
                self.view.error("Error : Wrong input")


class PlayersController():
    def __init__(self):
        self.players_view = PlayersView()
        self.main_view = MainView()

    def players_sub_menu(self):
        while True:
            self.main_view.clean_console()
            response = self.players_view.display_players_sub_menu()

            menu_choice = {
                "1": self.create_player,
                "2": self.update_player,
                "3": self.view_player,
                "4": self.view_all_player,
                "5": self.remove_player
            }

            if response in menu_choice:
                user_choice = menu_choice[response]
                user_choice()

            elif response == "6":
                break

            else:
                self.main_view.error("Error : Wrong input")

    def create_player(self):
        try:
            while True:
                player_data = self.players_view.get_new_player_inputs()

                ine_input = player_data["ine"]
                player_exist = Player.get_player_by_ine(ine_input)

                if player_exist:
                    self.main_view.error(f"🚫 Duplicate INE {ine_input} found.")
                    self.main_view.error("Please re-start.")
                    continue
                else:
                    break

            new_player = Player(**player_data)
            new_player.save_new_player()

            self.main_view.display_success_and_refresh(
                "✅ Player saved successfully!"
                )

        except CancelAction:
            self.main_view.display_success_and_refresh(
                "\n🔙 Creation cancelled. Returning to menu..."
                )
            return

        except Exception as e:
            self.main_view.error(f"Error while saving: {e}")

    def select_player(self):
        all_players = Player.get_all_players()

        if not all_players:
            self.main_view.error("❌ No players registered.")
            return None

        return PlayersView.select_player(all_players)

    def update_player(self):
        t_player = self.select_player()

        if not t_player or t_player == "RETURN":
            self.main_view.prompt_continue()
            return
        try:
            while True:
                updated_data = self.players_view.update_player_inputs(t_player)

                new_ine = updated_data["ine"]

                existing_player = Player.get_player_by_ine(new_ine)

                if existing_player and existing_player.id != t_player.id:
                    self.main_view.error("Error: INE  is already taken.")
                    self.main_view.error("Restarting update...")
                    continue

                else:
                    break

            Player.update_players(t_player.id, updated_data)
            self.main_view.display_success_and_refresh(
                "Player updated successfully!"
                )

        except CancelAction:
            self.main_view.display_success_and_refresh(
                "\n🔙 Update cancelled. Returning to menu..."
                )
            return

        except Exception as e:
            self.main_view.error(f"Error while updating: {e}")

    def view_player(self):
        target_player = self.select_player()
        self.main_view.clean_console()

        if target_player == "RETURN":
            self.main_view.error("🔙 Back to menu")
            return

        if not target_player:
            self.display_success_and_refresh("No players to display")
            return

        player_info = Player.get_players_by_id(target_player.id)
        if not player_info:
            return

        self.players_view.display_player_info(player_info)

    def view_all_player(self):
        # Get all players from Model --> Database
        p_sorted = Player.get_all_players()
        # Sort player by surname
        p_sorted = sorted(p_sorted, key=lambda x: x.surname, reverse=False)
        # Display all players infos
        if p_sorted == []:
            self.main_view.error("No players to display")
            self.main_view.prompt_continue()
            return
        self.players_view.display_all_players(p_sorted)

    def remove_player(self):
        target_player = self.select_player()

        if target_player == "RETURN":
            self.main_view.error("🔙 Back to menu")
            return

        if not target_player:
            self.main_view.prompt_continue()
            return

        player_info = Player.get_players_by_id(target_player.id)

        if not player_info:
            self.main_view.error("Player not found!")
            return
        else:
            Player.delete_player(player_info.id)
            self.main_view.display_success_and_refresh(
                "Player deleted successfully!"
                )


class TournamentController():
    def __init__(self):
        self.main_view = MainView()
        self.view = TournamentView()

    def tournament_sub_menu(self):
        self.main_view.clean_console()
        while True:
            response = self.view.display_tournaments_sub_menu()
            menu_choice = {
                "1": self.create_tournament,
                "2": self.launch_tournament,
                "3": self.update_tournament,
                "4": self.view_tournament,
                "5": self.view_all_tournaments,
                "6": self.remove_tournament,
            }

            if response in menu_choice:
                user_choice = menu_choice[response]
                user_choice()

            elif response == "7":
                break

            else:
                self.main_view.error("Error : Wrong input")

    def create_tournament(self):
        all_players = Player.get_all_players()
        if len(all_players) < 2:
            self.main_view.error("Register at least 2 players first.")
            self.main_view.prompt_continue()
            self.main_view.clean_console()
            return
        try:
            tournament_data = self.view.get_tournament_inputs()

            if tournament_data["start_date"] > tournament_data["end_date"]:
                self.main_view.error(
                    "Error: Start date cannot be after End date."
                    )
                return

            s_players = []
            while True:

                s_players = self.view.select_players_to_add(
                    all_players, tournament_data["total_round"]
                    )

                if not s_players:
                    choice = input(
                        "No players selected. Cancel creation? (y/n): "
                        )
                    if choice.lower() == 'y':
                        return
                    continue

                # ratio round / players (nb_players = nb_rounds + 1)
                nb_rounds = tournament_data["total_round"]
                nb_players = len(s_players)

                if nb_players < nb_rounds + 1:
                    self.main_view.error(f"min {nb_rounds + 1}.")
                    self.main_view.error("👉 Add more players.")
                    self.main_view.prompt_continue()
                    continue

                break

            tournament_data["players"] = s_players

            new_tournament = Tournament(**tournament_data)
            new_tournament.save_tournament()
            self.main_view.display_success_and_refresh(
                f"Tournament '{tournament_data['name']}' created"
                )

        except CancelAction:
            self.main_view.display_success_and_refresh(
                "\n🔙 Creation cancelled. Returning to menu..."
                )
            return

        except Exception as e:
            self.main_view.error(f"Error while saving: {e}")

    def update_tournament(self):
        tournament = self.select_tournament(
            filter_condition=lambda t: t.current_round == 0
            )

        if not tournament or tournament == "None":
            return

        try:

            update_info = self.view.update_tournament_inputs(tournament)
            if update_info["start_date"] > update_info["end_date"]:
                self.main_view.error("Invalid date")
                return

            players = self.manage_tournament_players(
                tournament.players, tournament.total_round
                )

            new_total_rounds = update_info["total_round"]
            new_total_players = len(players)

            if new_total_players < new_total_rounds + 1:
                self.main_view.clean_console()
                self.main_view.error("🚫 UPDATE ERROR")
                self.main_view.error("Min {new_total_rounds + 1} players")
                self.main_view.error("Restart")
                self.main_view.prompt_continue()
                return

            Tournament.update_tournament(tournament.id, update_info, players)
            self.main_view.display_success_and_refresh(
                "Tournament updated successfully!"
                )

        except CancelAction:
            self.main_view.display_success_and_refresh(
                "\n🔙 Update cancelled. Returning to menu..."
                )
            return

        except Exception as e:
            self.main_view.error(f"Error: {e}")

    def view_tournament(self):

        target_tournament = self.select_tournament()
        if not target_tournament:
            self.main_view.error("No Tournament!")
            return
        elif target_tournament == "None":
            return

        # Try to get actual standings
        try:
            current_standings = Tournament.current_standings(
                target_tournament.id
                )

        except FileNotFoundError:
            current_standings = []

        # Sorted player list
        player_list = sorted(
            target_tournament.players, key=lambda x: x.surname, reverse=False
            )

        target_tournament.players = player_list

        self.main_view.clean_console()
        self.view.display_tournament_info(target_tournament, current_standings)
        return target_tournament

    def view_all_tournaments(self):
        all_tournaments = Tournament.get_all_tournaments()
        self.main_view.clean_console()
        self.view.display_all_tournament(all_tournaments)

    def remove_tournament(self):
        tournament_target = self.select_tournament()
        if not tournament_target:
            self.main_view.error("Tournament not find")

        self.main_view.display_success_and_refresh(
            f"{tournament_target.name} successfully deleted"
            )

        Tournament.delete_tournament(tournament_target.id)

    def get_players_list(self, number_of_players):
        all_players = Player.get_all_players()
        selected_players = []

        print(f"\n--- Select {number_of_players} players ---")

        while len(selected_players) < number_of_players:
            candidates = [p for p in all_players if p not in selected_players]

            if not candidates:
                self.main_view.error("Not enough players in database!")
                break

            new_player = PlayersView.select_player(candidates)

            if new_player == "RETURN" or new_player is None:
                break

            selected_players.append(new_player)
            self.main_view.success(f"{new_player.name} added")

        return selected_players

    def select_tournament(self, filter_condition=None):
        # Get all tournament
        all_tournaments = Tournament.get_all_tournaments()

        if filter_condition:
            tournaments_to_display = [
                t for t in all_tournaments if filter_condition(t)]
        else:
            tournaments_to_display = all_tournaments

        if len(tournaments_to_display) == 0:
            self.main_view.display_success_and_refresh(
                "No tournament to display."
                )

            return None

        return self.view.select_tournament(tournaments_to_display)

    def manage_tournament_players(self, actual_players, total_round):
        self.main_view.clean_console()

        all_players = Player.get_all_players()

        while True:
            print(f"\n--- 👥 CURRENT PLAYERS ({len(actual_players)}) ---")
            self.view.print_players_table(actual_players)
            action = self.view.display_manage_menu()

            if action == "add":

                current_ids = {p.id for p in actual_players}
                candidates = [
                    p for p in all_players if p.id not in current_ids
                    ]

                new_players = self.view.select_players_to_add(
                    candidates, total_round
                    )

                if new_players:
                    actual_players.extend(new_players)
                    self.main_view.success(
                        f"{len(new_players)} players added!"
                        )

                self.main_view.clean_console()

            elif action == "remove":
                actual_players = self.remove_tournament_player(actual_players)
                self.main_view.clean_console()

            elif action == "confirm":
                if len(actual_players) < total_round + 1:
                    self.main_view.error(f"Min : {total_round + 1} players.")
                    continue
                return actual_players

            elif action == "back":
                return actual_players

    def remove_tournament_player(self, players_data):
        players_to_remove = self.view.get_players_to_delete(players_data)

        if not players_to_remove:
            self.main_view.error("❌ No changes made.")
            return players_data

        for player in players_to_remove:
            if player in players_data:
                players_data.remove(player)
                self.main_view.success(f"Player {player.surname} deleted.")

        return players_data

    def launch_tournament(self):
        """
        Runs the tournament loop.
        Manages rounds, displays standings,
        and checks if the tournament is finished.

        """
        self.main_view.clean_console()
        # Select Tournament objects
        tournament = self.select_tournament(
            filter_condition=lambda x: x.finish is False
            )
        # choice return value="None"
        if not tournament or tournament == "None":
            return

        Tournament.initialize_standings(tournament.id)

        while tournament.current_round < tournament.total_round:

            RoundController.run_round(tournament)

            if tournament.current_round == tournament.total_round:
                break

            # Display current standings
            current_standings = Tournament.current_standings(tournament.id)
            RoundView.current_standings(
                current_standings, tournament.current_round
                )

            # Option to continue / stop tournament
            response = RoundView.continue_tournament(tournament.current_round)
            if response == '2':
                self.main_view.clean_console()
                break

        if tournament.current_round == tournament.total_round:
            Tournament.finish_tournament(tournament.id)
            self.main_view.success('Tournament Finished')

    @staticmethod
    def has_already_played(p1_id, p2_id, match_history):
        if [p1_id, p2_id] in match_history:
            return True

        if [p2_id, p1_id] in match_history:
            return True

        return False


class RoundController:

    @classmethod
    def run_round(cls, tournament):
        """
        Launch a single round: generates pairs, saves the round,
        and processes match results.

        Args:
            tournament: The current tournament instance.
        """
        # Create round count + Round Object
        tournament.current_round += 1
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        new_round = Round(f"Round {tournament.current_round}", start_time)

        # Get Player + match history
        players_list = Round.get_round_players_list(tournament.id)

        random.shuffle(players_list)
        s_players_list = sorted(
            players_list, key=lambda p: p.score, reverse=True
            )
        match_history = Round.get_all_pairs_played(tournament.id)

        # Generate Pairs
        new_round.matches = cls.generate_pairs(s_players_list, match_history)

        # Create round file
        new_round.save_round(tournament.id)

        # Process Match and verify if finish
        round_finished = MatchController.process_match(
            new_round.matches, tournament.id
            )

        if not round_finished:
            view = MainView()
            view.error("Round not finished")
            tournament.current_round -= 1
            return

        new_round.end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        new_round.save_round(tournament.id)

        # Save the Round
        tournament.save_tournament()

    @staticmethod
    def generate_pairs(players_list_sorted, match_history):
        """
        Generates match pairs.
        Pairs players by score while avoiding previous opponents.

        Args:
            players_list_sorted (list): Players sorted by score.
            match_history (list): List of pairs already played.

        Returns:
            list: A list of Match objects for the new round.
        """
        match_list = []

        if len(players_list_sorted) % 2 != 0:
            exit_player = players_list_sorted.pop()
            match_exit = Match(
                player1=exit_player, player2=None, score1=1, score2=0)
            match_list.append(match_exit)

        while len(players_list_sorted) > 0:
            p1 = players_list_sorted.pop(0)
            match_found = False

            for i in range(len(players_list_sorted)):
                possible_opponent = players_list_sorted[i]

                if not TournamentController.has_already_played(
                    p1.id, possible_opponent.id, match_history
                ):
                    p2 = players_list_sorted.pop(i)

                    new_match = Match(player1=p1, player2=p2)
                    match_list.append(new_match)
                    match_found = True
                    break

            if not match_found:
                p2 = players_list_sorted.pop(0)
                new_match = Match(player1=p1, player2=p2)
                match_list.append(new_match)

        return match_list


class MatchController:
    @staticmethod
    def process_match(match_list_objects, tournament_id):
        """
        Get user input for match results and updates standings.

        Args:
            match_list_objects (list): The matches to process.
            tournament_id (str): The current tournament ID.

        Returns:
            bool: True if all matches are processed, False otherwise.
        """
        view = MainView()
        # Create temporary list to hold scores before validation
        score_list = []

        try:
            for match in match_list_objects:

                # if Player 2 is missing
                if match.player2 is None:
                    # Update match object directly
                    match.score1 = 1.0
                    match.score2 = 0.0
                    score_list.append({"match": match, "p1": 1, "p2": 0})
                    continue

                # Prepare data for the view
                match_data = [match.player1.to_dict(), match.player2.to_dict()]
                # Get scores from user input
                score1, score2 = MatchView.display_match(match_data)

                # Update the match object
                match.score1 = score1
                match.score2 = score2

                score_list.append(
                    {"match": match, "p1": match.score1, "p2": match.score2}
                    )

        except KeyboardInterrupt:
            view.error("(CTRL+C)")
            return False

        except Exception as e:
            view.error(f"Error : {e}")
            return False

        view.display_success_and_refresh("All matches are finished")

        # Update standing
        for item in score_list:
            m = item["match"]
            score1 = item["p1"]
            score2 = item["p2"]

            if m.player2:
                if score1 > score2:
                    Round.update_standing(tournament_id, m.player1.id, 1)
                elif score1 < score2:
                    Round.update_standing(tournament_id, m.player2.id, 1)
                else:
                    Round.update_standing(tournament_id, m.player1.id, 0.5)
                    Round.update_standing(tournament_id, m.player2.id, 0.5)
            else:
                # Case for exempt
                Round.update_standing(tournament_id, m.player1.id, 1)

        return True


class ReportController:
    def __init__(self):
        self.players_controller = PlayersController()
        self.tournament_controller = TournamentController()
        self.report_view = ReportView()
        self.main_view = MainView()

    def report_sub_menu(self):
        while True:
            self.main_view.clean_console()
            response = self.report_view.display_report_sub_menu()

            menu_choice = {
                "1": self.players_controller.view_all_player,
                "2": self.tournament_controller.view_all_tournaments,
                "3": self.tournament_controller.view_tournament,
                "4": self.tournament_player_list,
                "5": self.tournament_summary
            }

            if response in menu_choice:
                user_choice = menu_choice[response]
                user_choice()

            elif response == "6":
                break

            else:
                self.main_view.error("Error : Wrong input")

    def tournament_player_list(self):
        self.main_view.clean_console()

        target_tournament = self.tournament_controller.select_tournament()
        if not target_tournament:
            return

        player_list_sorted = sorted(
            target_tournament.players, key=lambda p: p.surname, reverse=False
            )

        player_list_dicts = [p.to_dict() for p in player_list_sorted]

        self.report_view.display_players_in_tournament(
            target_tournament.name, player_list_dicts
            )

    def tournament_summary(self):
        self.main_view.clean_console()

        target_tournament = self.tournament_controller.select_tournament(
            filter_condition=lambda x: x.finish
            )
        if not target_tournament:
            return

        rounds_data = Round.tournament_summary(target_tournament.id)

        clean_rounds_data = []

        for round_data in rounds_data:
            round_name = round_data['name']
            formatted_matches = []

            for match in round_data['match_list']:
                # Data for player 1
                p1_data = match[0][0]
                p1_score = match[0][1]
                p1_txt = f"{p1_data['name']} {p1_data['surname']}"

                # Player 2 or exempt
                if match[1] and match[1][0]:
                    p2_data = match[1][0]
                    p2_score = match[1][1]
                    p2_txt = f"{p2_data['name']} {p2_data['surname']}"
                else:
                    p2_txt = "Exempt "
                    p2_score = "0"

                # Formated data
                row = [p1_txt, p1_score, "VS", p2_score, p2_txt]
                formatted_matches.append(row)

            clean_rounds_data.append({
                "name": round_name,
                "matches": formatted_matches
            })

        self.report_view.display_round_matches(clean_rounds_data)
