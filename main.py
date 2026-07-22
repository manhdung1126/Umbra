import pygame
import sys
from types import SimpleNamespace
from player import Player
from enemy import Enemy
from main_menu import MainMenu, PauseMenu, GameOverMenu
from game_states import MenuState, PlayingState, PausedState, GameOverState

pygame.init()

WIDTH = 1440
HEIGHT = 900
LEVEL_WIDTH = 2880
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Umbra')

world_surface = pygame.Surface((LEVEL_WIDTH, HEIGHT))
clock = pygame.time.Clock()

solid_platforms = [
    pygame.Rect(0, HEIGHT - 80, LEVEL_WIDTH, 80),
    pygame.Rect(900, HEIGHT - 180, 40, 100),
]

one_way_platforms = [
    pygame.Rect(300, 600, 200, 30),
    pygame.Rect(600, 480, 200, 30),
]

all_platforms = solid_platforms + one_way_platforms

game = SimpleNamespace(
    WIDTH = WIDTH, 
    HEIGHT = HEIGHT, 
    LEVEL_WIDTH = LEVEL_WIDTH, 
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

    player = None, 
    enemies = [], 
    camera_x = 0,

    solid_platforms = solid_platforms,
    one_way_platforms = one_way_platforms,
    all_platforms = all_platforms,
)


def change_state(state_name):
    game.current_state = states[state_name]


def start_game():
    game.player = Player(100, 100)
    game.enemies = [Enemy(600, HEIGHT - 90 * 4), Enemy(500, HEIGHT - 90 * 4)]
    game.camera_x = 0
    change_state('playing')


def draw_game_scene(screen):
    game.world_surface.fill('#1c1c2e')
    for platform in game.all_platforms:
        pygame.draw.rect(game.world_surface, game.WHITE, platform)
    game.player.draw(game.world_surface)
    for enemy in game.enemies:
        enemy.draw(game.world_surface)
    screen.blit(game.world_surface, (-game.camera_x, 0))

game.change_state = change_state
game.start_game = start_game
game.draw_game_scene = draw_game_scene

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
    clock.tick(FPS)

pygame.quit()
sys.exit()