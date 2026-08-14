import pygame
from boss import Boss
from support import import_sprite_sheet


class IceBoss(Boss):
    def __init__(self, x, y):
        super().__init__(x, y, max_health=100)
        self.facing_right = False

        self.melee_damage = 30
        self.attack_range = 330
        self.notice_radius = 450
        self.chase_speed = 2.5
        self.cooldown = 1200

        self.foot_padding = 18 * 3
        self.hitbox = pygame.Rect(0, 0, 160, 220)
        self.hitbox.midbottom = (self.rect.centerx, self.rect.bottom - self.foot_padding)

        self.animation_speed = 0.15
        self.animation_speed_attack = 0.25
        self.animation_speed_hurt = 0.25
        self.animation_speed_death = 0.2

    def import_assets(self):
        FRAME_WIDTH = 192
        FRAME_HEIGHT = 128
        SCALE = 3

        self.animations = {
            'idle': import_sprite_sheet('graphics/boss1/idle.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'walk': import_sprite_sheet('graphics/boss1/walk.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'hurt': import_sprite_sheet('graphics/boss1/take hit.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'death': import_sprite_sheet('graphics/boss1/death.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'attack': import_sprite_sheet('graphics/boss1/attack.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
        }

    def get_status(self, player, all_platforms=None):
        if not self.alive:
            return
        if self.hurt:
            self.status = 'hurt'
            return
        if self.state == 'attack':
            self.status = 'attack'
            return

        distance_x = abs(player.hitbox.centerx - self.hitbox.centerx) - 40
        current_time = pygame.time.get_ticks()

        if distance_x <= self.attack_range and current_time - self.attack_time >= self.cooldown:
            self.state = 'attack'
            self.attacking = True
            self.attack_time = current_time
            self.frame_index = 0
            self.player_already_hit = False
            return

        if self.state == 'chase':
            stop_distance = self.attack_range - 5
            if distance_x > stop_distance:
                self.status = 'walk'
            else:
                self.status = 'idle' 
        elif self.state == 'patrol':
            self.status = 'walk'
        else:
            self.status = 'idle'

        self.status = 'walk' if self.state == 'chase' else 'idle'

    def animate(self):
        animation = self.animations[self.status]

        if self.status == 'attack':
            self.frame_index += self.animation_speed_attack
        elif self.status == 'death':
            self.frame_index += self.animation_speed_death
        elif self.status == 'hurt':
            self.frame_index += self.animation_speed_hurt
        else:
            self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == 'death':
                self.frame_index = len(animation) - 1
            else:
                self.frame_index = 0
                if self.status == 'attack':
                    self.state = 'chase'
                    self.attacking = False
                if self.status == 'hurt':
                    self.hurt = False

        image = animation[int(self.frame_index)]
        if self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.image = image
        self.rect = self.image.get_rect(
            midbottom=(self.hitbox.centerx, self.hitbox.bottom + self.foot_padding)
        )

    def get_attack_hitbox(self):
        if not self.attacking:
            return None

        current_frame = int(self.frame_index)
        if current_frame not in [7, 8]: 
            return None

        attack_width = 300
        attack_height = 100

        hitbox_y = self.hitbox.centery - (attack_height // 2) - 20

        if self.facing_right:
            return pygame.Rect(self.hitbox.right - 40, hitbox_y, attack_width, attack_height)
        else:
            return pygame.Rect(self.hitbox.left + 40 - attack_width, hitbox_y, attack_width, attack_height)

    def update(self, solid_platforms, all_platforms, player):
        super().update(solid_platforms, all_platforms, player)
        
        if not self.alive:
            return

        if not self.hurt:
            if self.state == 'chase' and not self.attacking:
                self.chase_player(player)
        self.check_collision(solid_platforms)

        self.get_status(player, all_platforms)
        self.animate()