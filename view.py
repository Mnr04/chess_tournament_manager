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
        print(tabulate(all_players, headers="keys", tablefmt="fancy_grid"))
        
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
        start_date = input("Start Date (YYYY-MM-DD): ")
        end_date = input("End Date (YYYY-MM-DD): ")
        total_tour_number = input("Total tour number:  (default = 4)")
        description = input("description: ")
        numbers_of_players = input("How many players in this Tournament ? : ")

        return {"name": name, "city": city, "Total_tour_number":total_tour_number, "Description":description, "Start_date": start_date, "End_date" : end_date}, numbers_of_players

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
        city = input(f"City ({tournament['City']}): ") or tournament['City']
        start_date = input(f"start date ({tournament['Start_date']}): ") or tournament['Start_date']
        end_date = input(f"end date ({tournament['End_date']}): ") or tournament['End_date']
        total_round = input(f"Age ({tournament['Total_round']}): ") or tournament['Total_round']
        description = input(f"INE ({tournament['Description']}): ") or tournament['Description']

        return {"Name": name, "City": city, "Total_round": total_round, "Description": description, "Players": [], "Start_date" :start_date, "End_date" :end_date}
    
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

    @staticmethod
    def display_tournament_info(tournaments_info):
        print(f"{'Name':<12} : {tournaments_info['Name']}")
        print(f"{'City':<12} : {tournaments_info['City']}")
        print(f"{'Start date':<12} : {tournaments_info['Start_date']}")
        print(f"{'End date':<12} : {tournaments_info['End_date']}")
        print(f"{'Total round':<12} : {tournaments_info['Total_round']}")
        print(f"they are {len(tournaments_info['Players'])} players Registred")
        print("Players List: ")
        for info in tournaments_info['Players']:
            print(f"Name : {info["Name"]}, Surname : {info["Surname"]},  Id : {info["Id"]}")

        print(f"{'Description':<12} : {tournaments_info.get('Description'), 'N/A'}")
        
        response = input("Press any button to return")
        return response
    
    #View all Tournaments
    @staticmethod
    def display_all_tournament(all_tournaments):
        table_data = [
            {
                "ID": data.get("id"), 
                "Name": data.get("Name"), 
                "City": data.get("City"),
                "Players": len(data.get("Players")), 
                "Description": data.get("Description", "")[0:15] 
            } for data in all_tournaments
        ]
            
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid")) 
        
        input("Press any button to return")

    @staticmethod
    def display_delete_view(tournament_id):
        print(f"Tournament {tournament_id} succesfuly delete")
        input("Press any button to return")

    def display_start_tournament(all_tournaments):
        table_data = [
            {
                "ID": data.get("id"), 
                "Name": data.get("Name"), 
                "City": data.get("City"),
                "Players": len(data.get("Players")), 
                "Description": data.get("Description", "")[0:15] 
            } for data in all_tournaments
        ]
        print("List of tournament ready to start ! ")
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))
        return input("tap id of tournament you want to start: ")

class RoundView():
    def display_continue_tournament(actual_round, total_round):
        print(f'Round {actual_round} / {total_round} Finished')
        print("[Any Button] Continue")
        print("[2] Stop")
        reponse = input("Your choice: ")
        return reponse

class MatchView():
    @staticmethod
    def display_match(match):
        if match[1] is None:
            print(f"⚠️  {match[0]['Name']} is exempt (Bye) and wins 1 point.")
            return 1, 0 
        
        player1_data = match[0] 
        player2_data = match[1]

        print(f"\n--- MATCH : {player1_data['Name']} vs {player2_data['Name']} ---")
        
        valid_scores = ['0', '0.5', '1']

        while True:
            score1 = input(f"Score {player1_data['Name']} (0, 0.5, 1): ")
            if score1 in valid_scores:
                break 
            print("Invalid score. Please enter 0, 0.5 or 1.")

        while True:
            score2 = input(f"Score {player2_data['Name']} (0, 0.5, 1): ")
            if score2 in valid_scores:
                if float(score1) + float(score2) != 1:
                     print(f"Total must be 1 (Ex: 1 vs 0, or 0.5 vs 0.5)")
                     continue 
                break
            print("Invalid score.")

        return score1, score2

class RapportView:
    @staticmethod
    def display_rapport_sub_menu():
        print("\n--- 📊 REPORTS MENU ---")
        print(" [1] List of all players 👥")
        print(" [2] List of all tournaments 🏆")
        print(" [3] Tournament Details (Name & Dates) 📅")
        print(" [4] Tournament Players (Alphabetical) ♟️")
        print(" [5] Tournament Rounds & Matches ⚔️")
        print(" [6] Return to Main Menu ❌")
        
        response = input("Your choice: ")
        return response
    
    def display_players_in_tournament(tournament_name, player_list):
        print(f"Players list for {tournament_name} Tournament 🏆")
        print(tabulate(player_list, headers="keys", tablefmt="fancy_grid"))
        
        input("Press any button to return")
