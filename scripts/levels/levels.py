from typing import Dict

levels: Dict[str, Dict] = {
    "menu": {
        "shape": [
            [True, True, True, True, True, True, True, True, ],
            [True, True, True, False, False, False, "start_continue", True, ],
            [True, False, False, False, True, True, True, True],
            [True, True, True, False, False, False, "exit_game", True, ],
            [True, True, True, True, True, True, True, True],
        ],

        "start": (2, 1),
        "end": None
    },

    "ending": {
        "shape": [
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
            [True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, True],
            [True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, True, True, True, False, True, False, True, False, True],
            [True, False, False, False, False, False, True, False, False, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
            [True, True, True, True, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
            [True, False, False, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, False, False, True, False, True, False, True],
            [True, False, True, True, True, False, True, False, True, False, True, False, True, False, True, False, True, True, True, False, True, False, True, False, True],
            [True, False, False, False, False, False, False, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
            [True, True, True, True, True, False, True, True, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
            [True, False, False, False, False, False, True, False, False, False, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
            [True, True, True, True, True, False, True, False, True, True, True, False, True, False, True, False, True, False, True, False, True, False, True, False, True],
            [True, False, False, False, False, False, True, False, False, False, False, False, True, False, True, False, True, False, True, False, False, False, True, False, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, True, False, True, True, True, False, True],
            [True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, False, True, False, True, False, True],
            [True, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, True, False, True, False, True],
            [True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True],
            [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
        ],
        "start": (5, 3),
        "end": (13, 21),

        "villagers": {
            (1, 1): 5,
            (3, 1): 1,
            (9, 1): 2,
            (11, 1): 3,
            (3, 17): 4,
            (7, 17): 0,
            (11, 23): 8
        }
    }
}
