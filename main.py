import json
import sys
from typing import Dict, List

import pygame

from scripts.asset_loader.asset_loader import load_paths
from scripts.events.event_handler import handle_position, handle_events
from scripts.events.input_handler import handle_input
from scripts.maze_gen.maze import Maze
from scripts.movement.movement import calculate_interpolated_position
from scripts.rendering.rendering import draw_maze, calculate_move_progress, sprite_picker, \
    draw, update_window_title, draw_villagers, recalculate_sizes
from scripts.writing.database import load_db, save_db

with open(".config.json", "r", encoding="UTF-8") as file:
    config: Dict = json.load(file)


def main():
    pygame.init()
    pygame.mixer.init()

    paths = load_paths("assets")

    pygame.mixer.music.load("assets/sounds/music/music2.mp3")
    pygame.display.set_icon(pygame.image.load("assets/textures/icon.png"))
    pygame.mixer.music.play(loops=-1)

    window_size = 800, 600
    window = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    clock = pygame.time.Clock()

    menu_level = None
    # Current, Menu
    levels = [None, None]
    loaded_levels: List[Maze] = []

    next_level = True
    i = 0
    for i, (level, values) in enumerate(config["LEVELS"].items()):
        if not next_level:
            break

        current_maze = Maze.get_maze(level, **values)
        if len(loaded_levels) > 1:
            current_maze.play_music = loaded_levels[-1].play_music

        loaded_levels.append(current_maze)

        if level == "Menu":
            menu_level = current_maze
            levels[1] = current_maze

        else:
            levels[0] = current_maze

        cell_size, offset, images = recalculate_sizes(window_size, current_maze.size, paths["textures"])

        window.fill(0)
        update_window_title(level)

        running = True
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                        next_level = False

                    case pygame.VIDEORESIZE:
                        window_size = event.size
                        window = pygame.display.set_mode(window_size, pygame.RESIZABLE)

                        cell_size, offset, images = recalculate_sizes(window_size, current_maze.size, paths["textures"])

            if not running:
                break

            result = handle_input(current_maze)
            if result is not None:
                running, next_level = handle_input(current_maze)

            else:
                if levels[0] is None:
                    running = False
                    continue

                current_maze = levels[1]
                levels[0], levels[1] = levels[1], levels[0]

                if current_maze is menu_level:
                    current_maze.cur_pos = current_maze.start_pos
                    current_maze.move_progress = 1.0

                window.fill(0)
                cell_size, offset, images = recalculate_sizes(window_size, current_maze.size, paths["textures"])

                update_window_title(current_maze.level)
                continue

            handle_events(current_maze)
            handle_position(current_maze)

            if current_maze.move_progress >= 1:
                render_pos = current_maze.last_pos = current_maze.cur_pos
                current_player_sprite = images["player"]["idle"]

            else:
                current_maze.move_progress = calculate_move_progress(
                    current_maze.move_progress, clock.get_time(), config["MOVE_SPEED"]
                )

                render_pos = calculate_interpolated_position(
                    current_maze.last_pos, current_maze.cur_pos, current_maze.move_progress
                )

                current_player_sprite = sprite_picker(
                    list(images["player"]["walk"]["3"].values()), current_maze.move_progress
                )

            draw_maze(
                maze=current_maze,
                window=window,
                cells=images["cells"],
                cell_size=cell_size,
                offset=offset
            )

            if current_maze.villagers:
                draw_villagers(
                    window=window,
                    sprites=list(images["villagers" if level != "Final" else "ending_villagers"].values()),
                    villagers=current_maze.villagers,
                    cell_size=cell_size,
                    offset=offset
                )

            draw(
                window,
                offset,
                cell_size,

                # Player
                (render_pos, current_player_sprite, current_maze.flip),
            )

            current_maze.frames_inside += 1
            pygame.display.flip()
            clock.tick(config["FPS"])

    pygame.mixer.quit()
    pygame.display.quit()

    if i > 1:
        db = load_db("database.json")

        nome = input("Digite seu Nome: ")
        final_time = sum(level.frames_inside for level in loaded_levels if level is not menu_level) / config["FPS"]

        db[nome] = final_time
        db["finalizou"] = i+1 == len(config["LEVELS"])

        save_db("database.json", db)

    sys.exit()


if __name__ == '__main__':
    main()
