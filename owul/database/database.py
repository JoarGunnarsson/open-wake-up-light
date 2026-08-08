import json
import os.path
import pathlib


class JSONDatabase:
    def __init__(self, path: str):
        self.path = path
        self.db = {}
        self._read()

    def _write(self):
        # Serialise the database to a string first, in case the serialisation fails
        with open(self.path, "w") as f:
            file_contents = json.dumps(self.db)
            f.write(file_contents)

    def _read(self):
        if not os.path.isfile(self.path):
            self._write()
            return
        
        with open(self.path) as f:
            self.db = json.load(f)

    def update(self, key: str, value):
        self.db[key] = value
        self._write()

    def get(self, key: str, default=None):
        return self.db.get(key, default)


PROJECT_DIR = pathlib.Path(__file__).parent
DATABASE_PATH = PROJECT_DIR / "database.json"
database = JSONDatabase(DATABASE_PATH)
