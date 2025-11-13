from tabulate import tabulate

class Main_view:
    #Message 
    def welcome_message(self):
        print("--- Welcome in Chess Manager ---")
    
    def finish_message(self):
        print("--- See you next time ---")

    def error(self, message):
        print(message)

    def success(self, message):
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
    
class Players_view():
    def display_players_sub_menu(self):
        print("\Players Menu:")
        print(" [1] Create Player 👤")
        print(" [2] Update Player 🏆")
        print(" [3] View Player")
        print(" [4] View All Player")
        print(" [5] Remove Player")
        print(" [6] Return ❌")
        reponse = input("Your choice: ")
        return reponse
    
    #Create Player
    def get_new_player_inputs(self):
        print("\n--- Add a new player ---")
        
        name = input("Last Name: ")
        surname = input("First Name: ")
        age = input("Age: ")
        ine = input("INE: ")

        return {"name": name, "surname": surname, "age": age, "ine": ine}
    
    #Update Player
    def get_id_view(self):
        print("\n--- Choose player ---")
        player_id = input("Player id: " )
        return player_id
    
    def update_player_inputs(self, player):
        print(f"\n--- Update Player {player['name']} {player['surname']} ---") 
        
        name = input(f"Last Name ({player['surname']}): ") or player['surname']
        surname = input(f"First Name ({player['name']}): ") or player['name']
        age = input(f"Age ({player['age']}): ") or player['age']
        ine = input(f"INE ({player['ine']}): ") or player['ine']

        return {"name": name, "surname": surname, "age": age, "ine": ine}
    
    #View Player
    @classmethod
    def display_player_info(cls, player_info):
        print(f"Id : {player_info['id']}")
        print(f"Name : {player_info['name']}")
        print(f"Surname : {player_info['surname']}")
        print(f"Age : {player_info['age']}")
        print(f"Ine : {player_info['ine']}")
        
        response = input("Press any button to return")
        return response
    @classmethod
    #View all Players
    def display_all_players(cls, all_players):
        print(tabulate(all_players, headers="keys"))
        
        input("Press any button to return")

    #Delete View
    def display_delete_view(cls, player_id):
        print(f"Player {player_id} succesfuly delete")
        input("Press any button to return")
""" 
    # Tournament Menu
    def display_tournaments_menu(self):
        print(" [A] New Tournaments ➕")
        print(" [M] Manage Tournaments 🛠️")
        print(" [R] Return ⬅️")
        reponse = input("Your choice: ")
        return reponse
    
    def get_new_tournament_inputs(self):
    
        print("\n--- Create a new tournament ---")
        
        name = input("Tournament Name: ")
        city = input("City: ")
        print("start Date : ")
        year = input('Enter a year [yyyy]: ')
        month = input('Enter a month [mm]: ')
        day = input('Enter a day [d]: ')
        Total_tour_number = input("Total tour number:  (default = 4)")
        Description = input("description: ")

        return {"name": name, "city": city, "year":year, "month":month, "day":day, "Total_tour_number":Total_tour_number, "Description":Description}

"""
