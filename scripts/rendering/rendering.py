from typing import Optional, Tuple, List, Dict

import pygame

from scripts.asset_loader.asset_loader import ImagePaths, load_images
from scripts.maze_gen.maze_gen import Coord
from scripts.maze_gen.maze import Maze


def draw_maze(
        maze: Maze,
        window: pygame.Surface,
        cells: ImagePaths,
        cell_size: int,
        offset: Coord,
) -> None:
    offset_x, offset_y = offset
    for i, row in enumerate(maze.maze):
        py = i * cell_size + offset_y
        for j, col in enumerate(row):
            px = j * cell_size + offset_x

            tile = maze.maze[i][j]
            if isinstance(tile, bool):
                tile = "wall" if tile else "floor"

            window.blit(cells[tile], (px, py))


def update_tile(
        maze: Maze,
        window: pygame.Surface,
        cells: ImagePaths,
        cell_size: int,
        offset: Coord,
        *,
        before: Optional[Coord] = None,
        after: Coord
):
    offset_x, offset_y = offset
    apx = offset_y + after[0] * cell_size
    apy = offset_x + after[1] * cell_size

    tile = maze.maze[after[0]][after[1]]

    if isinstance(tile, bool):
        tile = "wall" if maze.maze[after[0]][after[1]] else "floor"

    window.blit(cells[tile], (apy, apx))

    if before:
        update_tile(maze, window, cells, cell_size, offset, after=before)


def calculate_maze_dimensions(window_size: Tuple[int, int], maze_size: Tuple[int, int]) -> Tuple[int, Tuple[int, int]]:
    width, height = window_size
    cell_size = min(width // maze_size[1], height // maze_size[0])
    maze_width = maze_size[1] * cell_size
    maze_height = maze_size[0] * cell_size
    offset_x = (width - maze_width) // 2
    offset_y = (height - maze_height) // 2
    return cell_size, (offset_x, offset_y)


def sprite_picker(sprites: List[pygame.Surface], progress: float) -> pygame.Surface:
    i = int(round(progress * (len(sprites)-1)))
    return sprites[i]


def draw_villagers(
        window: pygame.Surface,
        sprites: List[pygame.Surface],
        villagers: Dict[Coord, int],
        cell_size: int,
        offset: Coord
):
    if not villagers:
        return

    ox, oy = offset

    for pos, index in villagers.items():
        px, py = pos
        window.blit(sprites[index], (ox + py * cell_size, oy + px * cell_size))


def draw(
        window: pygame.Surface,
        offset: Coord,
        cell_size: int,

        *sprites: Tuple[Coord, pygame.Surface, bool]
):
    ox, oy = offset

    for (py, px), sprite, flip in sprites:
        if flip:
            sprite = pygame.transform.flip(sprite, True, False)

        window.blit(sprite, (ox + px * cell_size, oy + py * cell_size))


def unpack_villagers_for_draw(
        villagers: List[Tuple[Coord, int]],
        sprites: List[pygame.Surface]
) -> List[Tuple[Coord, pygame.Surface, bool]]:

    return [(coord, sprites[index], False) for coord, index in villagers]


def update_window_title(level: str) -> None:
    caption = f"Dungeon Dive - {level}"

    if pygame.display.get_caption() != caption:
        pygame.display.set_caption(caption)


def calculate_move_progress(progress: float, fps: int, move_speed: float):
    return min(1.0, progress + (1/fps * move_speed))


def recalculate_sizes(
        window_size: Tuple[int, int],
        maze_size: Tuple[int, int],
        texture_paths: ImagePaths,
):
    cell_size, offset = calculate_maze_dimensions(window_size, maze_size)
    images = load_images(texture_paths, cell_size)

    return cell_size, offset, images
