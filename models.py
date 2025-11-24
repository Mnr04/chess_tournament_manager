import shortuuid
import shutil
import random
import datetime
from database import JsonManager
from pathlib import Path
import os
import json

class Player():

    DB_FILE = Path("data") / "players_infos.json"

    def __init__(self, surname, name, birth_date, ine, id=None):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.ine = ine
        self.id = id if id else shortuuid.uuid()

    def to_dict(self):
        return {
            "id": self.id,  
            "name": self.name,
            "surname": self.surname,
            "birth_date": self.birth_date,
            "ine": self.ine
        }
    
    @classmethod
    def get_all_players(cls):
        return JsonManager.load_data(cls.DB_FILE)
    
    @classmethod
    def get_players_by_id(cls, id_to_find):
        players_list = cls.get_all_players()
        return next((p for p in players_list if p["id"] == id_to_find),None)

    @classmethod
    def update_players(cls, player_id, player_data):
       all_players = cls.get_all_players()
       player_found = False

       for player in all_players:
           if player['id'] == player_id:
               player["surname"] = player_data['surname']
               player["name"] = player_data['name']
               player["birth_date"] = player_data['birth_date']
               player["ine"] = player_data['ine']
               player_found = True
               break 

       if player_found:
           JsonManager.save_data(cls.DB_FILE, all_players)
    
    def save_new_player(self):
        all_players = JsonManager.load_data(self.DB_FILE)
        new_player_data = self.to_dict()
        all_players.append(new_player_data)
        JsonManager.save_data(self.DB_FILE, all_players)
  
    @classmethod
    def delete_player(cls, target_id):
       all_players = [p for p in cls.get_all_players() if p['id'] != target_id]
       JsonManager.save_data(cls.DB_FILE, all_players)

class Tournament():

    def __init__(self, name, city, total_round, players, description, start_date, end_date, id=None):
        self.id = id if id else shortuuid.uuid()
        self.name = name
        self.city = city
        self.actual_round = 0
        self.total_round = total_round
        self.players = players
        self.description = description
        self.finish = False
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        tournois_info = {
            "id" : self.id,
            "name" : self.name,
            "city" : self.city,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_round": self.total_round,
            "players": self.players,
            "description": self.description,
            "actual_round": self.actual_round,
            "finish": self.finish
        }
        return tournois_info
    
    @staticmethod
    def get_file_path(tournament_id):
        # Get the path for tournament general info
        file_path = Path("data") / "tournament" /tournament_id /"tournament_general_info.json"
        return file_path
 
    def save_tournament(self):
        # Transform Data  
        tournament_data = self.to_dict()
        # Save with JsonManager
        JsonManager.save_data(self.get_file_path(tournament_data['id']), tournament_data)

    @staticmethod  
    def get_tournaments_id_list():
        tournaments_list = []

        path = Path("data") /  "tournament"
        # Get all the round number from folder
        try:
            for file_name in os.listdir(path):
                tournaments_list.append(file_name)
            
            return tournaments_list

        except FileNotFoundError:
            print("Folder don't exist")
            return []
        
    @classmethod
    def get_tournament_by_id(cls, tournament_id):
        # Get tournament info from id 
        return JsonManager.load_data(cls.get_file_path(tournament_id))
    
    @classmethod
    def get_all_tournement(cls):
        all_tournament_data = []
        # Get all the tournament Id
        tournaments_name_list = Tournament.get_tournaments_id_list()
        # For each id , load data tournament
        for id in tournaments_name_list:
            tournament_data = JsonManager.load_data(cls.get_file_path(id))
            all_tournament_data.append(tournament_data)
        return all_tournament_data

    @classmethod
    def update_tournament(cls, tournament_id, new_tournament_data, players_data):
       # Get tournament info from his Id
       actual_tournement_data = cls.get_tournament_by_id(tournament_id)
       # Update dictionnary with new value
       actual_tournement_data.update(new_tournament_data)
       # Update player list 
       actual_tournement_data["players"] = players_data
       # Save new data
       JsonManager.save_data(cls.get_file_path(actual_tournement_data['id']), actual_tournement_data)

    @classmethod
    def delete_tournament(cls, target_id):

        # Get the file 
        path = Path('data') / "tournament" / target_id

        # Delete the id corresponding file
        if os.path.isdir(path):
            shutil.rmtree(path)
            return True
        else :
            return False

    @classmethod     
    def update_tournament_actual_round(cls , tournament_id):
        # Get tournament info from id
        tournament_to_start = cls.get_tournament_by_id(tournament_id)
        # Update tournament actual round
        tournament_to_start["actual_round"] += 1
        # Save new data
        JsonManager.save_data(cls.get_file_path(tournament_to_start['id']), tournament_to_start)

    @staticmethod
    def initialize_standings(tournament_id):
        
        file_path = Path("data") /"tournament"/ tournament_id/ "standings.json"
        if os.path.exists(file_path):
            return
        # Get tournament info from id
        tournament_data = Tournament.get_tournament_by_id(tournament_id)
        # Create players list from tournament_data
        player_list = [
            {"name": p[0], "surname": p[1], "id": p[2], "score": 0} 
            for p in tournament_data["players"]
            ]
        # Shuffle player list
        random.shuffle(player_list)
        JsonManager.save_data(file_path, player_list)

    @classmethod
    def finish_tournament(cls , tournament_id):
        tournament_to_finish = cls.get_tournament_by_id(tournament_id)
        # Update finish attribute
        tournament_to_finish["finish"] = True
        JsonManager.save_data(cls.get_file_path(tournament_to_finish['id']), tournament_to_finish)

class Round():
    @classmethod
    def create_round(cls, round_number, tournament_id):
        #Create match list file + round folder
        round_number = str(round_number)
        file_path = os.path.join("data", "tournament", tournament_id, f"Round_{round_number}", "Match.json")
        directory_to_create = os.path.dirname(file_path)
        os.makedirs(directory_to_create, exist_ok=True)

    def get_round_players_list(tournament_id):
        file_path = os.path.join("data", "tournament", tournament_id, "Ranking.json")
        with open(file_path, "r") as file:
            player_list_sort = json.load(file)
        return player_list_sort
    
    def create_match_list(player_list, tournament_id, round_number):
        match_list = []
        
        for i in range(0, len(player_list), 2):
            
            player_1 = player_list[i]
            player_2 = player_list[i + 1]

            match_player_1 = [player_1["Id"], player_1["Name"], player_1["Surname"], 0]
            match_player_2 = [player_2["Id"], player_2["Name"], player_2["Surname"], 0]

            match = (match_player_1, match_player_2)
            #on creer un fichier AllMatchList 
            #pour chaque match quon creer on verifie si il a pas etais joué sinon on lui donne le joueur d'aprés
            
            match_list.append(match)

            directory = "data"
            file_path = os.path.join(directory, "tournament", tournament_id, f"Round_{round_number}", "Match.json")

        with open(file_path , "w") as file :
            json.dump(match_list, file, indent=2)
            
        return match_list

    def update_match_list(tournament_id, match_list,round_number):
        directory = "data"
        file_path = os.path.join(directory, "tournament", tournament_id, f"Round_{round_number}", "Match.json")

        with open(file_path , "w") as file :
                json.dump(match_list, file, indent=2)

    @classmethod
    def update_ranking(cls, tournament_id, player_id, points_to_add):
        directory = "data"
        file_path = os.path.join(directory, "tournament", tournament_id, "Ranking.json")

        if not os.path.exists(file_path):
            return 

        with open(file_path, "r") as file:
            ranking = json.load(file)

        for p in ranking:
            if p["Id"] == player_id: 
                p["Score"] += points_to_add
                break
        
        #on met a jour le classement 
        ranking = sorted(ranking, key=lambda x: x['Score'], reverse=True)
                
        with open(file_path, "w") as file:
            json.dump(ranking, file, indent=2)

    def start_time_round(round_number, tournament_id):
        #On creer un fichier time.json avec un dictionnaire startTour : et endTour: 
        file_path = os.path.join("data", "tournament", tournament_id, f"Round_{round_number}", "time.json")
        directory_to_create = os.path.dirname(file_path)
        os.makedirs(directory_to_create, exist_ok=True)
        #la on prend le datetime now au moment ou on lance
        start_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        time = {
            'start_time' : start_timestamp,
            'end_time' : ""
        }

        # et le end time pareil
        with open(file_path, "w") as file:
            json.dump(time, file, indent=2)
    
    def end_time_round(round_number, tournament_id): 
        file_path = Path("data") / "tournament" / tournament_id / f"Round_{round_number}" /"time.json"
    
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(f"Erreur  {round_number} n")
            return

        end_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        data['end_time'] = end_timestamp 

        with open(file_path, "w") as file:
            json.dump(data, file, indent=2)

    def tournament_summary(tournament_id):
        #on veut tout les folder enfant a ca 
        tournament_dir = Path("data") / "tournament" / tournament_id
        if tournament_dir.exists():
            round_folders = [x for x in tournament_dir.iterdir() if x.is_dir()]
        else:
            round_folders = []
        #pour chaque folder on charge les matchs 
        round_folders.sort()
        all_rounds_data = []

        for folder in round_folders:
            target_file = folder / "Match.json" 

            if target_file.exists():
                with open(target_file, "r") as file:
                    data = json.load(file)
                    current_round_name = folder.name 
       
                    round_summary = {
                        "name": current_round_name, 
                        "match_list": data      
                    }

                    all_rounds_data.append(round_summary)
            else:
                print(f"No {folder.name}")
        
        return all_rounds_data
