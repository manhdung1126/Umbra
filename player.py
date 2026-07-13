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
        self.attack_type = 'attack1'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = (x, y))
        self.hitbox = pygame.Rect(0, 0, 80, 92)
        self.foot_padding = 63 * 4
        self.hitbox.midbottom = (
            self.rect.centerx,
            self.rect.bottom - self.foot_padding,   # trừ phần đệm trống ra
        )

        self.attacking = False
        self.cooldown = 500
        self.attack_time = 0
        self.enemies_hit_attack = set()
        self.current_hit_window = None

        self.direction = pygame.math.Vector2()
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

        self.speed = 5
        self.jump_strength = -15
        self.gravity = 0.6

    def get_input(self): #Xử lý giữ phím
        keys = pygame.key.get_pressed() # Lấy trạng thái phím MỚI NHẤT mỗi frame
        self.direction.x = 0
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        if keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False

    def limit_screen(self, width): #Chặn 2 bên màn
        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > width:
            self.hitbox.right = width

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
        
        if window_index == None:
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

    def apply_gravity(self): # Trọng lực rơi
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y

    def move_x(self): #Di chuyển ngang
        self.hitbox.x += self.direction.x * self.speed

    def check_collision(self, platforms):
        for platform in platforms:
            if self.hitbox.colliderect(platform):
                overlap_x = min(self.hitbox.right, platform.right) - max(self.hitbox.left, platform.left)
                overlap_y = min(self.hitbox.bottom, platform.bottom) - max(self.hitbox.top, platform.top)

                if overlap_x < overlap_y:
                    old_x = self.hitbox.x
                    if self.direction.x > 0:
                        self.hitbox.right = platform.left
                    elif self.direction.x < 0:
                        self.hitbox.left = platform.right
                    # print(f'VA CHẠM NGANG: x {old_x:.1f} -> {self.hitbox.x:.1f} (platform={platform})')

    def check_vertical_collisions(self, platforms): # Xử lý rơi chạm đất 
        self.on_ground = False  

        for platform in platforms:
            if (self.velocity_y >= 0 and
                self.hitbox.bottom >= platform.top and
                self.hitbox.right >= platform.left and
                self.hitbox.left <= platform.right and
                self.hitbox.bottom <= platform.top + self.velocity_y + 1):
                self.hitbox.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True

    def import_assets(self):
        FRAME_SIZE = 144
        SCALE = 4
        self.animations = {
            'idle' : import_sprite_sheet('graphics/player/Idle.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'run' : import_sprite_sheet('graphics/player/Run.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'jump' : import_sprite_sheet('graphics/player/Jump.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'fall' : import_sprite_sheet('graphics/player/Fall.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'attack1' : import_sprite_sheet('graphics/player/Attack 1.png', FRAME_SIZE, FRAME_SIZE, SCALE),
            'attack2' : import_sprite_sheet('graphics/player/Attack 2.png', FRAME_SIZE, FRAME_SIZE, SCALE)
        }

    def get_status(self):
        if self.attacking:
            self.status = self.attack_type
            return

        if not self.on_ground:
            if self.velocity_y < 0:
                self.status = 'jump'
            if self.velocity_y > 0:
                self.status = 'fall'
        elif self.direction.x != 0:
            self.status = 'run'
        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]
        if 'attack' in self.status:
            self.frame_index += self.animation_speed_attack
        else: 
            self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0
            if 'attack' in self.status:
                self.attacking = False

            
        self.image = animation[int(self.frame_index)]

        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(
            midbottom=(self.hitbox.centerx, self.hitbox.bottom + self.foot_padding)
        )


    def update(self, platforms, width):
        self.get_input()
        # if not self.attacking:
        self.move_x()
        self.check_collision(platforms)

        self.limit_screen(width)
        self.apply_gravity()
        self.check_vertical_collisions(platforms)

        # print(f'TRƯỚC gravity: x={self.hitbox.x:.1f} y={self.hitbox.y:.1f} vel_y={self.velocity_y:.1f}')
        # self.apply_gravity()
        # print(f'SAU gravity: x={self.hitbox.x:.1f}  y={self.hitbox.y:.1f} vel_y={self.velocity_y:.1f}')

        # self.check_vertical_collisions(platforms)
        # print(f'SAU vertical_collision: x={self.hitbox.x:.1f} y={self.hitbox.y:.1f} vel_y={self.velocity_y:.1f} on_ground={self.on_ground}')

        self.get_status()
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        #Vẽ hitbox
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
        #vẽ attack_hitbox
        attack_hitbox = self.get_attack_hitbox()
        if attack_hitbox:
            pygame.draw.rect(screen, (255, 255, 0), attack_hitbox, 2)