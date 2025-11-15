from view import MainView, PlayersView, TournamentView
from models import Player, Tournament
import datetime

class MainController:
    def __init__(self):
        self.view = MainView()
        self.players_controller = PlayersController()
        self.tournaments_controller = TournamentController()
  
    def run(self):
        while True:
            self.view.welcome_message()
            response = self.view.display_menu()

            menu_choice = {
                "1": self.players_controller.players_sub_menu,
                "2": self.tournaments_controller.tournament_sub_menu,
                "3": "",
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

    # Sub_Menu
    def players_sub_menu(self):
        while True:
            response = self.players_view.display_players_sub_menu()

            menu_choice = {
                "1": self.create_new_player,
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
    
    # Create
    def create_new_player(self):
        player_data = self.players_view.get_new_player_inputs()

        try:
            name = player_data["name"]
            surname = player_data["surname"]
            age_str = player_data["age"]
            ine_str = player_data["ine"]

            if not name or not surname or not age_str or not ine_str:
                self.main_view.error("Name, surname, age, and INE cannot be empty.")
                return 

            age = int(age_str) 
            ine = int(ine_str)

        except ValueError:
            self.main_view.error(f"Error: The age '{age_str}' or INE '{ine_str}' is not a valid number.")
            return

        try:
            new_player = Player(surname=surname, name=name, age=age, ine=ine)
            new_player.save_new_player() 
            
            self.main_view.success(f"Player {name} {surname} saved successfully!")
            
        except Exception as e:
            self.main_view.error(f"Error while saving the player: {e}")
    
    # Update
    def update_player(self):
        #on recupere un id
        player_id = self.players_view.get_id_view()

        #on recupere les info du joueur via son id 
        player_info = Player.get_players_by_id(player_id)

        if not player_info:
            self.main_view.error("Player not found!")
            return

        player_data = self.players_view.update_player_inputs(player_info)

        try:
            player_data['age'] = int(player_data['age'])
            player_data['ine'] = int(player_data['ine'])
        except ValueError:
            self.main_view.error("Error , age or ine is not valid")
            return 

        try:
            Player.update_players(player_id, player_data)
            self.main_view.success("Player updated successfully!")
        except Exception as e:
            self.main_view.error(f"Error: {e}")

    # View
    def view_player(self):
        #Afficher une vue qui permet de choisir un joueur via son ID
        player_id = self.players_view.get_id_view()

        #On récupère les infos du joueur
        player_info = Player.get_players_by_id(player_id)

        if not player_info:
            self.main_view.error("Player not found!")
            return
        
        #On affiche ses données via un view
        self.players_view.display_player_info(player_info)

    # view all players
    def view_all_player(self):
        #On récupère tout les joueurs 
        all_players = Player.get_all_players()
        self.players_view.display_all_players(all_players)
 
    # Remove player
    def remove_player(self):
        #recupere player with id
        player_id = self.players_view.get_id_view()
        #creer option dans le model qui va supprimer ce joueur de la base de données
        Player.delete_player(player_id)
        self.players_view.display_delete_view(player_id)

class TournamentController():
    def tournament_sub_menu(self):
        while True:
            response = TournamentView.display_tournaments_sub_menu()
            menu_choice = {
                "1": self.create_new_tournament,
                "2": self.create_new_tournament,
                "3": self.update_tournament,
                "4": self.create_new_tournament,
                "5": self.create_new_tournament,
                "6": self.create_new_tournament
            }
        
            if response in menu_choice:
                user_choice = menu_choice[response]
                user_choice()
                
            elif response == "7":
                 break
            
            else :
                MainView.error("Error : Wrong input")

    #Create Tournament
    def create_new_tournament(self):
        tournament_data, str_numbers_of_players = TournamentView.get_new_tournament_inputs()

        name = tournament_data["name"]
        city = tournament_data["city"]
        total_tour_number = tournament_data["Total_tour_number"]
        description = tournament_data["Description"]
        player_list = ""

        if not name or not city :
            MainView.error("Name or city cannot be empty.")
            return 
        try : 
            total_tour_number = int(total_tour_number) 
        except:
            total_tour_number = 4

        try:
            #Logic to get numbers of players and send view to get Id, name and surname of players
            numbers_of_players = int(str_numbers_of_players)
            player_list = self.get_players_list(numbers_of_players)
            new_tournament = Tournament(name, city, total_tour_number,player_list, description)
            new_tournament.save_tournament()
        
            MainView.success(f"Tournament {name} saved successfully!")
            
        except Exception as e:
            MainView.error(f"Error while saving the tournament: {e}")

    def get_players_list(self, numbers_of_players):
        player_list = []
        numbers_of_players = int(numbers_of_players)
        for i in range(numbers_of_players):
            while True:
                print(f"\n--- Registration Player {i + 1} / {numbers_of_players} ---")
                
                id = TournamentView.get_players_list()
                target_player = Player.get_players_by_id(id)

                if target_player:
                    player_list.append([target_player["surname"], target_player["name"], target_player["id"]])
                    MainView.success(f"Player {target_player['surname']} added!")
                    break 
                else:
                    MainView.error(f"Player with ID {id} not found. Please try again.")

        return player_list

    #Update Tournament
    def update_tournament(self):
        #on recupere un id
        tournament_id = TournamentView.get_id_view()

        #on recupere les info du joueur via son id 
        tournament_info = Tournament.get_tournament_by_id(tournament_id)

        if not tournament_info:
            MainView.error("Tournament not found!")
            return

        tournament_data = TournamentView.update_tournament_inputs(tournament_info)

        try:
            tournament_data['Total_round'] = int(tournament_data['Total_round'])
        except ValueError:
            tournament_data['Total_round'] = 4
            return
        
        #Update Players 
        actual_players_data = tournament_info["Players"]
        players_data = self.update_tournament_players_menu(actual_players_data)
      
        try:
            Tournament.update_tournament(tournament_id, tournament_data,players_data)
            MainView.success("Tournament updated successfully!")
        except Exception as e:
            MainView.error(f"Error: {e}")

    #Update Tournament Player List
    def update_tournament_players_menu(self, actual_players_data):
        while True:
            print(f"📋 CURRENT PLAYERS LIST ({len(actual_players_data)})")
            TournamentView.print_players_table(actual_players_data)
            
            response = TournamentView.display_players_update_menu()
            
            if response == "1": 
                number_of_players = TournamentView.display_numbers_players("Add")
                list_update = self.get_players_list(number_of_players)
                actual_players_data += list_update
                #return actual_players_data
            
            elif response == "2": 
                actual_players_data = self.remove_tournament_player(actual_players_data)
                #return actual_players_data
            
            elif response == "3": 
                return actual_players_data
                
            else:
                 MainView.error("Error : Wrong input")
    
    @classmethod
    def remove_tournament_player(self, players_data):
        to_delete = TournamentView.display_numbers_players("Remove")
        to_delete = int(to_delete)
        for number in range(to_delete):
            while True:
                print(f"\n--- Delete Player {number + 1} / {to_delete} ---")
                target_id = TournamentView.get_remove_list()
                
                player_found = False
                for index, p in enumerate(players_data):
                    if p[2] == target_id:
                        removed_player = players_data.pop(index)
                        print(f"Joueur {removed_player[0]} {removed_player[1]} (ID: {target_id}) supprimé.")
                        player_found = True
                        break 
                
                if player_found:
                    break 
                else:
                    MainView.error(f"Player {target_id} not in tournament , retry")
                    
        return players_data



            
  







""" 
    # Tournament Option
  
    def all_tournament_list(self):
        tournament_list = Tournament.get_all_tournaments()
        value = self.view.display_tournament_list(tournament_list)
        
        for tournament in tournament_list:
            if value in tournament_list:
                print(True)
    
    
        response = self.view.display_tournaments_menu()
        menu_choice = {
            "A": self.create_new_tournament,
            "R": self.view.display_menu,
            "M": self.all_tournament_list
        }
              
"""