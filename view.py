from tabulate import tabulate
import datetime
import re
import os

class MainView:
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
        
        name = InputView.get_valid_name("Last Name: ")
        surname = InputView.get_valid_name("First Name: ")
        birth_date = InputView.get_valid_date("Birth Date (YYYY-MM-DD): ")
        ine = InputView.get_valid_ine("INE (AB12345): ")

        return {
            "name": name, 
            "surname": surname, 
            "birth_date": birth_date, 
            "ine": ine
        }
    
    #Update Player
    @staticmethod
    def get_id_view():
        print("\n--- Choose player ---")
        player_id = input("Player id: " )
        return player_id
    
    @staticmethod
    def update_player_inputs(player):
        print(f"\n--- Update Player {player.name} {player.surname} ---") 
        
        surname = InputView.get_valid_name(
            f"Last Name ({player.surname}): ", 
            default=player.surname
        )
        
        name = InputView.get_valid_name(
            f"First Name ({player.name}): ", 
            default=player.name
        )
        
        birth_date = InputView.get_valid_date(
            f"Birth Date ({player.birth_date}): ", 
            default=player.birth_date
        )
        
        ine = InputView.get_valid_ine(
            f"INE ({player.ine}): ", 
            default=player.ine
        )

        return {
            "name": name, 
            "surname": surname, 
            "birth_date": birth_date, 
            "ine": ine
        }
    
    @staticmethod
    def display_players_list(players_list):
        print("\n--- Players List ---")
        for i, player in enumerate(players_list, start=1):
            print(f"[{i}] {player.name} {player.surname} ({player.ine})")
            
        print("[0] Return")
    
    #View Player
    @staticmethod
    def display_player_info(player_info):
        print(f"Id : {player_info.id}")
        print(f"Name : {player_info.name}")
        print(f"Surname : {player_info.surname}")
        print(f"birth date : {player_info.birth_date}")
        print(f"Ine : {player_info.ine}")
        
        response = input("Press any button to return")
        return response

    #View all Players
    @staticmethod
    def display_all_players(all_players):
        # Transform player objects in dictonnary
        table_data = [player.to_dict() for player in all_players]
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))
    
        input("Press any button to return")

    #Delete View
    def display_delete_view(cls, player_info):
        print(f"Player {player_info.name} {player_info.surname} succesfuly delete")
        input("Press any button to return")

class TournamentView():

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
    def get_tournament_inputs():
        print("\n--- Create a new tournament ---")
        
        name = InputView.get_valid_name("Tournament Name: ")
        city = InputView.get_valid_name("City: ")
        start_date = InputView.get_valid_date("Start Date (YYYY-MM-DD): ")
        end_date = InputView.get_valid_date("End Date (YYYY-MM-DD): ")
        total_round = InputView.get_valid_int("Total round number (default = 4): ", 4)
        description = input("Description: ") 
    
        numbers_of_players = InputView.get_valid_int("How many players?: ")

        return {
            "name": name, 
            "city": city, 
            "total_round": total_round,   
            "description": description,   
            "start_date": start_date,     
            "end_date": end_date          
        }, numbers_of_players

    @staticmethod
    def update_tournament_inputs(tournament):
        print(f"\n--- Update Tournament {tournament.name} ---") 
        
        name = InputView.get_valid_name(
            f"Name ({tournament.name}): ", 
            default=tournament.name
        )
        
        city = InputView.get_valid_name(
            f"City ({tournament.city}): ", 
            default=tournament.city
        )
        
        start_date = InputView.get_valid_date(
            f"Start Date ({tournament.start_date}): ", 
            default=tournament.start_date
        )

        end_date = InputView.get_valid_date(
            f"End date ({tournament.end_date}): ", 
            default=tournament.end_date
        )
        
        total_round = InputView.get_valid_int(
            f"Total Round ({tournament.total_round}): ", 
            default=tournament.total_round
        )

        description = InputView.get_valid_name(
            f"Description ({tournament.description}): ", 
            default=tournament.description
        )

        return {
            "name": name, 
            "city": city, 
            "total_round": total_round, 
            "description": description, 
            "players": [], 
            "start_date": start_date, 
            "end_date": end_date
        }
    
    @staticmethod
    def display_players_update_menu():
        print("Do you add or remove player list")
        print(" [1] Add player 👤")
        print(" [2] Remove Player 🏆")
        print(" [3] Finish and Save")
        response =input("Your choice: ")
        return response
    
    @staticmethod
    def display_numbers_players(action):
        print(f"How many player you want to {action}? ")
        numbers_of_players = input("Your choice ? : ")
        return numbers_of_players
    
    @staticmethod
    def print_players_table(players_list):
        if not players_list:
            print("   🚫 No players registered yet.")
        else:
            table_data = [player.to_dict() for player in players_list]
            print(tabulate(table_data, headers="keys", tablefmt="fancy_grid"))
  
    @staticmethod
    def display_tournament_info(tournament): 
        print("\n--- TOURNAMENT DETAILS ---")

        general_data = [
            ["Name", tournament.name],
            ["City", tournament.city],
            ["Start Date", tournament.start_date],
            ["End Date", tournament.end_date],
            ["Total Rounds", tournament.total_round],
            ["Finish", "Finished" if tournament.finish else "In Progress"],
            ["Description", tournament.description] 
        ]

        print(tabulate(general_data, tablefmt="fancy_grid"))

        len_players = len(tournament.players)
        print(f"\n -- REGISTERED PLAYERS ({len_players}) ---")

        if len_players == 0:
            print("   No players registered yet.")
        else:
            headers = ["Name", "Surname", "ID"]
            
            players_data = [[p.name, p.surname, p.id] for p in tournament.players]

            print(tabulate(players_data, headers=headers, tablefmt="fancy_grid"))
        
        input("\nPress Enter to return...")
    
    @staticmethod
    def display_all_tournament(all_tournaments):
        table_data = [
            {
                "ID": data.id, 
                "Name": data.name, 
                "City": data.city,
                "Players": len(data.players), 
                "Description": data.description[0:15] if data.description else ""
            } for data in all_tournaments
        ]
            
        print(tabulate(table_data, headers="keys", tablefmt="fancy_grid")) 
        
        input("Press any button to return")

    @staticmethod
    def display_delete_view(tournament_id):
        print(f"Tournament {tournament_id} succesfuly delete")
        input("Press any button to return")
    
    @staticmethod
    def display_tournament_list(all_tournaments):
        print("\n--- Tournament List ---")
        for i, tournament in enumerate(all_tournaments, start=1):
            print(f"[{i}] {tournament.name} {tournament.city}")
            
        print("[0] Return")

    @staticmethod
    def get_player_to_delete(players_list):
        print("\n--- DELETE PLAYER ---")
        
        for i, p in enumerate(players_list):
            print(f"[{i + 1}] {p.name} {p.surname}") 
            
        choice = InputView.get_valid_int(f"Number to remove (0 to cancel): ")
        return choice

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
            print(f"{match[0]['name']} is exempt and wins 1 point.")
            return 1, 0 
        
        player1_data = match[0] 
        player2_data = match[1]

        print(f"\n--- MATCH : {player1_data['name']} vs {player2_data['name']} ---")
        
        valid_scores = ['0', '0.5', '1']

        while True:
            score1 = input(f"Score {player1_data['name']} (0, 0.5, 1): ")
            if score1 in valid_scores:
                break 
            print("Invalid score. Please enter 0, 0.5 or 1.")

        while True:
            score2 = input(f"Score {player2_data['name']} (0, 0.5, 1): ")
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

    @staticmethod
    def display_round_matches(all_rounds_data):
        
        for round_data in all_rounds_data:
            round_name = round_data['name']
            match_list = round_data['match_list']
            
            print(f"\n--- {round_name} ---") 
            
            table_data = []

            for match in match_list:
                # Match Object structure : [[p1_dict, s1], [p2_dict, s2]]
                p1_data = match[0][0]  
                p1_score = match[0][1] 
                p1_name = f"{p1_data['name']} {p1_data['surname']}"
            
                if match[1] and match[1][0]: 
                    p2_data = match[1][0]
                    p2_score = match[1][1]
                    p2_name = f"{p2_data['name']} {p2_data['surname']}"
                else:
                    p2_name = "Exempté"
                    p2_score = "0"

                row = [p1_name, p1_score, "VS", p2_score, p2_name]
                table_data.append(row)

            headers = ["Player 1", "Pts", "", "Pts", "Player 2"]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
            
        input("\nPress any button to return")
      
class InputView:
    @staticmethod
    def get_non_empty_string(prompt):
        while True:
            user_input = input(prompt)
            if user_input.strip(): 
                return user_input
            print("Error: This field cannot be empty.")

    @staticmethod
    def get_valid_date(prompt, default=None):
        while True:
            date_str = input(prompt).strip()
            
            if not date_str:
                if default is not None:
                    return default 
                
                print("Error: This field cannot be empty.")
                continue 

            try:
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                return date_obj.isoformat()
            except ValueError:
                print("Error: Invalid date format. Please use YYYY-MM-DD.")

    @staticmethod
    def get_valid_int(prompt, default=None):
        while True:
            value = input(prompt)
            if not value:
                return default
            try:
                return int(value)
            except ValueError:
                print("Error: Please enter a valid number.")

    @staticmethod
    def get_valid_name(prompt, default=None):
        while True:
            user_input = input(prompt).strip()
            if not user_input:
                if default is not None:
                    return default
                
                print("Error: This field cannot be empty.")
                continue
            
            if user_input.isalpha():
                return user_input
            else:
                print("Error: Name must contain only letters.")
    
    @staticmethod
    def get_valid_ine(prompt, default=None):
        while True:
            ine_input = input(prompt).strip().upper() 
            if not ine_input :
                if default is not None:
                    return default
            elif re.match(r"^[A-Z]{2}[0-9]{5}$", ine_input):
                return ine_input
            else:
                print("Invalid Format exemple : AB12345 .")