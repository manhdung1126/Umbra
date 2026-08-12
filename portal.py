import pygame
from support import import_sprite_sheet


class Portal:
    def __init__(self, x, y):
        self.import_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.animations[self.status][int(self.frame_index)]

        self.hitbox = pygame.Rect(0, 0, 130, 160)
        self.hitbox.midbottom = (x, y)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        self.interact_radius = 130

    def import_assets(self):
        FRAME_WIDTH = 66
        FRAME_HEIGHT = 68
        SCALE = 3
        self.animations = {
            'idle': import_sprite_sheet('graphics/portal/portal.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
        }

    def get_distance_to_player(self, player):
        portal_pos = pygame.math.Vector2(self.hitbox.center)
        player_pos = pygame.math.Vector2(player.hitbox.center)
        return portal_pos.distance_to(player_pos)

    def can_interact(self, player):
        return self.get_distance_to_player(player) < self.interact_radius

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

    def update(self):
        self.animate()

    def draw(self, screen, cam_x, cam_y, player):
        draw_rect = self.rect.move(-cam_x, -cam_y)
        screen.blit(self.image, draw_rect)
        
        if self.can_interact(player):
            font = pygame.font.SysFont('arial', 20)
            hint = font.render('Nhấn E để sang màn tiếp theo', True, (255, 255, 255))
            
            center_x = self.hitbox.centerx - cam_x
            top_y = self.hitbox.top - cam_y - 8
            
            hint_rect = hint.get_rect(midbottom=(center_x, top_y))
            screen.blit(hint, hint_rect)