from tabulate import tabulate

class MainView:
    #Message 
    @staticmethod
    def welcome_message():
        print("--- Welcome in Chess Manager ---")
    
    @staticmethod
    def finish_message():
        print("--- See you next time ---")

    @staticmethod
    def error(message):
        print(message)

    @staticmethod
    def success(message):
        print(message)
    
    # Main Menu
    def display_menu(self):
        print("\nMain Menu:")
        print(" [1] Players 👤")
        print(" [2] Tournaments 🏆")
        print(" [3] Rapports")
        print(" [4] Quit ❌")
        reponse = input("Your choice: ")
        return reponse
    
class PlayersView():
    @staticmethod
    def display_players_sub_menu():
        print("\nPlayers Menu:")
        print(" [1] Create Player 👤")
        print(" [2] Update Player 🏆")
        print(" [3] View Player")
        print(" [4] View All Player")
        print(" [5] Remove Player")
        print(" [6] Return ❌")
        reponse = input("Your choice: ")
        return reponse
    
    #Create Player
    @staticmethod
    def get_new_player_inputs():
        print("\n--- Add a new player ---")
        
        name = input("Last Name: ")
        surname = input("First Name: ")
        age = input("Age: ")
        ine = input("INE: ")

        return {"name": name, "surname": surname, "age": age, "ine": ine}
    
    #Update Player
    @staticmethod
    def get_id_view():
        print("\n--- Choose player ---")
        player_id = input("Player id: " )
        return player_id
    
    @staticmethod
    def update_player_inputs(player):
        print(f"\n--- Update Player {player['name']} {player['surname']} ---") 
        
        name = input(f"Last Name ({player['surname']}): ") or player['surname']
        surname = input(f"First Name ({player['name']}): ") or player['name']
        age = input(f"Age ({player['age']}): ") or player['age']
        ine = input(f"INE ({player['ine']}): ") or player['ine']

        return {"name": name, "surname": surname, "age": age, "ine": ine}
    
    #View Player
    @staticmethod
    def display_player_info(player_info):
        print(f"Id : {player_info['id']}")
        print(f"Name : {player_info['name']}")
        print(f"Surname : {player_info['surname']}")
        print(f"Age : {player_info['age']}")
        print(f"Ine : {player_info['ine']}")
        
        response = input("Press any button to return")
        return response

    #View all Players
    @staticmethod
    def display_all_players(all_players):
        print(tabulate(all_players, headers="keys"))
        
        input("Press any button to return")

    #Delete View
    def display_delete_view(cls, player_id):
        print(f"Player {player_id} succesfuly delete")
        input("Press any button to return")

class TournamentView():
    # Tournament Menu
    @staticmethod
    def display_tournaments_sub_menu():
        print(" [1] Create Tournaments ➕")
        print(" [2] Start Tournament ➕")
        print(" [3] Update Tournaments 🛠️")
        print(" [4] view Tournament ➕")
        print(" [5] view all Tournaments ➕")
        print(" [6] Remove Tournaments 🛠️")
        print(" [7] Return ⬅️")
        reponse = input("Your choice: ")
        
        return reponse
    
    @staticmethod
    def get_new_tournament_inputs():
    
        print("\n--- Create a new tournament ---")
        
        name = input("Tournament Name: ")
        city = input("City: ")
        Total_tour_number = input("Total tour number:  (default = 4)")
        Description = input("description: ")
        numbers_of_players = input("How many players in this Tournament ? : ")

        return {"name": name, "city": city, "Total_tour_number":Total_tour_number, "Description":Description}, numbers_of_players

    @staticmethod
    def get_players_list():
        print("\n--- Enter id of player you want to registred ---")
        id = input("id: ")
        return id

    @staticmethod
    def get_id_view():
        print("\n--- Choose Tournament ---")
        tournament_id = input("Tournament id: " )
        return tournament_id

    @staticmethod
    def update_tournament_inputs(tournament):
        print(f"\n--- Update Tournament {tournament['Name']} ---") 
        
        name = input(f"Last Name ({tournament['Name']}): ") or tournament['Name']
        City = input(f"City ({tournament['City']}): ") or tournament['City']
        Total_round = input(f"Age ({tournament['Total_round']}): ") or tournament['Total_round']
        Description = input(f"INE ({tournament['Description']}): ") or tournament['Description']

        return {"Name": name, "City": City, "Total_round": Total_round, "Description": Description, "Players": []}
    
    def display_players_update_menu():
        print("Do you add or remove player list")
        print(" [1] Add player 👤")
        print(" [2] Remove Player 🏆")
        print(" [3] NO")
        response = input("Your Choice: ")
        return response
    

    def display_numbers_players(action):
        print(f"How many player you want to {action}? ")
        numbers_of_players = input("Your choice ? : ")
        return numbers_of_players
    
    @staticmethod
    def get_remove_list():
        print("\n--- Enter id of player you want to remove ---")
        id = input("id: ")
        return id
    
    def print_players_table(players_list):
        if not players_list:
            print("   🚫 No players registered yet.")
        else:
            headers = ["Surname", "Name", "ID"]
            print(tabulate(players_list, headers=headers, tablefmt="simple"))