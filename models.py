import json
import uuid
import os

class Player():
    def __init__(self, surname, name, age, ine):
        self.surname = surname
        self.name = name
        self.age = age
        self.ine = ine
        self.id = None 

    def get_all_players():
        file_path = os.path.join("data", "players_infos.json")

        try : 
            with open (file_path , "r") as file:
                return json.load(file)
        except (FileNotFoundError ,json.JSONDecodeError):   
            return []
    
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
               player["age"] = player_data['age']
               player["ine"] = player_data['ine']
               player_found = True
               break 

       if player_found:
           file_path = os.path.join('data', "players_infos.json")
           with open(file_path, "w") as file:
                json.dump(all_players, file, indent=2)
    

    def save_new_player(self):
        file_path = os.path.join('data', "players_infos.json")

        #Verify if exists
        os.makedirs("data", exist_ok=True)

        #Loads all players
        try : 
            all_players = []
            with open (file_path , "r") as file:
                all_players = json.load(file)
        except:
            all_players = []

        #Create new player 
        new_player = {
            "id" : str(uuid.uuid4()),
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "ine": self.ine
        }

        all_players.append(new_player)

        #Modify the json files
        with open(file_path, "w") as file:
            json.dump(all_players, file, indent=2)

    @classmethod
    def delete_player(cls, target_id):
       all_players = [p for p in cls.get_all_players() if p['id'] != target_id]
       file_path = os.path.join('data', "players_infos.json")
       with open(file_path, "w") as file:
            json.dump(all_players, file, indent=2)

class Tournament():
    def __init__(self, name, city, date, tournament_tour_number, registred_player, description):
        self.name = name
        self.city = city
        self.date = date
        self.tournament_tour_number = tournament_tour_number
        self.registred_player = registred_player
        self.description = description
        pass

    def create_tournament(self):
        tournois_info = {
            "Name" : self.name,
            "City" : self.city,
            "Date": self.date,
            "Total_tour_number": self.tournament_tour_number,
            "Players": self.registred_player,
            "Description": self.description
        }
        directory = "data"
        tournament_name = self.name
        file_path = os.path.join(directory, "tournament", tournament_name, "info.json")
        directory_to_create = os.path.dirname(file_path)
        os.makedirs(directory_to_create, exist_ok=True)

        with open(file_path, "w") as file:
            json.dump(tournois_info, file, indent=2)
        
    def get_all_tournaments():
        tournaments_list = []
        directory = "data"

        directory_path = os.path.join(directory, "tournament")
        
        try:
            for file_name in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file_name)
                tournaments_list.append(file_name)
            
            return tournaments_list

        except FileNotFoundError:
            print("Folder don't exist")
            return []


class Round():
    pass
class Match():
    def __init__(self):
        pass


