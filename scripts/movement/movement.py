from typing import Tuple, Literal, Dict

import pygame

from scripts.maze_gen.maze import Maze

Direction = Tuple[int, int]
DirectionName = Literal["up", "down", "right", "left"]
Directions: Dict[DirectionName, Direction] = {
    "up": (-1, 0),
    "down": (1, 0),
    "right": (0, 1),
    "left": (0, -1)
}

MOVEMENT_KEYS = {
    pygame.K_UP: Directions["up"],
    pygame.K_w: Directions["up"],

    pygame.K_DOWN: Directions["down"],
    pygame.K_s: Directions["down"],

    pygame.K_LEFT: Directions["left"],
    pygame.K_a: Directions["left"],

    pygame.K_RIGHT: Directions["right"],
    pygame.K_d: Directions["right"],
}


def move(maze: Maze, direction: Tuple[int, int]) -> None:
    nx, ny = maze.cur_pos[0] + direction[0], maze.cur_pos[1] + direction[1]
    if direction == Directions["left"]:
        maze.flip = False

    elif direction == Directions["right"]:
        maze.flip = True

    if maze.maze[nx][ny] is True:
        return

    maze.move_progress = 0.0
    maze.last_pos = maze.cur_pos
    maze.cur_pos = nx, ny


def calculate_interpolated_position(
        start_pos: Tuple[int, int],
        cur_pos: Tuple[int, int],
        progress: float
) -> Tuple[float, float]:
    px = start_pos[0] + (cur_pos[0] - start_pos[0]) * progress
    py = start_pos[1] + (cur_pos[1] - start_pos[1]) * progress

    return px, py
