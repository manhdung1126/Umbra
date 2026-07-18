import pygame
from support import import_sprite_sheet

class Enemy:
    def __init__(self, x, y, patrol_range = 150):
        self.font = pygame.font.SysFont(None, 24)
        self.import_assets()
        self.status = 'walk'
        self.frame_index = 0
        self.animation_speed = 0.1
        self.animation_speed_attack = 0.12
        self.animation_speed_death = 0.08
        self.image = self.animations[self.status][int(self.frame_index)]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hitbox = pygame.Rect(0, 0, 140, 160)  
        self.hitbox.midbottom = self.rect.midbottom
        self.max_health = 50
        self.health = self.max_health
        self.alive = True

        self.attacking = False
        self.cooldown = 2000
        self.attack_time = 0
        self.attack_range = 100
        self.attack_damage = 15
        self.player_already_hit = False

        self.hurt = False

        self.direction = 1
        self.facing_right = True

        self.velocity_y = 0
        self.gravity = 0.6
        self.on_ground = False

        #Tuần tra
        self.patrol_left_bound = x - patrol_range
        self.patrol_right_bound = x + patrol_range + 200
        self.speed = 1
        self.chase_speed = 2
        self.state = 'patrol'      
        self.notice_radius = 250  
        self.give_up_radius = 400


    
    def import_assets(self):
        FRAME_WIDTH = 90
        FRAME_HEIGHT = 64
        SCALE = 4
        self.animations = {
            'idle' : import_sprite_sheet('graphics/golem/Idle.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'walk' : import_sprite_sheet('graphics/golem/Walk.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'hurt' : import_sprite_sheet('graphics/golem/Hurt.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'death' : import_sprite_sheet('graphics/golem/Death.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'attack' : import_sprite_sheet('graphics/golem/Attack.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
        }
    
    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y

    def check_collision(self, platforms):
        collided = False
        for platform in platforms:
            if not self.hitbox.colliderect(platform):
                continue

            overlap_x = min(self.hitbox.right, platform.right) - max(self.hitbox.left, platform.left)
            overlap_y = min(self.hitbox.bottom, platform.bottom) - max(self.hitbox.top, platform.top)

            if overlap_x < overlap_y:
                if self.direction > 0:
                    self.hitbox.right = platform.left
                elif self.direction < 0:
                    self.hitbox.left = platform.right
                collided = True
        return collided

    def check_vertical_collisions(self, platforms):
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
    
    def get_distance_to_player(self, player):
        enemy_pos = pygame.math.Vector2(self.hitbox.center)
        player_pos = pygame.math.Vector2(player.hitbox.center)
        return enemy_pos.distance_to(player_pos) - 40
    
    def get_distance_horizontal_to_player(self, player):
        return abs(self.hitbox.centerx - player.hitbox.centerx)
    
    def is_the_same_level_with_player(self, player, max_gap_y = 50):
        return abs(player.hitbox.bottom - self.hitbox.bottom) <= max_gap_y
    
    def has_path_to_player(self, player, platforms):
        left = min(self.hitbox.centerx, player.hitbox.centerx)
        right = max(self.hitbox.centerx, player.hitbox.centerx)
        gap = pygame.Rect(left, self.hitbox.top + 1, max(1, right - left), self.hitbox.height - 2)
        return not any(gap.colliderect(platform) for platform in platforms)
    
    def can_interact_with_player(self, player, platforms):
        return (self.is_the_same_level_with_player(player) and self.has_path_to_player(player, platforms))
    
    def update_state(self, player, platforms):
        distance_x = self.get_distance_horizontal_to_player(player)
        can_interact = self.can_interact_with_player(player, platforms)

        if self.state == 'patrol' and can_interact and distance_x <= self.notice_radius :
            self.state = 'chase'
            self.animation_speed *= 2
        elif self.state == 'chase' and (not can_interact or distance_x >= self.give_up_radius):
            self.state = 'patrol'
            self.animation_speed *= 1/2

    def get_status(self, player, platforms):
        if not self.alive:
            return
        
        if self.hurt:
            self.status = 'hurt'
            return
        
        if self.state == 'attack':
            self.status = 'attack'
            return
        
        distance = self.get_distance_to_player(player)
        current_time = pygame.time.get_ticks()
        if (self.can_interact_with_player(player, platforms) and distance <= self.attack_range
            and current_time - self.attack_time >= self.cooldown):
            self.state = 'attack'
            self.attacking = True
            self.attack_time = current_time
            self.frame_index = 0
            self.player_already_hit = False
            return
        
        if self.state == 'chase':
            distance_x = abs(player.hitbox.centerx - self.hitbox.centerx) - 40
            stop_distance = self.attack_range - 5
            
            if distance_x > stop_distance:
                self.status = 'walk'
            else:
                self.status = 'idle'
                
        elif self.state == 'patrol':
            self.status = 'walk'

    def patrol(self):
        self.hitbox.x += self.direction * self.speed

        if self.hitbox.x <= self.patrol_left_bound:
            self.direction = 1
            self.facing_right = True
        elif self.hitbox.x >= self.patrol_right_bound:
            self.direction = -1
            self.facing_right = False

    def chase_player(self, player):
        if player.hitbox.centerx > self.hitbox.centerx:
            self.direction = 1
            self.facing_right = True
        else:
            self.direction = -1
            self.facing_right = False

        distance_x = abs(player.hitbox.centerx - self.hitbox.centerx) - 40
        stop_distance = self.attack_range - 5


        if distance_x > stop_distance:
            self.hitbox.x += self.direction * self.chase_speed

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.status = 'death'
        else:
            self.hurt = True
            self.attacking = False
            self.frame_index = 0

    # def attack(self):
    #     current_time = pygame.time.get_ticks()
    #     if not self.attacking and current_time - self.attack_time >= self.cooldown:
    #         self.attacking = True
    #         self.attack_time = current_time
    #         self.frame_index = 0
    #         self.player_already_hit = False

    def get_attack_hitbox(self):
        if not self.attacking:
            return None
        
        current_frame = int(self.frame_index)
        if current_frame not in [7]:
            return None

        attack_width = 150
        attack_height = 80

        if self.facing_right:
            attack_hitbox = pygame.Rect(self.hitbox.right - 80, 
                                        self.hitbox.centery,
                                        attack_width, attack_height
                                        )
        else :
            attack_hitbox = pygame.Rect(self.hitbox.left - attack_width + 80, 
                                        self.hitbox.centery,
                                        attack_width, attack_height
                                        )
        
        return attack_hitbox

    def animate(self):
        animation = self.animations[self.status]

        if 'attack' in self.status:
            self.frame_index += self.animation_speed_attack
        elif self.status == 'death':
            self.frame_index += self.animation_speed_death
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

        if not self.facing_right:
            image = pygame.transform.flip(image, True, False)

        self.image = image
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)


    def update(self,solid_platforms, all_platforms, player):
        if not self.alive:
            self.animate()
            return

        self.update_state(player, all_platforms)
        

        if not self.hurt:
            if self.state == 'patrol':
                self.patrol()
            elif self.state == 'chase':
                if not self.attacking:  
                    self.chase_player(player)
        
        hit_wall = self.check_collision(solid_platforms)
        if hit_wall and self.state == 'patrol':
            self.direction *= -1
            self.facing_right = self.direction > 0
        
        self.check_vertical_collisions(all_platforms)
        self.apply_gravity()
        

        self.get_status(player, all_platforms)
        self.animate()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.alive:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2) 

            # Attack Range (vòng tròn xanh nhạt)
            pygame.draw.circle(screen, (0, 255, 100, 80), self.hitbox.center, self.attack_range, 2)

            # Attack Hitbox (nếu đang attack - màu vàng)
            attack_hitbox = self.get_attack_hitbox()
            if attack_hitbox:
                pygame.draw.rect(screen, (255, 255, 0), attack_hitbox, 3)

            # Hiển thị cả State (Quyết định AI) và Status (Hoạt ảnh)
            debug_text = self.font.render(f"{self.state} | {self.status}", True, (255, 255, 255))
            # Căn giữa dòng chữ và đặt nó cao hơn thanh máu một chút (y - 15)
            text_rect = debug_text.get_rect(midbottom=(self.hitbox.centerx, self.hitbox.y - 15))
            
            # Vẽ một viền đen mờ lót dưới chữ để dễ đọc nếu nền game sáng
            bg_rect = text_rect.copy()
            bg_rect.inflate_ip(4, 4)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)
            
            # Vẽ chữ lên màn hình
            screen.blit(debug_text, text_rect)

            #Thanh máu nhỏ phía trên đầu quái
            bar_width = self.hitbox.width
            bar_height = 6
            bar_x = self.hitbox.x
            bar_y = self.hitbox.y - bar_height - 4

            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
