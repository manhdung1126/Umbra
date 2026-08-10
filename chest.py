import pygame
from support import import_sprite_sheet

class Chest:
    def __init__(self, x, y, heal_amount = 30):
        self.import_assets()
        self.status = 'close'
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations[self.status][self.frame_index]
        self.hitbox = pygame.Rect(x, y, 80, 80)
        self.hitbox.bottomleft = (x, y)
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
        self.opened = False
        self.heal_amount = heal_amount
        self.interact_radius = 120

    def import_assets(self):
            FRAME_WIDTH = 48
            FRAME_HEIGHT = 32
            SCALE = 2
            self.animations = {
                'close' : import_sprite_sheet('graphics/item/chest1_close.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
                'open' : import_sprite_sheet('graphics/item/chest1_open.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            }

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
        self.frame_index = 0
        self.status = 'open'
        player.health = min(player.health + self.heal_amount, player.max_health)

    def animate(self):
            animation = self.animations[self.status]
            self.frame_index += self.animation_speed
            if self.status == 'close':
                if self.frame_index >= len(animation):
                    self.frame_index = 0
            elif self.status == 'open':
                self.frame_index = len(animation) - 1
            self.image = animation[int(self.frame_index)]

    def update(self):
        self.animate()

    def draw(self, screen, cam_x, cam_y, player):
        draw_rect = self.rect.move(-cam_x, -cam_y)
        screen.blit(self.image, draw_rect)
        
        if self.can_interact(player):
            font = pygame.font.SysFont('arial', 20)
            hint = font.render('Nhấn E để mở', True, (255, 255, 255))
            
            center_x = self.hitbox.centerx - cam_x
            top_y = self.hitbox.top - cam_y - 8
            
            hint_rect = hint.get_rect(midbottom=(center_x, top_y))
            screen.blit(hint, hint_rect)