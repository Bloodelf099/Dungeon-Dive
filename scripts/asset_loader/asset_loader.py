import os
from typing import Dict, List, Optional, Union, ForwardRef

import pygame


Paths = Dict[str, Union[str, ForwardRef('Paths')]]
ImagePaths = Dict[str, Union[pygame.Surface, 'ImagePaths']]


def load_paths(
        dir_path: str,
        whitelist: Optional[List[str]] = None,
        blacklist: Optional[List[str]] = (".venv", ".idea", ".vs"),
) -> Paths:
    paths = {}

    for entry in os.scandir(dir_path):
        if whitelist is not None and entry.name not in whitelist:
            continue

        if blacklist is not None and entry.name in blacklist:
            continue

        if entry.is_dir():
            paths[entry.name] = load_paths(entry.path)

        else:
            paths[entry.name] = entry.path

    return paths


def load_images(paths: Paths, cell_size: Optional[int] = None) -> ImagePaths:
    images = {}

    for key, value in paths.items():
        key = key.rsplit(".", 1)[0]

        if isinstance(value, dict):
            images[key] = load_images(value, cell_size)
        else:
            image = pygame.image.load(value)
            if cell_size is None:
                images[key] = image

            else:
                images[key] = pygame.transform.scale(image, (cell_size, cell_size))

    return images


def load_audio(paths: Paths) -> Paths:
    audios = {}

    for key, value in paths.items():
        key = key.rsplit(".", 1)[0]

        if isinstance(value, dict):
            audios[key] = load_audio(value)
        else:
            audios[key] = value

    return audios
