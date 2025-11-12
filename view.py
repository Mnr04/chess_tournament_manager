
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
        print(" [3] Remove Player")
        print(" [3] View Player")
        print(" [4] Return ❌")
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
    def update_view(self):
        print("\n--- Choose player to update ---")
        player_id = input("Player id to update: " )
        return player_id
    
    def update_player_inputs(self, player):
        print(f"\n--- Update Player {player['name']} {player['surname']} ---") 
        
        name = input(f"Last Name ({player['surname']}): ") or player['surname']
        surname = input(f"First Name ({player['name']}): ") or player['name']
        age = input(f"Age ({player['age']}): ") or player['age']
        ine = input(f"INE ({player['ine']}): ") or player['ine']

        return {"name": name, "surname": surname, "age": age, "ine": ine}
    
  
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
