import json

class ConfigLoader:
    @staticmethod
    def load_settings(file_path="../infra/config.json"):  # Updated line
        """Loads configuration settings from a JSON file."""
        with open(file_path, 'r') as file:
            return json.load(file)
