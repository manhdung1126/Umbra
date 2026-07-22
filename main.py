import pygame
import sys
from types import SimpleNamespace
from player import Player
from enemy import Enemy
from ui import UI
from main_menu import MainMenu, PauseMenu, GameOverMenu
from game_states import MenuState, PlayingState, PausedState, GameOverState
from tilemap import build_solid_rect_from_csv, get_map_size, load_csv_map, build_tile_cache, draw_tile_layer

pygame.init()

WIDTH = 1440
HEIGHT = 900
LEVEL_WIDTH, LEVEL_HEIGHT = get_map_size('Map/level1_solid.csv')
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Umbra')

world_surface = pygame.Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
clock = pygame.time.Clock()

solid_platforms = build_solid_rect_from_csv('Map/level1_solid.csv')
one_way_platforms = build_solid_rect_from_csv('Map/level1_oneway.csv')
all_platforms = solid_platforms + one_way_platforms

solid_grid = load_csv_map('Map/level1_solid.csv')
one_way_grid = load_csv_map('Map/level1_oneway.csv')

tile_cache = build_tile_cache('Map/Snow platform tileset.png')

game = SimpleNamespace(
    WIDTH = WIDTH,
    HEIGHT = HEIGHT,
    LEVEL_WIDTH = LEVEL_WIDTH,
    LEVEL_HEIGHT = LEVEL_HEIGHT,
    FPS = FPS,

    BLACK = BLACK,
    WHITE = WHITE,

    screen = screen,
    world_surface = world_surface,
    clock = clock,
    running = True,

    main_menu = MainMenu(WIDTH, HEIGHT),
    pause_menu = PauseMenu(WIDTH, HEIGHT),
    game_over_menu = GameOverMenu(WIDTH, HEIGHT),
    ui = UI(WIDTH, HEIGHT),

    player = None,
    enemies = [],
    camera_x = 0,
    camera_y = 0,

    solid_platforms = solid_platforms,
    one_way_platforms = one_way_platforms,
    all_platforms = all_platforms,

    solid_grid = solid_grid,
    one_way_grid = one_way_grid,
    tile_cache = tile_cache,
)


def change_state(state_name):
    game.current_state = states[state_name]


def start_game():
    game.player = Player(48, 1152)
    game.enemies = [
        Enemy(1168, 1280), Enemy(1776, 1216), Enemy(2512, 1216),
        Enemy(3272, 1216), Enemy(4056, 640), Enemy(7048, 448),
    ]
    game.camera_x = 0
    game.camera_y = 0
    change_state('playing')


def get_camera_offset(player, level_width, level_height, screen_width, screen_height):
    # Tinh camera theo player va giu camera trong bien level.
    camera_x = player.hitbox.centerx - screen_width // 2
    camera_y = player.hitbox.centery - screen_height // 2

    max_camera_x = max(0, level_width - screen_width)
    max_camera_y = max(0, level_height - screen_height)

    camera_x = max(0, min(camera_x, max_camera_x))
    camera_y = max(0, min(camera_y, max_camera_y))

    return camera_x, camera_y


def draw_game_scene(screen):
    game.world_surface.fill('#1c1c2e')
    draw_tile_layer(game.world_surface, game.solid_grid, game.tile_cache)
    draw_tile_layer(game.world_surface, game.one_way_grid, game.tile_cache)
    game.player.draw(game.world_surface)
    for enemy in game.enemies:
        enemy.draw(game.world_surface)
    screen.blit(game.world_surface, (-int(game.camera_x), -int(game.camera_y)))


game.change_state = change_state
game.start_game = start_game
game.draw_game_scene = draw_game_scene
game.get_camera_offset = get_camera_offset

states = {
    'menu': MenuState(game),
    'playing': PlayingState(game),
    'paused': PausedState(game),
    'game_over': GameOverState(game),
}

game.current_state = states['menu']

while game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        game.current_state.handle_event(event)

    game.current_state.update()
    game.current_state.draw(game.screen)

    pygame.display.update()
    game.clock.tick(game.FPS)

pygame.quit()
sys.exit()