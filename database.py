import json
import os


class JsonManager:
    @staticmethod
    def load_data(file_path):
        """
        Loads data from a JSON file.

        Args:
            file_path: The path to the JSON file.

        Returns:
            list or dict: The data loaded from the file.
        """
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError):
            return []

    @staticmethod
    def save_data(file_path, data):
        """
        Saves data to a JSON file. Creates the directory if it doesn't exist.

        Args:
            file_path (str or Path): The destination path.
            data (list or dict): The data to serialize and save.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)
