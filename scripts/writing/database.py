import json
from typing import Dict


def load_db(path: str) -> Dict[str, float]:
    try:
        with open(path, 'r') as db:
            return json.load(db)

    except FileNotFoundError:
        return {}


def save_db(path: str, data: Dict[str, float]) -> None:
    with open(path, 'w') as db:
        json.dump(data, db, indent=4)
