import pygame
import csv


SOURCE_TILE_SIZE = 16
SCALE = 4
WORLD_TILE_SIZE = SOURCE_TILE_SIZE * SCALE
TILESET_COLUMNS = 11
EMPTY_TILE = {-1}

def load_csv_map(path):
    grid = []

    with open(path, newline='') as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            grid.append([int(cell.strip()) for cell in row])

    return grid

def build_rect_from_csv(path):
    rects = []
    grid = load_csv_map(path)

    for row_index, row in enumerate(grid):
        for col_index, tile_id in enumerate(row):
            if tile_id in EMPTY_TILE:
                continue

            rects.append(
                pygame.Rect(
                    col_index * WORLD_TILE_SIZE,
                    row_index * WORLD_TILE_SIZE,
                    WORLD_TILE_SIZE,
                    WORLD_TILE_SIZE,
                )
            )

    return rects

def get_map_size(path):
    solid_grid = load_csv_map(path)

    level_width = len(solid_grid[0]) * WORLD_TILE_SIZE
    level_height = len(solid_grid) * WORLD_TILE_SIZE
    return level_width, level_height

def build_tile_cache(tileset_path):
    tileset = pygame.image.load(tileset_path).convert_alpha()
    cache = {}

    for tile_id in range(121):
        source_x = (tile_id % TILESET_COLUMNS) * SOURCE_TILE_SIZE
        source_y = (tile_id // TILESET_COLUMNS) * SOURCE_TILE_SIZE

        source_rect = pygame.Rect(
            source_x,
            source_y,
            SOURCE_TILE_SIZE,
            SOURCE_TILE_SIZE,
        )

        tile = tileset.subsurface(source_rect).copy()
        cache[tile_id] = pygame.transform.scale(
            tile,
            (WORLD_TILE_SIZE, WORLD_TILE_SIZE),
        )

    return cache


def draw_tile_layer(surface, grid, tile_cache, cam_x, cam_y):
    screen_w = surface.get_width()
    screen_h = surface.get_height()

    for row_index, row in enumerate(grid):
        for col_index, tile_id in enumerate(row):
            if tile_id in EMPTY_TILE:
                continue

            # Tính toán tọa độ vẽ trực tiếp trên màn hình sau khi áp dụng Camera Offset
            x = col_index * WORLD_TILE_SIZE - cam_x
            y = row_index * WORLD_TILE_SIZE - cam_y

            if -WORLD_TILE_SIZE <= x <= screen_w and -WORLD_TILE_SIZE <= y <= screen_h:
                surface.blit(
                    tile_cache[tile_id],
                    (x, y),
                )