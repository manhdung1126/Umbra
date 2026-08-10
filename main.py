import pygame
import sys
from types import SimpleNamespace
from player import Player
from enemy import Enemy
from boss import Boss
from chest import Chest
from ui import UI
from map_background import Background
from main_menu import MainMenu, PauseMenu, GameOverMenu
from game_states import MenuState, PlayingState, PausedState, GameOverState
from tilemap import build_rect_from_csv, get_map_size, load_csv_map, build_tile_cache, draw_tile_layer

pygame.init()

WIDTH = 1440
HEIGHT = 900
LEVEL_WIDTH, LEVEL_HEIGHT = get_map_size('Map/level1_solid.csv')
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Umbra')

clock = pygame.time.Clock()

solid_platforms = build_rect_from_csv('Map/level1_solid.csv')
one_way_platforms = build_rect_from_csv('Map/level1_oneway.csv')

all_platforms = solid_platforms + one_way_platforms

solid_grid = load_csv_map('Map/level1_solid.csv')
one_way_grid = load_csv_map('Map/level1_oneway.csv')
decor_back_grid = load_csv_map('Map/level1_decorback.csv')
decor_front_grid = load_csv_map('Map/level1_decorfront.csv')

tile_cache = build_tile_cache('Map/Snow platform tileset.png')

game = SimpleNamespace(
    WIDTH=WIDTH,
    HEIGHT=HEIGHT,
    LEVEL_WIDTH=LEVEL_WIDTH,
    LEVEL_HEIGHT=LEVEL_HEIGHT,
    FPS=FPS,

    BLACK=BLACK,
    WHITE=WHITE,

    screen=screen,
    clock=clock,
    running=True,

    main_menu=MainMenu(WIDTH, HEIGHT),
    pause_menu=PauseMenu(WIDTH, HEIGHT),
    game_over_menu=GameOverMenu(WIDTH, HEIGHT),
    ui=UI(WIDTH, HEIGHT),
    background=Background(WIDTH, HEIGHT),

    player=None,
    enemies=[],
    boss=None,
    chests=[],
    camera_x=0,
    camera_y=0,

    solid_platforms=solid_platforms,
    one_way_platforms=one_way_platforms,
    all_platforms=all_platforms,

    solid_grid=solid_grid,
    one_way_grid=one_way_grid,
    decor_back_grid=decor_back_grid,
    decor_front_grid=decor_front_grid,
    tile_cache=tile_cache,
)


def change_state(state_name):
    game.current_state = states[state_name]


def start_game():
    game.player = Player(48, 1152)
    game.enemies = [
        Enemy(1168, 1280), Enemy(1776, 1216), Enemy(2512, 1216),
        Enemy(3272, 1216), Enemy(4056, 640),
    ]
    game.boss = Boss(7048, 448)
    game.chests = [Chest(4128, 576), Chest(1304, 1280)]
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
    game.background.draw(screen)
    cam_x = int(game.camera_x)
    cam_y = int(game.camera_y)
    draw_tile_layer(screen, game.solid_grid, game.tile_cache, cam_x, cam_y)
    draw_tile_layer(screen, game.one_way_grid, game.tile_cache, cam_x, cam_y)
    draw_tile_layer(screen, game.decor_back_grid, game.tile_cache, cam_x, cam_y)
    draw_tile_layer(screen, game.decor_front_grid, game.tile_cache, cam_x, cam_y)
    for chest in game.chests:
        chest.draw(screen, cam_x, cam_y, game.player) 
    game.player.draw(screen, cam_x, cam_y)
    if game.boss:
        game.boss.draw(screen, cam_x, cam_y)
    for enemy in game.enemies:
        enemy.draw(screen, cam_x, cam_y)
    game.ui.draw_health_bar(screen, game.player.health, game.player.max_health)


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