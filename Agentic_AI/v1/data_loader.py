import json

from config import WORK_SOURCE_PATH, GAMBLE_SOURCE_PATH, EMOTIONAL_SOURCE_PATH, INVESTMENT_SOURCE_PATH

class data_loader:
    def __init__(self, data_class):
        self.source_paths = {
            'work': WORK_SOURCE_PATH,
            'gamble': GAMBLE_SOURCE_PATH,
            'emotional': EMOTIONAL_SOURCE_PATH,
            'investment': INVESTMENT_SOURCE_PATH
        }
        self.data_class = data_class

    def load(self):
        source_path = self.source_paths.get(self.data_class)
        if not source_path:
            raise ValueError(f"Invalid data class: {self.data_class}")
        with open(source_path, 'r') as f:
            return json.load(f)