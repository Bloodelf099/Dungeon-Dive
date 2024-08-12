import json
import time
from typing import Tuple

import pygame.key
from scripts.maze_gen.maze import Maze
from scripts.movement.movement import MOVEMENT_KEYS, move


with open(".config.json", "r") as config:
    config = json.load(config)


def handle_input(maze: Maze) -> Tuple[bool, bool] | None:
    keys = pygame.key.get_pressed()
    now = time.time()

    if keys[pygame.K_F10] and maze.end_pos:
        maze.cur_pos = maze.end_pos
        maze.maze[maze.end_pos[0]][maze.end_pos[1]] = "end_True" if maze.level != "Final" else "portal_True"

    if keys[pygame.K_ESCAPE] and maze.level.title() != "Menu":
        maze.key_last_pressed[pygame.K_ESCAPE] = now
        return None

    if keys[pygame.K_m] and now - maze.key_last_pressed.get(pygame.K_m, 0) > config["KEY_COOLDOWN"]:
        pygame.mixer.music.pause() if maze.play_music else pygame.mixer.music.unpause()
        maze.play_music = not maze.play_music
        maze.key_last_pressed[pygame.K_m] = now

    if any((keys[pygame.K_e], keys[pygame.K_RETURN], keys[pygame.K_KP_ENTER])):
        tile = maze.maze[maze.cur_pos[0]][maze.cur_pos[1]]

        match tile:
            case "end_True" | "portal_True":
                pygame.mixer.Sound("assets/sounds/next_level.mp3").play()
                return False, True

            case "start_continue":
                pygame.mixer.Sound("assets/sounds/next_level.mp3").play()
                return None

            case "exit_game":
                return False, False

    for m_key in MOVEMENT_KEYS:
        if keys[m_key]:
            if maze.move_progress >= 1.0:
                move(maze, MOVEMENT_KEYS[m_key])
            break

    return True, True
