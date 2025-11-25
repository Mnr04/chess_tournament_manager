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
    def from_dict(cls, data):
        return cls(
            surname=data['surname'],
            name=data['name'],
            birth_date=data['birth_date'],
            ine=data['ine'],
            id=data['id']
        )
    
    @classmethod
    def get_all_players(cls):
        players_data = JsonManager.load_data(cls.DB_FILE)
        players_objects = [cls.from_dict(data) for data in players_data]
        return players_objects
    
    @classmethod
    def get_players_by_id(cls, id_to_find):
        players_list = cls.get_all_players()
        return next((p for p in players_list if p.id == id_to_find),None)

    @classmethod
    def update_players(cls, player_id, player_data):
       all_players = cls.get_all_players()
       player_found = False

       for player in all_players:
           if player.id == player_id:
               
               player.surname = player_data['surname']
               player.name = player_data['name']
               player.birth_date = player_data['birth_date']
               player.ine = player_data['ine']
               
               player_found = True
               break 

       if player_found:
           all_players_dicts = [p.to_dict() for p in all_players]
           
           JsonManager.save_data(cls.DB_FILE, all_players_dicts)
    
    def save_new_player(self):
        all_players_objects = self.get_all_players()
        all_players_objects.append(self)
        all_players_dicts = [player.to_dict() for player in all_players_objects]
        JsonManager.save_data(self.DB_FILE, all_players_dicts)
  
    @classmethod
    def delete_player(cls, target_id):
       all_players_objects = [p for p in cls.get_all_players() if p.id != target_id]
       all_players_dicts = [player.to_dict() for player in all_players_objects]
       JsonManager.save_data(cls.DB_FILE, all_players_dicts)

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
            "players": [p.to_dict() for p in self.players],
            "description": self.description,
            "actual_round": self.actual_round,
            "finish": self.finish
        }
        return tournois_info
    
    @classmethod
    def from_dict(cls, data):
        players_data = data.get("players", [])
        
        players_objects = [Player.from_dict(p) for p in players_data]

        return cls(
            id = data["id"],
            name = data["name"],
            city = data["city"],
            start_date = data["start_date"],
            end_date = data["end_date"],
            total_round  = data["total_round"],
            players = players_objects,
            description = data["description"],
            actual_round = data["actual_round"],
            finish = data["finish"]
        )
    
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
        data = JsonManager.load_data(cls.get_file_path(tournament_id))
        return cls.from_dict(data)
       
    @classmethod
    def get_all_tournement(cls):
        all_tournament_data_dict = []
        # Get all the tournament Id
        tournaments_name_list = Tournament.get_tournaments_id_list()
        # For each id , load data tournament
        for id in tournaments_name_list:
            tournament_data = JsonManager.load_data(cls.get_file_path(id))
            all_tournament_data_dict.append(tournament_data)
        #Transform into objects
        all_tournament_data_object = [cls.from_dict(t)  for t in all_tournament_data_dict]
        return all_tournament_data_object

    @classmethod
    def update_tournament(cls, tournament_id, new_data_dict, players_data_list):
       tournament = cls.get_tournament_by_id(tournament_id)
       
       tournament.name = new_data_dict['name']
       tournament.city = new_data_dict['city']
       tournament.start_date = new_data_dict['start_date']
       tournament.end_date = new_data_dict['end_date']
       tournament.total_round = new_data_dict['total_round']
       tournament.description = new_data_dict['description']

        #Players a gerer
        #Save
       tournament.save_tournament()
       
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
        tournament_to_start.actual_round += 1
        # Transform and save
        tournament_to_start.save_tournament()
        

    @staticmethod
    def initialize_standings(tournament_id):
        
        file_path = Path("data") /"tournament"/ tournament_id/ "standings.json"
        if os.path.exists(file_path):
            return
        # Get tournament info from id
        tournament_data = Tournament.get_tournament_by_id(tournament_id)
        # Create players list from tournament_data
        player_list = [
            {"name": p.name, "surname": p.surname, "id": p.id, "score": 0} 
            for p in tournament_data.players
            ]
        # Shuffle player list
        random.shuffle(player_list)
        JsonManager.save_data(file_path, player_list)

    @classmethod
    def finish_tournament(cls , tournament_id):
        tournament_to_finish = cls.get_tournament_by_id(tournament_id)
        # Update finish attribute
        tournament_to_finish.finish = True
        #Transform into dict and save
        tournament_to_finish.save_tournament()

class Round():
    @classmethod
    def create_round(cls, round_number, tournament_id):
        #Create match list file + round folder
        round_number = str(round_number)
        file_path = Path("data") / "tournament" / tournament_id /f"Round_{round_number}"/ "Match.json"
        directory_to_create = os.path.dirname(file_path)
        os.makedirs(directory_to_create, exist_ok=True)

    def get_round_players_list(tournament_id):
        file_path = Path("data") / "tournament" /tournament_id /"Ranking.json"
        return JsonManager.load_data(file_path)
        
    def update_match_list(tournament_id, match_list,round_number):
        file_path = Path("data") /  "tournament" /tournament_id / f"Round_{round_number}" /"Match.json"
        JsonManager.save_data(file_path, match_list)

    @classmethod
    def update_standing(cls, tournament_id, player_id, points_to_add):
        file_path = Path("data") / "tournament" / tournament_id / "standings.json"

        if not os.path.exists(file_path):
            return 

        standing = JsonManager.load_data(file_path)

        for p in standing:
            if p["id"] == player_id: 
                p["score"] += points_to_add
                break
        
        #Sort ranking
        standing = sorted(standing, key=lambda x: x['score'], reverse=True)
        # Save the data 
        JsonManager.save_data(file_path, standing)

    def start_time_round(round_number, tournament_id):
        file_path = Path("data") / "tournament" / tournament_id / f"Round_{round_number}" /"time.json"

        # Get the time data
        start_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        time = {
            'start_time' : start_timestamp,
            'end_time' : ""
        }

        JsonManager.save_data(file_path, time)
    
    def end_time_round(round_number, tournament_id): 
        file_path = Path("data") / "tournament" / tournament_id / f"Round_{round_number}" /"time.json"
    
        try:
            data = JsonManager.load_data(file_path)
        except FileNotFoundError:
            print(f"Error {round_number} not exists ")
            return

        end_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        data['end_time'] = end_timestamp 

        JsonManager.save_data(file_path, data)

    def tournament_summary(tournament_id):
        # Build the path to the tournament directory
        tournament_dir = Path("data") / "tournament" / tournament_id
    
        # Retrieve all sub-folders if the directory exists
        if tournament_dir.exists():
            round_folders = [x for x in tournament_dir.iterdir() if x.is_dir()]
        else:
            round_folders = []

        # Sort folders 
        round_folders.sort()
        
        all_rounds_data = []

        # 4. Loop in each round folder
        for folder in round_folders:
            target_file = folder / "Match.json" 

            if target_file.exists():
                # Load match data using the DAO
                data = JsonManager.load_data(target_file)
                
                # Extract JUST the folder name (e.g., "Round_1") from the full path
                current_round_name = folder.name 
       
                # Structure data for the report
                round_summary = {
                    "name": current_round_name, 
                    "match_list": data      
                }

                all_rounds_data.append(round_summary)
            else:
                print(f"No {folder.name}")
        
        return all_rounds_data

    @staticmethod
    def get_all_pairs_played(tournament_id):
        summary = Round.tournament_summary(tournament_id)
        
        pairs_list = []
        
        for round_data in summary:
            for match in round_data["match_list"]:
                p1 = match[0]['id'] 
                if match[1]:
                    p2 = match[1]['id']
                    pairs_list.append([p1, p2])
                    
        return pairs_list