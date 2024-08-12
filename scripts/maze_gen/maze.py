import math
import random
from itertools import cycle
from typing import List, Tuple, Optional, Dict, Self, Final, Literal

from scripts.levels.levels import levels
from scripts.maze_gen.maze_gen import MazeStructure, Coord, gen_maze, random_pos, setup_positions


class Maze:
    def __init__(self, maze: MazeStructure, start_pos: Coord, end_pos: Optional[Coord], level_name: str):
        assert maze is not None, "maze is None"

        self.level: str = level_name

        self.maze: Final[MazeStructure] = maze
        self.size: Final[Tuple[int, int]] = (len(maze), len(maze[0]))

        self.start_pos: Final[Coord] = start_pos
        self.end_pos: Final[Optional[Coord]] = end_pos

        self.cur_pos: Coord = start_pos
        self.last_pos: Coord = start_pos
        self.checkpoint_pos: Coord = start_pos

        self.move_progress: float = 1.0

        self.flip: bool = self.maze[start_pos[0]][start_pos[1] + 1] is not True

        self.maze[start_pos[0]][start_pos[1]] = "start"

        if end_pos is not None:
            self.maze[end_pos[0]][end_pos[1]] = "end_False" if self.level != "Final" else "portal_False"

        self.dead_ends: Optional[List[Coord]] = None

        self.traps: Optional[List[int, bool, List[Coord]]] = None
        self.traps_info: Optional[Tuple[float, float]] = None
        self.villagers: Optional[Dict[Coord, int]] = None

        self.key_last_pressed: Dict[int, float] = {}

        self.play_music: bool = True

        self.frames_inside: int = 0

    @classmethod
    def get_maze(
            cls,
            level_name: str,
            maze: str | None = None,
            *,
            dimensions: Optional[Tuple[int, int]] = None,
            traps: Optional[Dict[Literal["random", "cooldown", "duration"], float]] = None,
            villagers: Optional[Dict[Literal["percentage"], float]] = None,
            end_is_portal: bool = False
    ) -> Self:
        if maze in levels:
            maze_structure = levels[maze]["shape"]
            start = levels[maze]["start"]
            end = levels[maze]["end"]
            maze_villagers = levels[maze].get("villagers", None)
            dead_ends = None

        else:
            maze_structure = gen_maze(*dimensions, start=random_pos(*dimensions))
            start, end, dead_ends = setup_positions(maze_structure)
            maze_villagers = None

        final_maze = cls(
            maze=maze_structure,
            start_pos=start,
            end_pos=end,
            level_name=level_name
        )

        final_maze.dead_ends = dead_ends

        if villagers is None and end is not None:
            maze_structure[end[0]][end[1]] = "end_True" if not end_is_portal else "portal_True"

        elif isinstance(villagers, dict):
            if villagers.get("random", True):
                final_maze.setup_villagers(villagers["percentage"], 7)

            else:
                final_maze.villagers = maze_villagers

        if traps is not None:
            if traps.get("random", True):
                final_maze.setup_traps(*[5, 7])

            final_maze.traps_info = traps["cooldown"], traps["duration"]

        return final_maze

    def setup_traps(self, spacing_min: int, spacing_max: int):
        def random_spacing(a: int, b: int):
            return random.randint(a, b)

        self.traps = [0, False, []]

        i = 0
        spacing = random_spacing(spacing_min, spacing_max)

        for x, row in enumerate(self.maze):
            for y, tile in enumerate(row):
                if tile is False:
                    if self.villagers and (x, y) in self.villagers:
                        continue

                    i += 1
                    if i % spacing == 0:
                        self.maze[x][y] = "trap_False"
                        self.traps[2].append((x, y))
                        spacing = random_spacing(spacing_min, spacing_max)

    def setup_villagers(self, pct: float, sprites_amount: int):
        length = len(self.dead_ends)
        amount = max(1, math.floor(length * pct))

        if not length or amount > length:
            self.villagers = None
            self.maze[self.end_pos[0]][self.end_pos[1]] = "end_True" if self.level != "ending" else "portal_True"
            return

        villagers_sprites_indexes = list(range(sprites_amount))
        random.shuffle(villagers_sprites_indexes)

        do_spawn_list = [True] * amount + [False] * (length - amount)
        random.shuffle(do_spawn_list)

        villagers: Dict[Coord, int] = {
            coord: sprite_index
            for coord, sprite_index, do_spawn
            in zip(self.dead_ends, cycle(villagers_sprites_indexes), do_spawn_list)
            if do_spawn
        }

        self.villagers = villagers
