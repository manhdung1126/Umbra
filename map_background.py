import pygame

class Background:
    LAYER_DATA = [
        ('graphics/background/sky up.png', 0.05),
        ('graphics/background/layer 5 mountain and sky.png', 0.10),
        ('graphics/background/layer 4 mountain.png', 0.20),
        ('graphics/background/layer 3 grass.png', 0.35),
        ('graphics/background/layer 2 florest fog.png', 0.50),
        ('graphics/background/layer 1 florest.png', 0.70)
    ]

    BACKDROP_PATH = 'graphics/background/florest downt.png'

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.backdrop_color = self._load_backdrop_color(self.BACKDROP_PATH)

        self.layer = []
        for path, speed_x in self.LAYER_DATA:
            self.layer.append(self._buid_layer(path, speed_x))

        self.surface = pygame.Surface((width, height))

    def _load_backdrop_color(self, path):
        image = pygame.image.load(path).convert()
        return image.get_at((0, 0))

    def _buid_layer(self, path, speed_x):
        raw_image = pygame.image.load(path).convert_alpha()

        scale = self.height / raw_image.get_height()
        new_width = max(1, int(raw_image.get_width() * scale))
        image = pygame.transform.scale(raw_image, (new_width, self.height))

        return {
            'image': image,
            'width': new_width,
            'speed_x': speed_x,
        }

    def draw(self, screen):
        self.surface.fill(self.backdrop_color)
 
        for layer in self.layer:
            x = 0
            while x < self.width:
                self.surface.blit(layer['image'], (x, 0))
                x += layer['width']

        screen.blit(self.surface, (0, 0))