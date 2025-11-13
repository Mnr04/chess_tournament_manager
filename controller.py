from view import Main_view, Players_view
from models import Player, Tournament
import datetime

class Main_controller:
    def __init__(self):
        self.view = Main_view()
        self.players_controller = Players_controller()
  
    def run(self):
        while True:
            self.view.welcome_message()
            response = self.view.display_menu()

            menu_choice = {
                "1": self.players_controller.players_sub_menu,
                "2": "",
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

class Players_controller():
    def __init__(self):
        self.players_view = Players_view()
        self.main_view = Main_view()

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
        
    def create_new_tournament(self):
        tournament_data = self.view.get_new_tournament_inputs()

        name = tournament_data["name"]
        city = tournament_data["city"]
        year = tournament_data["year"]
        month = tournament_data["month"]
        day = tournament_data["day"]
        total_tour_number = tournament_data["Total_tour_number"]
        description = tournament_data["Description"]
        player_list = Player.get_all_players()

        try :
            year = int(year)
            month = int(month)
            day = int(day)
            date = datetime.date(year, month, day)
            date = date.isoformat()
            print(date)
        except:
            self.view.error("Date format invalid")
            return 

        if not name or not city or not date:
            self.view.error("Name, city, or start date cannot be empty.")
            return 
        try : 
            total_tour_number = int(total_tour_number) 
        except:
            total_tour_number = 4

        try:
            new_tournament = Tournament(name, city, date, total_tour_number,player_list, description)
            new_tournament.create_tournament()
        
            self.view.success(f"Tournament {name} saved successfully!")
            
        except Exception as e:
            self.view.error(f"Error while saving the tournament: {e}")
       
           
"""