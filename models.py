import json
import shortuuid
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
            "id" : shortuuid.uuid(),
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

    def __init__(self, name, city, total_round, players, description):

        # statemapping(0:"not_start", 1="in_progress", 2="finish")
        self.id = shortuuid.uuid()
        self.name = name
        self.city = city
        self.start = "Not Start"
        self.end = "Not Finish"
        self.actual_round = 0
        self.total_round = total_round
        self.players = players
        self.description = description
        pass

    def tournament_to_dict(self):
        tournois_info = {
            "id" : self.id,
            "Name" : self.name,
            "City" : self.city,
            "Total_round": self.total_round,
            "Players": self.players,
            "Description": self.description,
        }
        return tournois_info
        
    def save_tournament(self):
        #on recupere les donné 
        tournament_data = self.tournament_to_dict()

        directory = "data"
        file_path = os.path.join(directory, "tournament", self.id, "info.json")
        directory_to_create = os.path.dirname(file_path)
        os.makedirs(directory_to_create, exist_ok=True)

        with open(file_path, "w") as file:
            json.dump(tournament_data, file, indent=2)
    
    def get_tournaments_id_list():
        tournaments_list = []
        directory = "data"

        directory_path = os.path.join(directory, "tournament")
        
        try:
            for file_name in os.listdir(directory_path):
                #file_path = os.path.join(directory_path, file_name)
                tournaments_list.append(file_name)
            
            return tournaments_list

        except FileNotFoundError:
            print("Folder don't exist")
            return []
        
    @classmethod
    def get_tournament_by_id(cls, tournament_id):
        file_path = os.path.join('data', 'tournament', tournament_id, "info.json")
        with open(file_path, "r") as file:
            tournament_data = json.load(file)
    
        return tournament_data
    
    def get_all_tournement_info():
        all_tournament_data = []

        tournaments_name_list = Tournament.get_tournaments_id_list()
        for id in tournaments_name_list:
            file_path = os.path.join('data', 'tournament', id, "info.json")
            with open(file_path, "r") as file:
                tournament_data = json.load(file)
                all_tournament_data.append(tournament_data)

        return all_tournament_data

    @classmethod
    def update_tournament(cls, tournament_id, new_tournament_data, players_data):
       actual_tournement_data = cls.get_tournament_by_id(tournament_id)

       actual_tournement_data["Name"] = new_tournament_data['Name']
       actual_tournement_data["City"] = new_tournament_data['City']
       actual_tournement_data["Total_round"] = new_tournament_data['Total_round']
       actual_tournement_data["Description"] = new_tournament_data['Description']
       actual_tournement_data["Players"] = players_data
              
      
       file_path = os.path.join('data', 'tournament', actual_tournement_data["id"], "info.json")
       with open(file_path, "w") as file:
            json.dump(actual_tournement_data, file, indent=2)



class Round():
    pass
class Match():
    def __init__(self):
        pass

