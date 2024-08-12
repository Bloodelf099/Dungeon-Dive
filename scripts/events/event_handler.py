import json
from typing import Optional

import pygame

from scripts.maze_gen.maze import Maze

with open(".config.json", "r") as config:
    config = json.load(config)


def _handle_traps(maze: Maze, cooldown: Optional[float], duration: Optional[float]) -> None:
    maze.traps[0] += 1

    if (
            (not maze.traps[1] and maze.traps[0] % (cooldown*config["FPS"]) == 0) or
            (maze.traps[1] and maze.traps[0] % (duration*config["FPS"]) == 0)
    ):
        maze.traps[0] = 0
        maze.traps[1] = not maze.traps[1]

        for px, py in maze.traps[2]:
            maze.maze[px][py] = f"trap_{maze.traps[1]}"

        pygame.mixer.Sound("assets/sounds/spike.mp3").play()


def handle_events(maze: Maze) -> None:
    if maze.traps is not None:
        _handle_traps(maze, *maze.traps_info)


def handle_position(maze: Maze):
    px, py = maze.cur_pos
    tile = maze.maze[px][py]

    if isinstance(tile, str) and tile.startswith("trap") and maze.traps[1]:
        maze.move_progress = 0.0
        maze.cur_pos = maze.checkpoint_pos
        pygame.mixer.Sound("assets/sounds/hurt.mp3").play()

    if maze.villagers and maze.move_progress >= 0.5 and (px, py) in maze.villagers:
        maze.villagers.pop((px, py))
        maze.checkpoint_pos = px, py

        pygame.mixer.Sound("assets/sounds/collect.wav").play()

        if not maze.villagers:
            maze.maze[maze.end_pos[0]][maze.end_pos[1]] = "end_True" if maze.level != "Final" else "portal_True"
            pygame.mixer.Sound("assets/sounds/door2.mp3").play()
