import pygame
import sys
from player import Player
from enemy import Enemy
from main_menu import MainMenu, PauseMenu, GameOverMenu
from game_states import MenuState, PlayingState, PausedState, GameOverState


class Game:
    def __init__(self):
        self.WIDTH = 1440
        self.HEIGHT = 900
        self.LEVEL_WIDTH = 2880
        self.FPS = 60

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Umbra')

        self.world_surface = pygame.Surface((self.LEVEL_WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Menu
        self.main_menu = MainMenu(self.WIDTH, self.HEIGHT)
        self.pause_menu = PauseMenu(self.WIDTH, self.HEIGHT)
        self.game_over_menu = GameOverMenu(self.WIDTH, self.HEIGHT)

        # Khởi tạo vật thể
        self.player = None
        self.enemies = []
        self.camera_x = 0

        self.solid_platforms = [
            pygame.Rect(0, self.HEIGHT - 80, self.LEVEL_WIDTH, 80),
            pygame.Rect(900, self.HEIGHT - 180, 40, 100)
        ]

        self.one_way_platforms = [
            pygame.Rect(300, 600, 200, 30),
            pygame.Rect(600, 480, 200, 30)
        ]

        self.all_platforms = self.solid_platforms + self.one_way_platforms

        self.states = {
            'menu': MenuState(self),
            'playing': PlayingState(self),
            'paused': PausedState(self),
            'game_over': GameOverState(self),
        }
        self.current_state = self.states['menu']

    def change_state(self, state_name):
        self.current_state = self.states[state_name]

    def start_game(self):
        self.player = Player(100, 100)
        self.enemies = [Enemy(600, self.HEIGHT - 90 * 4), Enemy(500, self.HEIGHT - 90 * 4)]
        self.camera_x = 0
        self.change_state('playing')

    def draw_game_scene(self, screen):
        self.world_surface.fill('#1c1c2e')
        for platform in self.all_platforms:
            pygame.draw.rect(self.world_surface, self.WHITE, platform)
        self.player.draw(self.world_surface)
        for enemy in self.enemies:
            enemy.draw(self.world_surface)
        screen.blit(self.world_surface, (-self.camera_x, 0))

    def run(self):
        while self.running:
            # Xử lý ấn nút
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.current_state.handle_event(event)

            # Update
            self.current_state.update()

            # Draw
            self.current_state.draw(self.screen)

            pygame.display.update()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()