from view import MainView, PlayersView, TournamentView, MatchView, RoundView, RapportView, InputView
from models import Player, Tournament, Round

class MainController:
    def __init__(self):
        self.view = MainView()
        self.players_controller = PlayersController()
        self.tournaments_controller = TournamentController()
        self.rapport_controller = RapportController()
  
    def run(self):
        while True:
            self.view.welcome_message()
            response = self.view.display_menu()

            menu_choice = {
                "1": self.players_controller.players_sub_menu,
                "2": self.tournaments_controller.tournament_sub_menu,
                "3": self.rapport_controller.Rapport_sub_menu,
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
        player_data = self.players_view.get_new_player_inputs()
        
        name = player_data["name"]
        surname = player_data["surname"]
        birth_date = player_data["birth_date"] 
        ine = player_data["ine"]

        try:
            new_player = Player(**player_data)
            new_player.save_new_player()
            self.main_view.success(f"Player {name} {surname} saved successfully!")
            
        except Exception as e:
            self.main_view.error(f"Technical error while saving: {e}")
    
    @classmethod
    def select_player(cls):
        while True : 
            # Get all the players
            all_players = Player.get_all_players()
            number_of_players = len(all_players) 
            
            # Case where player list is empty
            if number_of_players == 0:
                MainView.error("No players registered.")
                return

            # Display players list
            PlayersView.display_players_list(all_players)
    
            print(f"\nSelect a player (1 - {number_of_players})")
            user_choice = InputView.get_valid_int("Your choice (0 to cancel): ")

            # Case where user want to return
            if user_choice == 0:
                return 

            # User imputs need to be in [1 - number of players]
            if 1 <= user_choice <= number_of_players:
                
                index = user_choice - 1
                target_player = all_players[index]
                return target_player


            else:
                MainView.error(f"Error: Please choose a number between 1 and {number_of_players}")
         
    def update_player(self):
            target_player = self.select_player()

            if not target_player:
                return

            updated_data = self.players_view.update_player_inputs(target_player)
            Player.update_players(target_player.id, updated_data)
            
            self.main_view.success("Player updated successfully!")
            
    def view_player(self):
        target_player = self.select_player()

        if not target_player:
            return
        
        # Get info from model -->  database
        player_info = Player.get_players_by_id(target_player.id)
        # Case where player doesn't exist
        if not player_info:
            self.main_view.error("Player not found!")
            return
        
        # Display player data
        self.players_view.display_player_info(player_info)

    def view_all_player(self):
        # Get all players from Model --> Database
        all_players_sorted = Player.get_all_players()
        # Sort player by surname
        all_players_sorted = sorted(all_players_sorted, key=lambda x: x.surname, reverse=False)
        # Display all players infos
        self.players_view.display_all_players(all_players_sorted)
 
    def remove_player(self):
        target_player = self.select_player()

        if not target_player:
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
            # Print message 
            self.players_view.display_delete_view(player_info)
    
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
        # Get tournament data and number of players in view
        tournament_data, number_of_players = TournamentView.get_tournament_inputs()

        # Verify date is ok
        if tournament_data["start_date"] > tournament_data["end_date"]:
            MainView.error("Error: Start date cannot be after End date.")
            return
        # Get all the players list 
        player_list = self.get_players_list(number_of_players)
        
        # Update tournament data dictionnary with players
        tournament_data["players"] = player_list

        try:
            #map tournamant data keys with Tournament model to create tournament
            new_tournament = Tournament(**tournament_data)
            
            new_tournament.save_tournament()
            MainView.success(f"Tournament '{tournament_data['name']}' created successfully!")
            
        except Exception as e:
            MainView.error(f"Error while saving: {e}")

    def update_tournament(self):
        # Select a tournament 
        target_tournament = TournamentController.select_tournament(filter_condition=lambda t: t['actual_round'] == 0)
        
        if not target_tournament:
                return
        
        update_info = TournamentView.update_tournament_inputs(target_tournament)
        if update_info["start_date"] > update_info["end_date"]:
            MainView.error("Invalid date")
            return
        
        #Update Players 
        actual_players_data = target_tournament["players"]
        players_data = self.manage_tournament_players(actual_players_data)

        try:
            Tournament.update_tournament(target_tournament["id"], update_info ,players_data)
            MainView.success("Tournament updated successfully!")
        except Exception as e:
            MainView.error(f"Error: {e}")
    
    def view_tournament(self):

        target_tournament = TournamentController.select_tournament()
        if not target_tournament:
            MainView.error("No Tournament!")
            return
        
        player_list = sorted(target_tournament['players'], key=lambda x: x[1], reverse=False)
        target_tournament['players'] = player_list
        
     
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
            already_registered = [p[2] for p in actual_players_data]
        
        for i in range(int(number_of_players)):
            while True:
                print(f"\n--- Player {i + 1} / {number_of_players} ---")
                
                selected_player = PlayersController.select_player()

                if selected_player is None:
                    print("You must select a player.")
                    continue
      
                if selected_player['id'] in already_registered:
                    MainView.error("Player already registered in this tournament.")
                    continue 

                is_duplicate = False
                for p in registered_players:
                    if p[2] == selected_player['id']:
                        is_duplicate = True
                        break 
      
                if is_duplicate:
                    MainView.error(f"{selected_player['surname']} is already selected in this list!")
                    continue 


                registered_players.append([
                    selected_player['surname'], 
                    selected_player['name'], 
                    selected_player['id']
                ])
                MainView.success(f"Player {selected_player['surname']} added!")
                break 
                    
        return registered_players

    @classmethod
    def select_tournament(cls, filter_condition=None):
        all_tournaments = Tournament.get_all_tournement()

        if filter_condition:
            tournaments_to_display = [t for t in all_tournaments if filter_condition(t)]
        else:
            tournaments_to_display = all_tournaments

        number_of_tournaments = len(tournaments_to_display)

        if number_of_tournaments == 0:
            MainView.error("No tournament to display.")
            return None
        
        TournamentView.display_tournament_list(tournaments_to_display)
        
        print(f"\nSelect a tournament (1 - {number_of_tournaments})")
        user_choice = InputView.get_valid_int("Your choice (0 to cancel): ")

        if user_choice == 0:
            return None

        if 1 <= user_choice <= number_of_tournaments:
            index = user_choice - 1
            return tournaments_to_display[index]
        else:
            MainView.error(f"Error: Please choose a number between 1 and {number_of_tournaments}")
            return None
         
    def manage_tournament_players(self, actual_players_data):
        while True:
            print(f"\n CURRENT PLAYERS LIST ({len(actual_players_data)})")
            TournamentView.print_players_table(actual_players_data)
            
            response = TournamentView.display_players_update_menu()
            
            if response == "1": 
                number_of_players = TournamentView.display_numbers_players("Add")
                list_update = self.get_players_list(number_of_players, actual_players_data=actual_players_data)
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
                MainView.success(f"Player {removed[0]} deleted.")
            else:
                MainView.error("Invalid number.")

        return players_data

    def launch_tournament(self):
        #Select tournament to launch
        select_tournament = TournamentController.select_tournament(filter_condition=lambda x: x['finish'] == False)
        # Initialise standings 
        Tournament.initialize_standings(select_tournament['id'])
        # Get actual tournament status 
        actual_round = int(select_tournament["actual_round"])
        total_round = int(select_tournament["total_round"])

        #initialise match_history
        match_history = ()
        while actual_round != total_round:
            
            actual_round = RoundController.run_round(actual_round, select_tournament['id'], match_history)
               
            #Display to check if we continue
            response = RoundView.display_continue_tournament(actual_round, total_round)

            if response == '2':
                break

            if actual_round == total_round:
                Tournament.finish_tournament(select_tournament['id'])
                MainView.success('Tournament Finished')
                break
            
      
    def has_already_played(p1_id, p2_id, match_history):
        if [p1_id, p2_id] in match_history:
            return True
        
        if [p2_id, p1_id] in match_history:
            return True
            
        return False

class RoundController:
    def close_round(tournament_id, actual_round, match_list):
        Round.update_match_list(tournament_id, match_list, actual_round)
        Round.end_time_round(actual_round, tournament_id)
        MainView.success(f'Round {actual_round} Finished')

    @classmethod
    def run_round(cls, actual_round ,tournament_id, match_history):
        actual_round += 1
        Round.create_round(actual_round, tournament_id)
        Round.start_time_round(actual_round, tournament_id)
        # Get Player List
        player_list_sort= Round.get_round_players_list(tournament_id)
        #Create match
        match_list = RoundController.generate_pairs(player_list_sort, tournament_id)
        print(match_list)
        # Match Processing
        MatchController.process_match(match_list, tournament_id)
        # Close Round
        cls.close_round(tournament_id, actual_round, match_list)
        return actual_round

    def generate_pairs(player_list_sort, tournament_id):
        match_list = []

        match_history = Round.get_all_pairs_played(tournament_id)

        if len(player_list_sort) % 2 != 0:
            exit_player = player_list_sort.pop() 
            match_exit = [exit_player, None] 
            match_list.append(match_exit)
        
        while len(player_list_sort) > 0:
            player1 = player_list_sort.pop(0)
            match_found = False

            for i in range(len(player_list_sort)):
                possible_opponent = player_list_sort[i]

                p1_id = player1['id']
                p2_id = possible_opponent['id']
                
                if not TournamentController.has_already_played(p1_id, p2_id, match_history):
                    player2 = player_list_sort.pop(i) 
                    match = [player1, player2]
                    match_list.append(match)
                    match_found = True
                    break 
            
            if match_found == False:
                player2 = player_list_sort.pop(0)
                match = [player1, player2]
                match_list.append(match) 
        return match_list

class MatchController:
    def process_match(match_list, tournament_id):
        for match in match_list:
            score1, score2 = MatchView.display_match(match)

            #Case with 1 player exempt
            if match[1] == None :
                match[0]["Match_score"] = score1
                pass

            else : 
                match[0]["Match_score"] = score1
                match[1]["Match_score"] = score2
            
            # Analyse score and update standings
            if float(score1) > float(score2):
                Round.update_standing(tournament_id, match[0]["Id"], 1) 
            elif float(score1) < float(score2):
                Round.update_standing(tournament_id, match[1]["Id"], 1) 
            else:
                Round.update_standing(tournament_id, match[0]["Id"], 0.5)
                Round.update_standing(tournament_id, match[1]["Id"], 0.5)
    
class RapportController:
    def __init__(self):
            self.players_controller = PlayersController()
            self.tournament_controller = TournamentController()
            self.main_view = MainView()

    def Rapport_sub_menu(self):
        while True:
            response = RapportView.display_rapport_sub_menu()

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
        tournament_id = TournamentView.get_id_view()
        tournament_info = Tournament.get_tournament_by_id(tournament_id)
        player_list = [
            {"name": p[0], "surname": p[1], "id": p[2]} 
            for p in tournament_info["players"]
        ]
        player_list = sorted(player_list, key=lambda x: x['surname'], reverse=False)

        tournament_info['Players'] = player_list
        RapportView.display_players_in_tournament(tournament_info["name"],player_list)

    def tournament_summary(self):
        tournament_id = TournamentView.get_id_view()
        all_rounds_data = Round.tournament_summary(tournament_id)
        RapportView.display_round_matches(all_rounds_data)