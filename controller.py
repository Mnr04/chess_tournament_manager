from view import MainView, PlayersView, TournamentView, MatchView, RoundView, RapportView
from models import Player, Tournament, Round
import datetime

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
        all_players_sorted = Player.get_all_players()
        all_players_sorted = sorted(all_players_sorted, key=lambda x: x['surname'], reverse=False)
        self.players_view.display_all_players(all_players_sorted)
 
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
                "2": self.launch_tournament,
                "3": self.update_tournament,
                "4": self.view_tournament_info,
                "5": self.view_all_tournaments,
                "6": self.remove_tournaments,
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
        start_date = tournament_data["Start_date"]
        end_date = tournament_data["End_date"]

        #Date et city verification
        if not name or not city :
            MainView.error("Name or city cannot be empty.")
            return
        #Number verification
        try : 
            total_tour_number = int(total_tour_number) 
        except:
            total_tour_number = 4
        #Date verification
        try : 
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

        except ValueError:
            MainView.error("Invalid date format")
            return

        if start_date > end_date:
            MainView.error("Invalid date format")
            return
            
        #clean the date
        start_date_str = start_date.isoformat()
        end_date_str = end_date.isoformat()

        try:
        #Logic to get numbers of players and send view to get Id, name and surname of players
            numbers_of_players = int(str_numbers_of_players)
            player_list = self.get_players_list(numbers_of_players)
            new_tournament = Tournament(name, city, total_tour_number,player_list, description, start_date_str, end_date_str)
            new_tournament.save_tournament()
            
            MainView.success(f"Tournament {name} saved successfully!")
            
        except Exception as e:
            MainView.error(f"Error while saving the tournament: {e}")
            return
        else : 
            MainView.error("Probleme with date")

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
        try :  
            tournament_info = Tournament.get_tournament_by_id(tournament_id)

        except :
            MainView.error("Tournament not found!")
            return

        #On recupere les nouveaux inputs
        tournament_data = TournamentView.update_tournament_inputs(tournament_info)

        try:
            tournament_data['Total_round'] = int(tournament_data['Total_round'])
        except ValueError:
            tournament_data['Total_round'] = 4
            return
        
        #Date verification
        try : 
            tournament_data["Start_date"] = datetime.datetime.strptime(tournament_data["Start_date"], "%Y-%m-%d").date()
            tournament_data["End_date"] = datetime.datetime.strptime(tournament_data["End_date"], "%Y-%m-%d").date()

        except ValueError:
            MainView.error("Invalid date format")
            return

        if tournament_data["Start_date"] > tournament_data["End_date"]:
            MainView.error("Invalid date format")
            return
            
        #clean the date
        tournament_data["Start_date"] = tournament_data["Start_date"].isoformat()
        tournament_data["End_date"] = tournament_data["End_date"].isoformat()

        
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

    #Access one tournament data
    def view_tournament_info(self):
        tournament_id = TournamentView.get_id_view()
        tournament_info = Tournament.get_tournament_by_id(tournament_id)

        if not tournament_info:
            MainView.error("Tournament not found!")
            return
        
        player_list = [
            {"Name": p[0], "Surname": p[1], "Id": p[2]} 
            for p in tournament_info["Players"]
        ]
        player_list = sorted(player_list, key=lambda x: x['Surname'], reverse=False)

        tournament_info['Players'] = player_list

        TournamentView.display_tournament_info(tournament_info)
        return tournament_info

    #Access all tournaments data
    def view_all_tournaments(self):
        #On récupère tout les joueurs 
        all_tournaments = Tournament.get_all_tournement_info()
        TournamentView.display_all_tournament(all_tournaments)

    #Remove Tournaments
    def remove_tournaments(self):
        #recupere player with id
        tournament_id = TournamentView.get_id_view()
        #creer option dans le model qui va supprimer ce joueur de la base de données
        response = Tournament.delete_tournament(tournament_id)
        if response == False:
            MainView.error("Tournament not find")
        else:
            TournamentView.display_delete_view(tournament_id)     
  
    #Start Tournament
    def launch_tournament(self):
        tournament_not_finish = [t for t in Tournament.get_all_tournement_info() if t['Finish'] == False]
        tournament_id = TournamentView.display_start_tournament(tournament_not_finish)
        
        #On active le compteur des rounds pour le tournois
        Tournament.start_tournament(tournament_id)
        
        #On recupère les infos du tournois
        tournament_info = Tournament.get_tournament_by_id(tournament_id)

        #on récupère le statut actuel du tournois
        actual_round = int(tournament_info["Actual_round"])
        total_round = int(tournament_info["Total_round"])

        #On initialise le match_history
        match_history = ()

        while actual_round != total_round:
            
            actual_round = TournamentController.run_round(actual_round, tournament_id, match_history)
               
            #Display pour voir si on contunue
            response = RoundView.display_continue_tournament(actual_round, total_round)

            if response == '2':
                break

            if actual_round == total_round:
                Tournament.finish_tournament(tournament_id)
                MainView.success('Tournament Finished')
                break
        
    def process_match(match_list, tournament_id):
        for match in match_list:
            score1, score2 = MatchView.display_match(match)

            match[0]["Match_score"] = score1
            match[1]["Match_score"] = score2
                
            #on check les scores et update le ranking en fonction 
            if float(score1) > float(score2):
                Round.update_ranking(tournament_id, match[0]["Id"], 1) 
            elif float(score1) < float(score2):
                Round.update_ranking(tournament_id, match[1]["Id"], 1) 
            else:
                Round.update_ranking(tournament_id, match[0]["Id"], 0.5)
                Round.update_ranking(tournament_id, match[1]["Id"], 0.5)

    def close_round(tournament_id, actual_round, match_list):
        Round.update_match_list(tournament_id, match_list, actual_round)
        Tournament.update_tournament_statut(tournament_id)
        Round.end_time_round(actual_round, tournament_id)
        MainView.success(f'Round {actual_round} Finished')

    def run_round(actual_round ,tournament_id, match_history):
        actual_round += 1
        Round.create_round(actual_round, tournament_id)
        Round.start_time_round(actual_round, tournament_id)
        #on recupère la liste des joueurs
        player_list_sort= Round.get_round_players_list(tournament_id)
        #on creer la match list
        match_list = TournamentController.generate_pairs(player_list_sort, match_history)
        #On Génère les matchs et met à jour le ranking
        TournamentController.process_match(match_list, tournament_id)
        #On Close le Round
        TournamentController.close_round(tournament_id, actual_round, match_list)
        return actual_round
    
    def generate_pairs(player_list_sort, match_history):
        match_list = []

        #Cas ou list players impair , on pop le dernier et on lui donne 1 point
        if len(player_list_sort) % 2 != 0:
            exit_player = player_list_sort.pop() 
            match_exit = [exit_player, None] 
            match_list.append(match_exit)
        
        while len(player_list_sort) > 0:
            player1 = player_list_sort.pop(0)
            match_found = False
            for i in range(len(player_list_sort)):
                possible_opponent = player_list_sort[i]

                p1_id = player1['Id']
                p2_id = possible_opponent['Id']
                
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

    def has_already_played(p1_id, p2_id, match_history):
        if [p1_id, p2_id] in match_history:
            return True
        
        if [p2_id, p1_id] in match_history:
            return True
            
        return False
    
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
                "3": self.tournament_controller.view_tournament_info,
                "4": self.tournament_player_list,
                "5": ''
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
            {"Name": p[0], "Surname": p[1], "Id": p[2]} 
            for p in tournament_info["Players"]
        ]
        player_list = sorted(player_list, key=lambda x: x['Surname'], reverse=False)

        tournament_info['Players'] = player_list
        RapportView.display_players_in_tournament(tournament_info["Name"],player_list)