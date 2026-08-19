import pygame

class Checkpoint:
    def __init__(self, x, y):
        self.spawn_position = (x, y)
        self.hitbox = pygame.Rect(0, 0, 80, 160)
        self.hitbox.bottomleft = (x, y)
        self.active = False

    def check(self, player):
        if not self.active and self.hitbox.colliderect(player.hitbox):
            self.active = True
            return True
        return False