import pygame
import sys
from types import SimpleNamespace
from player import Player
from enemy import Enemy
from boss_ice import IceBoss
from boss_witch import WitchBoss
from chest import Chest
from portal import Portal
from checkpoint import Checkpoint
from ui import UI
from map_background import Background
from audio import MusicManager
from main_menu import MainMenu, PauseMenu, GameOverMenu, VictoryMenu
from game_states import MenuState, PlayingState, PausedState, GameOverState, VictoryState
from tilemap import build_rect_from_csv, get_map_size, load_csv_map, build_tile_cache, draw_tile_layer

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH = 1440
HEIGHT = 900
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Umbra')

clock = pygame.time.Clock()

LEVELS = {
    1: {
        'solid': 'Map/level1_solid.csv',
        'oneway': 'Map/level1_oneway.csv',
        'decorback': 'Map/level1_decorback.csv',
        'decorfront': 'Map/level1_decorfront.csv',
        'tileset': 'Map/Snow platform tileset.png',
        'player_spawn': (48, 1152),
        'checkpoints': [
            (1338, 896),
            (4398, 384),
        ],
        'enemies': [
            (1168, 1280), (1776, 1216), (2512, 1216),
            (3272, 1216), (4056, 640),
        ],
        'boss_class': IceBoss,
        'boss': (7048, 448),
        'portal_offset': (300, 0),
        'chests': [
            (4128, 576), (1304, 1280),
        ],
        'portal_pos': None,
    },
    2: {
        'solid': 'Map/level2_solid.csv',
        'oneway': 'Map/level2_oneway.csv',
        'decorback': 'Map/level2_decorback.csv',
        'decorfront': 'Map/level2_decorfront.csv',
        'tileset': 'Map/Snow platform tileset.png',
        'player_spawn': (48, 1152),
        'checkpoints': [
            (4594, 1216), (6574, 1024),
        ],
        'enemies': [
            (1200, 1200), (2400, 1200), (2088, 192),
            (3408, 704), (4092, 1024)
        ],
        'boss_class': WitchBoss,
        'boss': (6922, 1024),
        'chests': [
            (1786, 1280), (4480, 1216)
        ],
        'portal_pos': None,
    },
    3: {
        'solid': 'Map/level3_solid.csv',
        'oneway': 'Map/level3_oneway.csv',
        'decorback': 'Map/level3_decorback.csv',
        'decorfront': 'Map/level3_decorfront.csv',
        'tileset': 'Map/Snow platform tileset.png',
        'player_spawn': (48, 1152),
        'checkpoints': [
            (1648, 320), (6592, 640),
        ],
        'enemies': [
            (1760, 320), (2728, 832), (4080, 256),
            (4056, 1216), (6586, 640)
        ],
        'boss_class': WitchBoss,
        'boss': (7456, 640),
        'chests': [
            (4738, 1088), (3072, 832)
        ],
        'portal_pos': None,
    },
}


def load_level_assets(level_number):
    cfg = LEVELS[level_number]

    level_width, level_height = get_map_size(cfg['solid'])

    solid_platforms = build_rect_from_csv(cfg['solid'])
    one_way_platforms = build_rect_from_csv(cfg['oneway'])
    all_platforms = solid_platforms + one_way_platforms

    solid_grid = load_csv_map(cfg['solid'])
    one_way_grid = load_csv_map(cfg['oneway'])
    decor_back_grid = load_csv_map(cfg['decorback'])
    decor_front_grid = load_csv_map(cfg['decorfront'])

    tile_cache = build_tile_cache(cfg['tileset'])

    return {
        'LEVEL_WIDTH': level_width,
        'LEVEL_HEIGHT': level_height,
        'solid_platforms': solid_platforms,
        'one_way_platforms': one_way_platforms,
        'all_platforms': all_platforms,
        'solid_grid': solid_grid,
        'one_way_grid': one_way_grid,
        'decor_back_grid': decor_back_grid,
        'decor_front_grid': decor_front_grid,
        'tile_cache': tile_cache,
    }


def apply_level_assets(level_number):
    assets = load_level_assets(level_number)
    for key, value in assets.items():
        setattr(game, key, value)

    game.world_surface = pygame.Surface((game.LEVEL_WIDTH, game.LEVEL_HEIGHT), pygame.SRCALPHA)
    game.current_level = level_number


def make_chest(chest_cfg):
    if len(chest_cfg) == 3:
        x, y, heal_amount = chest_cfg
        return Chest(x, y, heal_amount)
    x, y = chest_cfg
    return Chest(x, y)


def populate_entities(level_number):
    game.boss_music_started = False
    cfg = LEVELS[level_number]

    game.enemies = [Enemy(x, y) for (x, y) in cfg.get('enemies', [])]
    game.chests = [make_chest(chest_cfg) for chest_cfg in cfg.get('chests', [])]
    game.checkpoints = [Checkpoint(x, y) for x, y in cfg.get('checkpoints', [])]

    game.respawn_position = cfg['player_spawn']
    boss_pos = cfg.get('boss')
    boss_class = cfg.get('boss_class')
    if boss_pos and boss_class:
        game.boss_spawn_pos = boss_pos
        game.boss = boss_class(*boss_pos) 
        game.portal_offset = cfg.get('portal_offset', (300, 0))
        game.portal = None
    else:
        game.boss_spawn_pos = None
        game.boss = None
        portal_pos = cfg.get('portal_pos')
        game.portal = Portal(*portal_pos) if portal_pos else None

def change_state(state_name):
    game.current_state = states[state_name]


def start_game():
    apply_level_assets(1)

    spawn_x, spawn_y = LEVELS[1]['player_spawn']
    game.player = Player(spawn_x, spawn_y)
    game.max_lives = 3
    game.lives = game.max_lives
    game.lives_at_level_start = game.lives
    populate_entities(1)

    game.camera_x = 0
    game.camera_y = 0
    game.music.play('play')
    change_state('playing')

def respawn_at_checkpoint():
    spawn_x, spawn_y = game.respawn_position
    game.player = Player(spawn_x, spawn_y)

    game.camera_x = max(0, spawn_x - game.WIDTH * 0.45)
    game.camera_y = max(0, spawn_y - game.HEIGHT * 0.5)

def restart_current_level():
    level = game.current_level
    game.lives = game.lives_at_level_start

    apply_level_assets(level)

    spawn_x, spawn_y = LEVELS[level]['player_spawn']
    game.player = Player(spawn_x, spawn_y)
    populate_entities(level)

    game.camera_x = 0
    game.camera_y = 0
    game.music.play('play', force=True)
    game.boss_music_started = False
    change_state('playing')


def advance_to_next_level():
    next_level = game.current_level + 1
    if next_level not in LEVELS:
        change_state('victory')
        return

    apply_level_assets(next_level)
    game.lives_at_level_start = game.lives

    spawn_x, spawn_y = LEVELS[next_level]['player_spawn']
    game.player.hitbox.bottomleft = (spawn_x, spawn_y)
    game.player.velocity_y = 0

    populate_entities(next_level)

    game.music.play('play')
    game.boss_music_started = False

    game.camera_x = 0
    game.camera_y = 0


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
    if game.portal:
            game.portal.draw(screen, cam_x, cam_y, game.player)
    game.player.draw(screen, cam_x, cam_y)
    if game.boss:
        game.boss.draw(screen, cam_x, cam_y)
    for enemy in game.enemies:
        enemy.draw(screen, cam_x, cam_y)
    game.ui.draw_health_bar(screen, game.player.health, game.player.max_health)
    game.ui.draw_lives(screen, game.lives, game.max_lives)
    if game.boss and game.boss.alive:
        if game.boss.state not in ['idle', 'patrol']:
            game.ui.draw_boss_health(screen, game.boss.health, game.boss.max_health)


initial_assets = load_level_assets(1)

game = SimpleNamespace(
    WIDTH=WIDTH,
    HEIGHT=HEIGHT,
    FPS=FPS,

    BLACK=BLACK,
    WHITE=WHITE,

    screen=screen,
    world_surface=pygame.Surface(
        (initial_assets['LEVEL_WIDTH'], initial_assets['LEVEL_HEIGHT']), pygame.SRCALPHA
    ),
    clock=clock,
    running=True,

    main_menu=MainMenu(WIDTH, HEIGHT),
    pause_menu=PauseMenu(WIDTH, HEIGHT),
    game_over_menu=GameOverMenu(WIDTH, HEIGHT),
    victory_menu=VictoryMenu(WIDTH, HEIGHT),
    ui=UI(WIDTH, HEIGHT),
    background=Background(WIDTH, HEIGHT),
    music=MusicManager(),
    boss_music_started=False,

    player=None,
    enemies=[],
    boss=None,
    boss_spawn_pos=None,
    portal_offset=(300, 0),
    chests=[],
    portal=None,
    current_level=1,
    camera_x=0,
    camera_y=0,
    max_lives=3,
    lives=3,
    lives_at_level_start=3,
    respawn_position=None,
    checkpoints=[],
    **initial_assets,
)

game.change_state = change_state
game.start_game = start_game
game.restart_current_level = restart_current_level
game.advance_to_next_level = advance_to_next_level
game.draw_game_scene = draw_game_scene
game.get_camera_offset = get_camera_offset
game.respawn_at_checkpoint = respawn_at_checkpoint

states = {
    'menu': MenuState(game),
    'playing': PlayingState(game),
    'paused': PausedState(game),
    'game_over': GameOverState(game),
    'victory': VictoryState(game),
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