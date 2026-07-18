import pygame
from support import import_sprite_sheet

ATTACK_HIT_WINDOWS = {
    'attack1': [
        [3],        
    ],
    'attack2': [
        [3],          
        [10],
    ],
}

class Player:
    def __init__(self, x, y):
        self.import_assets()
        self.status = 'idle'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.animation_speed_attack = 0.3
        self.animation_speed_death = 0.1
        self.animation_speed_hurt = 0.35
        self.attack_type = 'attack1'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = (x, y))
        self.hitbox = pygame.Rect(0, 0, 80, 92)
        self.foot_padding = 63 * 4
        self.hitbox.midbottom = (
            self.rect.centerx,
            self.rect.bottom - self.foot_padding,   # trừ phần đệm trống ra
        )

        self.max_health = 100
        self.health = self.max_health
        self.alive = True
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 800

        self.attacking = False
        self.cooldown = 500
        self.attack_time = 0
        self.enemies_hit_attack = set()
        self.current_hit_window = None

        self.hurt = False

        self.direction = pygame.math.Vector2()
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

        self.speed = 8
        self.jump_strength = -15
        self.gravity = 0.6

        self.dashing = False
        self.dash_time = 0
        self.dash_duration = 200
        self.dash_cooldown = 800
        self.dash_speed = 18
        self.dash_direction = 1
        self.animation_speed_dash = 0.2
    
    def import_assets(self):
        FRAME_SIZE = 144
        SCALE = 4
        self.animations = {
            'idle' : import_sprite_sheet('graphics/player/Idle.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'run' : import_sprite_sheet('graphics/player/Run.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'dash' : import_sprite_sheet('graphics/player/Dash.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'jump' : import_sprite_sheet('graphics/player/Jump.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'fall' : import_sprite_sheet('graphics/player/Fall.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'hurt' : import_sprite_sheet('graphics/player/Hurt.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'death' : import_sprite_sheet('graphics/player/Death.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'attack1' : import_sprite_sheet('graphics/player/Attack 1.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'attack2' : import_sprite_sheet('graphics/player/Attack 2.png', FRAME_SIZE, FRAME_SIZE, SCALE)
        }

    def apply_gravity(self): # Trọng lực rơi
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y
    
    def limit_screen(self, width): #Chặn 2 bên màn
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > width:
            self.hitbox.right = width

    def check_collision(self, solid_platforms):
        current_dir_x = self.dash_direction if self.dashing else self.direction.x

        for platform in solid_platforms:
            if self.hitbox.colliderect(platform):
                overlap_x = min(self.hitbox.right, platform.right) - max(self.hitbox.left, platform.left)
                overlap_y = min(self.hitbox.bottom, platform.bottom) - max(self.hitbox.top, platform.top)

                if overlap_x < overlap_y:
                    if current_dir_x > 0:
                        self.hitbox.right = platform.left
                    elif current_dir_x < 0:
                        self.hitbox.left = platform.right

    def check_vertical_collisions(self, all_platforms): # Xử lý rơi chạm đất 
        self.on_ground = False  

        for platform in all_platforms:
            if (self.velocity_y >= 0 and
                self.hitbox.bottom >= platform.top and
                self.hitbox.right >= platform.left and
                self.hitbox.left <= platform.right and
                self.hitbox.bottom <= platform.top + self.velocity_y + 1):
                self.hitbox.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True

    def get_input(self): #Xử lý giữ phím
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        
    
    def move_x(self): #Di chuyển ngang
        self.hitbox.x += self.direction.x * self.speed

    def update_dash(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.dash_time >= self.dash_duration:
            self.dashing = False
            return
        
        self.hitbox.x += self.dash_direction * self.dash_speed

    def jump(self): 
        if self.on_ground == True:
            self.velocity_y = self.jump_strength
            self.on_ground = False

    def attack(self, attack_type = 'attack1'):
        current_time = pygame.time.get_ticks()
        if not self.attacking and current_time - self.attack_time >= self.cooldown:
            self.attack_type = attack_type
            self.attacking = True
            self.attack_time = current_time
            self.frame_index = 0
            self.enemies_hit_attack.clear()
            self.current_hit_window = None

    def dash(self):
        current_time = pygame.time.get_ticks()

        if self.dashing or self.hurt or self.attacking:
            return
        
        if current_time - self.dash_time < self.dash_cooldown:
            return
        
        self.dashing = True
        self.dash_time = current_time
        self.dash_direction = 1 if self.facing_right else -1
        self.frame_index = 0

    
    def get_attack_hitbox(self):
        if not self.attacking:
            return None
        
        current_frame = int(self.frame_index)
        hit_windows = ATTACK_HIT_WINDOWS.get(self.attack_type,[])

        window_index = None
        for index, frame_group in enumerate(hit_windows):
            if current_frame in frame_group:
                window_index = index
                break
        
        if window_index is None:
            return None
        
        if window_index != self.current_hit_window:
            self.enemies_hit_attack.clear()
            self.current_hit_window = window_index
        
        attack_width = 120 + 30
        attack_height = 80

        if self.facing_right:
            attack_hitbox = pygame.Rect(self.hitbox.right - 30, 
                                        self.hitbox.centery - attack_height // 2,
                                        attack_width, attack_height
                                        )
        else :
            attack_hitbox = pygame.Rect(self.hitbox.left - attack_width + 30, 
                                        self.hitbox.centery - attack_height // 2,
                                        attack_width, attack_height
                                        )
        
        return attack_hitbox
    
    def take_damage(self, amount):
        if self.invulnerable:
            return
        
        self.health -= amount

        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.status = 'death'
            self.frame_index = 0
        else:
            self.hurt = True
            self.attacking = False
            self.frame_index = 0

        self.invulnerable = True
        self.invulnerable_time = pygame.time.get_ticks()

    def update_invulnerable(self):
        if self.invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.invulnerable_time >= self.invulnerable_duration:
                self.invulnerable = False

    def get_status(self):
        if not self.alive:
            return
        
        if self.dashing:
            self.status = 'dash'
            return

        if self.hurt:
            self.status = 'hurt'
            return

        if self.attacking:
            self.status = self.attack_type
            return

        if not self.on_ground:
            if self.velocity_y < 0:
                self.status = 'jump'
            else :
                self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]
        if 'attack' in self.status:
            self.frame_index += self.animation_speed_attack
        elif self.status == 'death': 
            self.frame_index += self.animation_speed_death
        elif self.status == 'hurt':
            self.frame_index += self.animation_speed_hurt
        elif self.status == 'dash':
            self.frame_index += self.animation_speed_dash
        else: 
            self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == 'death':
                self.frame_index = len(animation) - 1
            else:
                self.frame_index = 0
                if 'attack' in self.status:
                    self.attacking = False
                elif self.status == 'hurt':
                    self.hurt = False
                    
        self.image = animation[int(self.frame_index)]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(
            midbottom=(self.hitbox.centerx, self.hitbox.bottom + self.foot_padding)
        )

    def update(self, solid_platforms, all_platforms, width):
        if not self.alive:
            self.apply_gravity()
            self.check_vertical_collisions(all_platforms)
            self.animate()
            return
        
        self.get_input()

        if self.dashing:
            self.update_dash()
        elif not self.hurt:
            self.move_x()

        if self.dashing or not self.hurt:
            self.check_collision(solid_platforms)

        self.limit_screen(width)

        if not self.dashing:
            self.apply_gravity()
            self.check_vertical_collisions(all_platforms)

        self.get_status()
        self.animate()
        self.update_invulnerable()

    def draw(self, screen):
        if self.alive and self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return
        screen.blit(self.image, self.rect)
        if self.alive:
            #Vẽ hitbox
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
            #vẽ attack_hitbox
            attack_hitbox = self.get_attack_hitbox()
            if attack_hitbox:
                pygame.draw.rect(screen, (255, 255, 0), attack_hitbox, 2)

            bar_width = self.hitbox.width
            bar_height = 6
            bar_x = self.hitbox.x
            bar_y = self.hitbox.y - bar_height - 4
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))