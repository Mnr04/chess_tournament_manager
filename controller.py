from view import MainView, PlayersView, TournamentView, MatchView, RoundView, RepportView, InputView
from models import Player, Tournament, Round, Match
import datetime
import time

class MainController:
    def __init__(self):
        self.view = MainView()
        self.players_controller = PlayersController()
        self.tournaments_controller = TournamentController()
        self.repport_controller = RepportController()
  
    def run(self):
        while True:
            self.view.welcome_message()
            response = self.view.display_menu()

            menu_choice = {
                "1": self.players_controller.players_sub_menu,
                "2": self.tournaments_controller.tournament_sub_menu,
                "3": self.repport_controller.Repport_sub_menu,
            }
        
            if response in menu_choice:
                user_choice = menu_choice[response]
                user_choice()
                
            elif response == "4":
                 self.view.finish_message()
                 break
            
            else :
                self.view.error("Error : Wrong input")

class PlayersController():
    def __init__(self):
        self.players_view = PlayersView()
        self.main_view = MainView()

    def players_sub_menu(self):
        while True:
            MainView.clean_console()
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
            
            else :
                self.main_view.error("Error : Wrong input")
    
    def create_player(self):
        while True:
            player_data = self.players_view.get_new_player_inputs()
            
            ine_input = player_data["ine"]

            player_exist = Player.get_player_by_ine(ine_input)

            if player_exist:
                self.main_view.error(f"Error: Duplicate INE {ine_input} found.")
                self.main_view.error("Please re-start.")
                continue 
            
            else:
                break

        try:
            new_player = Player(**player_data)
            new_player.save_new_player()
            self.main_view.success(f"✅ Player {player_data['name']} {player_data['surname']} saved successfully!")
            time.sleep(1.5)
            self.main_view.clean_console()
            
        except Exception as e:
            self.main_view.error(f"Technical error while saving: {e}")
    
    @classmethod
    def select_player(cls):
        all_players = Player.get_all_players()
        
        if not all_players:
            MainView.error("❌ No players registered.")
            return None

        return PlayersView.select_player(all_players)
         
    def update_player(self):
        target_player = self.select_player()

        if not target_player or target_player == "RETURN":
            time.sleep(1)
            return

        while True:
            updated_data = self.players_view.update_player_inputs(target_player)
            
            new_ine = updated_data["ine"]
            
            existing_player_with_ine = Player.get_player_by_ine(new_ine)

            if existing_player_with_ine and existing_player_with_ine.id != target_player.id:
                self.main_view.error(f"Error: INE  is already taken.")
                self.main_view.error("Restarting update...")
                continue 
            
            else:
                break 

        Player.update_players(target_player.id, updated_data)
        self.main_view.success(" Player updated successfully!")
        time.sleep(1)
        MainView.clean_console()
            
    def view_player(self):
        target_player = self.select_player()
        MainView.clean_console()

        if not target_player:
            MainView.error("No players to display")
            time.sleep(1)
            return
        
        # Get info from model -->  database
        player_info = Player.get_players_by_id(target_player.id)
        # Case where player doesn't exist
        if not player_info:
            return
        
        # Display player data
        self.players_view.display_player_info(player_info)

    def view_all_player(self):
        # Get all players from Model --> Database
        all_players_sorted = Player.get_all_players()
        # Sort player by surname
        all_players_sorted = sorted(all_players_sorted, key=lambda x: x.surname, reverse=False)
        # Display all players infos
        if all_players_sorted == []:
            MainView.error("No players to display")
            time.sleep(1)
            return
        self.players_view.display_all_players(all_players_sorted)
 
    def remove_player(self):
        target_player = self.select_player()

        if not target_player:
            time.sleep(1)
            return

        # Get info from model -->  database
        player_info = Player.get_players_by_id(target_player.id)

        # Case where player doesn't exist
        if not player_info:
            self.main_view.error("Player not found!")
            return
        else :
            # remove player from database 
            Player.delete_player(player_info.id)
            self.main_view.success(f"player {target_player.name} {target_player.surname} delete successfully !")
            time.sleep(1)
            MainView.clean_console()

   
class TournamentController():
    def tournament_sub_menu(self):
        while True:
            response = TournamentView.display_tournaments_sub_menu()
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
            
            else :
                MainView.error("Error : Wrong input")

    def create_tournament(self):
        #Verify they are players registred in the application
            all_players = Player.get_all_players()
            if len(all_players) < 2:
                MainView.error("Register players in the application first, then create the tournament.")
                time.sleep(1)
                MainView.clean_console()
                return

            # Get tournament data and number of players in view
            tournament_data, number_of_players = TournamentView.get_tournament_inputs()

            # Verify date is ok
            if tournament_data["start_date"] > tournament_data["end_date"]:
                MainView.error("Error: Start date cannot be after End date.")
                return
            MainView.clean_console()
            # Get all the players list 
            player_list = self.get_players_list(number_of_players)
            
            # Update tournament data dictionnary with players
            tournament_data["players"] = player_list

            try:
                #map tournamant data keys with Tournament model to create tournament
                new_tournament = Tournament(**tournament_data)
                
                new_tournament.save_tournament()
                MainView.success(f"Tournament '{tournament_data['name']}' created successfully!")
                time.sleep(1)
                MainView.clean_console()

                
            except Exception as e:
                MainView.error(f"Error while saving: {e}")

    def update_tournament(self):
        # Select a tournament 
        target_tournament = self.select_tournament(filter_condition=lambda t: t.actual_round == 0)
        
        if not target_tournament:
                return
        
        update_info = TournamentView.update_tournament_inputs(target_tournament)
        if update_info["start_date"] > update_info["end_date"]:
            MainView.error("Invalid date")
            return
        
        #Update Players 
        players_data = self.manage_tournament_players(target_tournament.players)

        try:
            Tournament.update_tournament(target_tournament.id, update_info ,players_data)
            MainView.success("Tournament updated successfully!")
        except Exception as e:
            MainView.error(f"Error: {e}")
    
    def view_tournament(self):

        target_tournament = TournamentController.select_tournament()
        if not target_tournament:
            MainView.error("No Tournament!")
            return
        
        player_list = sorted(target_tournament.players, key=lambda x: x.surname, reverse=False)
        target_tournament.players = player_list
        
     
        TournamentView.display_tournament_info(target_tournament)
        return target_tournament
       
    def view_all_tournaments(self):
        all_tournaments = Tournament.get_all_tournement()
        TournamentView.display_all_tournament(all_tournaments)

    def remove_tournament(self):
        tournament_target = TournamentController.select_tournament()
        if not tournament_target:
            MainView.error("Tournament not find")
        
        TournamentView.display_delete_view(tournament_target["id"])     
        Tournament.delete_tournament(tournament_target["id"])

    def get_players_list(self, number_of_players, actual_players_data=None):
        registered_players = []

        already_registered = []
        if actual_players_data:
            already_registered = [p.id for p in actual_players_data]
        
        for i in range(int(number_of_players)):
            while True:
                print(f"\n--- Player {i + 1} / {number_of_players} ---")
                
                selected_player = PlayersController.select_player()

                if selected_player is None:
                    print("You must select a player.")
                    continue
      
                if selected_player.id in already_registered:
                    MainView.error("Player already registered in this tournament.")
                    continue 

                is_duplicate = False
                for p in registered_players:
                    if p.id == selected_player.id:
                        is_duplicate = True
                        break 
      
                if is_duplicate:
                    MainView.error(f"{selected_player.surname} is already selected in this list!")
                    continue 


                registered_players.append(selected_player)
                MainView.success(f"Player {selected_player.surname} added!")
                break 
                    
        return registered_players

    @classmethod
    def select_tournament(cls, filter_condition=None):
        # Get all tournament 
        all_tournaments = Tournament.get_all_tournement()

        if filter_condition:
            tournaments_to_display = [t for t in all_tournaments if filter_condition(t)]
        else:
            tournaments_to_display = all_tournaments

        if len(tournaments_to_display) == 0:
            MainView.error("No tournament to display.")
            return None
        
        return TournamentView.select_tournament(tournaments_to_display)
          
    def manage_tournament_players(self, actual_players_data):
        MainView.clean_console()
        while True:
            print(f"\n CURRENT PLAYERS LIST ({len(actual_players_data)})")
            TournamentView.print_players_table(actual_players_data)
            
            response = TournamentView.display_players_update_menu()
            
            if response == "1": 
                number_of_players = TournamentView.display_numbers_players("Add")
                list_update = self.get_players_list(number_of_players, actual_players_data)
                actual_players_data += list_update
            
            elif response == "2": 
                actual_players_data = self.remove_tournament_player(actual_players_data)
            
            elif response == "3": 
                return actual_players_data
                
            else:
                 MainView.error("Error : Wrong input")
    
    @classmethod
    def remove_tournament_player(self, players_data):
        to_delete = InputView.get_valid_int("How many players to remove? ")

        for i in range(to_delete):
            if not players_data:
                MainView.error("List is empty.")
                break

            user_choice = TournamentView.get_player_to_delete(players_data)

            if user_choice == 0:
                break 

            index = user_choice - 1 

            if 0 <= index < len(players_data):
                removed = players_data.pop(index)
                MainView.success(f"Player {removed.surname} deleted.")
            else:
                MainView.error("Invalid number.")

        return players_data

    def launch_tournament(self):
        # Select Tournament objects
        tournament = TournamentController.select_tournament(filter_condition=lambda x: x.finish == False)
        if not tournament:
            return

        Tournament.initialize_standings(tournament.id)
        
        while tournament.actual_round < tournament.total_round:
            
            RoundController.run_round(tournament)
            
            response = RoundView.display_continue_tournament(tournament.actual_round, tournament.total_round)
            if response == '2':
                break

        if tournament.actual_round == tournament.total_round:
            Tournament.finish_tournament(tournament.id)
            MainView.success('Tournament Finished')

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
        # Create round count + Round Object
        tournament.actual_round += 1
        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        new_round = Round(f"Round {tournament.actual_round}", start_time)

        # Get Player + match history
        players_list = Round.get_round_players_list(tournament.id)
        players_list_sorted = sorted(players_list, key=lambda p: p.score, reverse=True)
        match_history = Round.get_all_pairs_played(tournament.id)

        # Generate Pairs
        new_round.matches = cls.generate_pairs(players_list_sorted, match_history)

        # Create round file
        new_round.save_round(tournament.id)
        
        # Process Match and verify if finish
        round_finished = MatchController.process_match(new_round.matches, tournament.id)

        if not round_finished:
            print("Round not finish")
            tournament.actual_round -= 1
            return
        
        #end time
        new_round.end_time  = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        new_round.save_round(tournament.id)

        # Save the Round
        tournament.save_tournament()

    @staticmethod
    def generate_pairs(players_list_sorted, match_history):
        match_list = [] 
        
        if len(players_list_sorted) % 2 != 0:
            exit_player = players_list_sorted.pop()
            match_exit = Match(player1=exit_player, player2=None, score1=1, score2=0)
            match_list.append(match_exit)
        
        while len(players_list_sorted) > 0:
            p1 = players_list_sorted.pop(0) 
            match_found = False

            for i in range(len(players_list_sorted)):
                possible_opponent = players_list_sorted[i] 
                
                if not TournamentController.has_already_played(p1.id, possible_opponent.id, match_history):
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
    def process_match(match_list_objects, tournament_id):
        #create temporary list if round not finish
        score_list = []

        try:
            for match in match_list_objects:
                
                if match.player2 is None:
                    score_list.append({"match": match, "p1": 1, "p2": 0})
                    continue 

                match_data = [match.player1.to_dict(), match.player2.to_dict()]
                score1, score2 = MatchView.display_match(match_data) 

                match.score1 = float(score1)
                match.score2 = float(score2)

                score_list.append({"match": match, "p1": match.score1, "p2": match.score2})

        except (KeyboardInterrupt, Exception): 
            print("\n Error ")
            return False

        print("All match are finished")
        
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
                Round.update_standing(tournament_id, m.player1.id, 1)
        
        return True
    
class RepportController:
    def __init__(self):
            self.players_controller = PlayersController()
            self.tournament_controller = TournamentController()
            self.main_view = MainView()

    def Repport_sub_menu(self):
        while True:
            response = RepportView.display_repport_sub_menu()

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
            
            else :
                self.main_view.error("Error : Wrong input")

    def tournament_player_list(self):
        target_tournament = TournamentController.select_tournament()
        if not target_tournament:
            return
            
        player_list_sorted = sorted(target_tournament.players, key=lambda p: p.surname, reverse=False)
        
        player_list_dicts = [p.to_dict() for p in player_list_sorted]

        RepportView.display_players_in_tournament(target_tournament.name, player_list_dicts)

    def tournament_summary(self):
        target_tournament = TournamentController.select_tournament(filter_condition= lambda x : x.finish == True)
        if not target_tournament:
            return
            
        all_rounds_data = Round.tournament_summary(target_tournament.id)
        RepportView.display_round_matches(all_rounds_data)