import math
import pygame


class MenuBackgroundAnimation:

    ASSET_DIR = 'graphics/main_menu/'

    def __init__(self, width, height):
        self.width = width
        self.height = height

        load = self._load

        # Load từng lớp
        self.sky = load('sky.png')
        self.sky_light = load('sky_lightened.png')

        self.clouds_bg = load('clouds_bg.png')

        self.mountains = load('glacial_mountains.png')
        self.mountains_light = load('glacial_mountains_lightened.png')

        self.mg3 = load('clouds_mg_3.png')
        self.mg2 = load('clouds_mg_2.png')
        self.mg1 = load('clouds_mg_1.png')
        self.mg1_light = load('clouds_mg_1_lightened.png')

        self.cloud_lonely = load('cloud_lonely.png')

        # Tiêu đề game
        self.title = self._load_title('umbra.png', max_width_ratio=0.5)
        self.title_top_ratio = 0.10

        # Vị trí cuộn hiện tại của từng lớp
        self.offset_clouds_bg = 0.0
        self.offset_mg3 = 0.0
        self.offset_mg2 = 0.0
        self.offset_mg1 = 0.0
        self.offset_lonely = 0.0

        # Tốc độ cuộn từng lớp
        self.speed_clouds_bg = 0.15
        self.speed_mg3 = 0.20
        self.speed_mg2 = 0.30
        self.speed_mg1 = 0.40
        self.speed_lonely = 0.55

        # Đồng hồ cho hiệu ứng glow
        self.glow_timer = 0.0
        self.glow_speed = 0.02          # tốc độ nhấp nháy
        self.glow_strength = 0.5        # độ trộn tối đa

    def _load(self, filename):
        img = pygame.image.load(self.ASSET_DIR + filename).convert_alpha()
        return pygame.transform.scale(img, (self.width, self.height))

    def _load_title(self, filename, max_width_ratio):
        raw = pygame.image.load(self.ASSET_DIR + filename).convert_alpha()
        target_w = int(self.width * max_width_ratio)
        scale = target_w / raw.get_width()
        target_h = int(raw.get_height() * scale)
        return pygame.transform.scale(raw, (target_w, target_h))

    def update(self):
        self.offset_clouds_bg += self.speed_clouds_bg
        self.offset_mg3 += self.speed_mg3
        self.offset_mg2 += self.speed_mg2
        self.offset_mg1 += self.speed_mg1
        self.offset_lonely += self.speed_lonely

        self.glow_timer += self.glow_speed

    def _glow_alpha(self):
        pulse = (math.sin(self.glow_timer) + 1) / 2
        return int(pulse * self.glow_strength * 255)

    def _draw_tile_layer(self, screen, tile, offset):
        """Vẽ 1 layer chỉ có 1 ảnh, lặp lại liên tục theo trục x (cuộn phải -> trái)."""
        tile_w = tile.get_width()
        x = -(offset % tile_w)
        while x < self.width:
            screen.blit(tile, (x, 0))
            x += tile_w

    def _draw_tile_layer_with_glow(self, screen, tile, glow_tile, offset, alpha):
        tile_w = tile.get_width()
        x = -(offset % tile_w)

        glow_tile.set_alpha(alpha)
        while x < self.width:
            screen.blit(tile, (x, 0))
            screen.blit(glow_tile, (x, 0))
            x += tile_w
        glow_tile.set_alpha(255)  # trả lại mặc định cho lần dùng sau

    def draw(self, screen):
        alpha = self._glow_alpha()

        # Sky
        screen.blit(self.sky, (0, 0))
        self.sky_light.set_alpha(alpha)
        screen.blit(self.sky_light, (0, 0))
        self.sky_light.set_alpha(255)

        # Clouds nền
        self._draw_tile_layer(screen, self.clouds_bg, self.offset_clouds_bg)

        # Mountains
        self._draw_tile_layer_with_glow(
            screen, self.mountains, self.mountains_light, 0, alpha
        )

        # Clouds giữa 3
        self._draw_tile_layer(screen, self.mg3, self.offset_mg3)

        # Clouds giữa 2
        self._draw_tile_layer(screen, self.mg2, self.offset_mg2)

        # Clouds giữa 1
        self._draw_tile_layer_with_glow(
            screen, self.mg1, self.mg1_light, self.offset_mg1, alpha
        )

        # Cloud đơn lẻ
        self._draw_tile_layer(screen, self.cloud_lonely, self.offset_lonely)

        # Tiêu đề game
        title_rect = self.title.get_rect()
        title_rect.centerx = self.width // 2
        title_rect.centery = int(self.height * self.title_top_ratio)
        screen.blit(self.title, title_rect)