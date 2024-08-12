import copy
import random
from collections import deque
from typing import NewType, List, Tuple, Optional, Dict

import numpy as np
import pygame

MazeStructure = NewType("Maze", List[List[int]])
Coord = Tuple[int, int]


def random_odd(start: int, end: int) -> int:
    return random.choice(range(start + (1 - (start % 2)), end + (end % 2), 2))


def random_pos(rows: int, cols: int) -> Coord:
    return random_odd(1, rows - 1), random_odd(1, cols - 1)


def gen_maze(rows: int, cols: int, start: Coord) -> MazeStructure:
    maze = [[True] * cols for _ in range(rows)]

    def carve_path(pos: Coord) -> None:
        stack: List[Coord] = [pos]
        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]

        while stack:
            x, y = stack[-1]
            random.shuffle(directions)
            carved = False

            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny]:
                    maze[x + dx][y + dy] = False
                    maze[nx][ny] = False
                    stack.append((nx, ny))
                    carved = True
                    break

            if not carved:
                stack.pop()

    start_x, start_y = start
    maze[start_x][start_y] = False
    carve_path(start)

    return MazeStructure(maze)


def _bfs_farthest_point(maze: MazeStructure, start: Coord) -> Coord:
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start[0], start[1], 0)])
    visited = np.zeros((rows, cols), dtype=bool)
    visited[start[0]][start[1]] = True
    farthest_point = start
    max_distance = 0

    while queue:
        x, y, dist = queue.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and not maze[nx][ny] and not visited[nx][ny]:
                visited[nx][ny] = True
                queue.append((nx, ny, dist + 1))
                if dist + 1 > max_distance:
                    max_distance = dist + 1
                    farthest_point = (nx, ny)

    return farthest_point


def _find_longest_path(maze: MazeStructure, *, start: Optional[Coord] = None) -> Tuple[Coord, Coord]:
    rows, cols = len(maze), len(maze[0])

    if start is not None:
        return start, _bfs_farthest_point(maze, start)

    start = next((i, j) for i in range(rows // 2, rows) for j in range(cols // 2, cols) if maze[i][j] is False)
    farthest_point = _bfs_farthest_point(maze, start)
    start_point = _bfs_farthest_point(maze, farthest_point)

    return start_point, farthest_point


def _bfs_dead_ends(maze: MazeStructure, start: Coord) -> List[Coord]:
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    queue = deque([(start[0], start[1], 0)])
    visited = [[False] * cols for _ in range(rows)]
    visited[start[0]][start[1]] = True
    dead_ends = []

    while queue:
        x, y, dist = queue.popleft()
        # Count the number of open neighbors
        open_neighbors = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] is False:
                open_neighbors += 1
                if not visited[nx][ny]:
                    visited[nx][ny] = True
                    queue.append((nx, ny, dist + 1))

        # A dead end is a cell with exactly one open neighbor
        if open_neighbors == 1:
            dead_ends.append(((x, y), dist))

    # Sort dead ends by distance in descending order and return only coordinates
    dead_ends.sort(key=lambda item: item[1], reverse=True)
    return [coord for coord, _ in dead_ends]


def place_spikes(maze: MazeStructure, coord_black_list: List[Coord]) -> List[Coord]:
    i = 0
    space = 5
    spikes = []

    for x in range(len(maze)):
        for y in range(len(maze[0])):
            if maze[x][y] is False and (x, y) not in coord_black_list:
                if i % space == 0:
                    maze[x][y] = "spike_False"
                    spikes.append((x, y))
                    space = random.randint(5, 10)
                i += 1

    return spikes


def setup_positions(maze: MazeStructure) -> Tuple[Coord, Coord, List[Coord]]:
    rows, cols = len(maze), len(maze[0])
    start = next((i, j) for i in range(rows // 2, rows) for j in range(cols // 2, cols) if maze[i][j] is False)

    dead_ends = _bfs_dead_ends(maze, start)

    farthest_point = dead_ends[0]
    start_point = _bfs_farthest_point(maze, farthest_point)

    dead_ends.remove(start_point)
    dead_ends.remove(farthest_point)

    return start_point, farthest_point, dead_ends
