import uuid
import shutil
import random
import os
from database import JsonManager
from pathlib import Path


class Player():

    DB_FILE = Path("data") / "players_infos.json"

    def __init__(self, surname, name, birth_date, ine, id=None):
        self.surname = surname
        self.name = name
        self.birth_date = birth_date
        self.ine = ine
        self.id = id if id else str(uuid.uuid4())

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
        return next((p for p in players_list if p.id == id_to_find), None)

    @classmethod
    def get_player_by_ine(cls, ine):
        all_players = cls.get_all_players()
        for player in all_players:
            if player.ine == ine:
                return player
        return None

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
        all_players = self.get_all_players()
        all_players.append(self)
        all_players_dicts = [player.to_dict() for player in all_players]
        JsonManager.save_data(self.DB_FILE, all_players_dicts)

    @classmethod
    def delete_player(cls, target_id):
        all_players_objects = [
            p for p in cls.get_all_players() if p.id != target_id
            ]
        all_players_dicts = [
            player.to_dict() for player in all_players_objects
            ]
        JsonManager.save_data(cls.DB_FILE, all_players_dicts)


class Tournament():
    def __init__(
        self, name, city, total_round, players, description, start_date,
        end_date, current_round=0, finish=False, id=None
    ):
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.city = city
        self.current_round = current_round
        self.total_round = total_round
        self.players = players
        self.description = description
        self.finish = finish
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        tournament_info = {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_round": self.total_round,
            "players": [p.to_dict() for p in self.players],
            "description": self.description,
            "current_round": self.current_round,
            "finish": self.finish
        }
        return tournament_info

    @classmethod
    def from_dict(cls, data):
        players_data = data.get("players", [])

        players_objects = [Player.from_dict(p) for p in players_data]

        return cls(
            id=data["id"],
            name=data["name"],
            city=data["city"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            total_round=data["total_round"],
            players=players_objects,
            description=data["description"],
            current_round=data["current_round"],
            finish=data["finish"]
        )

    @staticmethod
    def get_file_path(tournament_id):
        # Get the path for tournament general info
        file_path = (
            Path("data") / "tournament" / tournament_id /
            "tournament_general_info.json"
        )
        return file_path

    def save_tournament(self):
        # Transform Data
        tournament_data = self.to_dict()
        JsonManager.save_data(
            self.get_file_path(tournament_data['id']), tournament_data
        )

    @staticmethod
    def get_tournaments_id_list():
        tournaments_list = []

        path = Path("data") / "tournament"
        # Get all the round number from folder
        try:
            for file_name in os.listdir(path):
                tournaments_list.append(file_name)

            return tournaments_list

        except FileNotFoundError:
            print("Folder doesn't exist")
            return []

    @classmethod
    def get_tournament_by_id(cls, tournament_id):
        data = JsonManager.load_data(cls.get_file_path(tournament_id))
        return cls.from_dict(data)

    @classmethod
    def get_all_tournaments(cls):
        all_tournament_data_dict = []
        # Get all the tournament Id
        tournaments_name_list = Tournament.get_tournaments_id_list()
        # For each id, load data tournament
        for id in tournaments_name_list:
            tournament_data = JsonManager.load_data(cls.get_file_path(id))
            all_tournament_data_dict.append(tournament_data)
        # Transform into objects
        all_tournament_data_object = [
            cls.from_dict(t) for t in all_tournament_data_dict
        ]
        return all_tournament_data_object

    @classmethod
    def update_tournament(
        cls, tournament_id, new_data_dict, players_data_list
    ):
        tournament = cls.get_tournament_by_id(tournament_id)

        tournament.name = new_data_dict['name']
        tournament.city = new_data_dict['city']
        tournament.start_date = new_data_dict['start_date']
        tournament.end_date = new_data_dict['end_date']
        tournament.total_round = new_data_dict['total_round']
        tournament.description = new_data_dict['description']

        tournament.players = players_data_list

        tournament.save_tournament()

    @classmethod
    def delete_tournament(cls, target_id):

        # Get the file
        path = Path('data') / "tournament" / target_id

        # Delete the id corresponding file
        if os.path.isdir(path):
            shutil.rmtree(path)
            return True
        else:
            return False

    @staticmethod
    def initialize_standings(tournament_id):
        file_path = (
            Path("data") / "tournament" / tournament_id / "standings.json"
        )
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
    def finish_tournament(cls, tournament_id):
        tournament_to_finish = cls.get_tournament_by_id(tournament_id)
        # Update finish attribute
        tournament_to_finish.finish = True
        # Transform into dict and save
        tournament_to_finish.save_tournament()

    @classmethod
    def current_standings(cls, tournament_id):
        path = Path("data") / "tournament" / tournament_id / "standings.json"
        players_dicts = JsonManager.load_data(path)
        players_dicts.sort(key=lambda x: x['score'], reverse=True)
        return players_dicts


class Round:
    def __init__(self, name, start_time, end_time=None, matches=None):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.matches = matches if matches is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [match.to_dict() for match in self.matches]
        }

    @classmethod
    def from_dict(cls, data):
        matches_data = data.get("matches", [])
        matches_objects = [Match.from_dict(m) for m in matches_data]
        return cls(
            name=data['name'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            matches=matches_objects
        )

    @staticmethod
    def get_round_players_list(tournament_id):
        file_path = (
            Path("data") / "tournament" / tournament_id / "standings.json"
        )
        standings_data = JsonManager.load_data(file_path)

        players_list = []

        for player in standings_data:
            id = player['id']
            score = player['score']

            player_obj = Player.get_players_by_id(id)
            # Create score
            player_obj.score = score

            players_list.append(player_obj)

        return players_list

    @classmethod
    def update_standing(cls, tournament_id, player_id, points_to_add):
        file_path = (
            Path("data") / "tournament" / tournament_id / "standings.json"
        )

        if not os.path.exists(file_path):
            return

        standing = JsonManager.load_data(file_path)

        for p in standing:
            if p["id"] == player_id:
                p["score"] += points_to_add
                break

        # Sort ranking
        standing = sorted(standing, key=lambda x: x['score'], reverse=True)
        # Save the data
        JsonManager.save_data(file_path, standing)

    def save_round(self, tournament_id):
        file_path = (
            Path("data") / "tournament" / tournament_id / self.name /
            "Match.json"
        )

        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)

        JsonManager.save_data(file_path, self.to_dict())

    @staticmethod
    def tournament_summary(tournament_id):
        tournament_dir = Path("data") / "tournament" / tournament_id
        if tournament_dir.exists():
            round_folders = [x for x in tournament_dir.iterdir() if x.is_dir()]
        else:
            return []

        round_folders.sort()
        all_rounds_data = []

        for folder in round_folders:
            target_file = folder / "Match.json"
            if target_file.exists():
                data = JsonManager.load_data(target_file)
                match_list = data.get("matches", [])

                round_summary = {
                    "name": folder.name,
                    "match_list": match_list
                }
                all_rounds_data.append(round_summary)
        return all_rounds_data

    @staticmethod
    def get_all_pairs_played(tournament_id):
        summary = Round.tournament_summary(tournament_id)

        pairs_list = []

        for round_data in summary:
            for match in round_data["match_list"]:

                p1 = match[0][0]['id']

                if match[1] and match[1][0]:
                    p2 = match[1][0]['id']
                    pairs_list.append([p1, p2])

        return pairs_list


class Match:
    def __init__(self, player1, player2, score1=0, score2=0):
        self.player1 = player1
        self.player2 = player2
        self.score1 = score1
        self.score2 = score2

    def to_dict(self):
        p1_dict = self.player1.to_dict()
        p2_dict = self.player2.to_dict() if self.player2 else None

        return (
            [p1_dict, self.score1],
            [p2_dict, self.score2]
        )

    @classmethod
    def from_dict(cls, data):

        player1 = Player.from_dict(data[0][0])
        score1 = data[0][1]

        player2 = None
        score2 = 0
        if data[1][0]:
            player2 = Player.from_dict(data[1][0])
            score2 = data[1][1]

        return cls(player1, player2, score1, score2)
