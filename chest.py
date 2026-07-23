import pygame

class Chest:
    def __init__(self, x, y, heal_amount = 30):
        self.hitbox = pygame.Rect(x, y, 80, 80)
        self.hitbox.bottomleft = (x, y)
        self.opened = False
        self.heal_amount = heal_amount
        self.interact_radius = 120

    def get_distance_to_player(self, player):
        chest_pos = pygame.math.Vector2(self.hitbox.center)
        player_pos = pygame.math.Vector2(player.hitbox.center)
        return chest_pos.distance_to(player_pos)
    
    def can_interact(self, player):
        if self.opened:
            return False
        return self.get_distance_to_player(player) < self.interact_radius
    
    def open(self, player):
        if self.opened:
            return
        self.opened = True
        player.health = min(player.health + self.heal_amount, player.max_health)

    def draw(self, screen, player):
        color = '#c9a34a' if self.opened else '#7a4a1e'
        pygame.draw.rect(screen, color, self.hitbox)
        pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 2)  # viền đen cho rõ

        if self.can_interact(player):
            font = pygame.font.SysFont('arial', 20)
            hint = font.render('Nhấn E để mở', True, (255, 255, 255))
            hint_rect = hint.get_rect(midbottom=(self.hitbox.centerx, self.hitbox.top - 8))
            screen.blit(hint, hint_rect)