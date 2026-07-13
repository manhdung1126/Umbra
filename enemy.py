import pygame
from support import import_sprite_sheet

class Enemy:
    def __init__(self, x, y, patrol_range = 150):
        self.hitbox = pygame.Rect(x, y, 48, 64)
        self.max_health = 100
        self.health = self.max_health
        self.alive = True

        self.attacking = False
        self.cooldown = 500
        self.attack_time = 0

        self.direction = pygame.math.Vector2()
        self.facing_right = True

        self.velocity_y = 0
        self.gravity = 0.6
        self.on_ground = False

        # --- Tuần tra ---
        self.patrol_left_bound = x - patrol_range
        self.patrol_right_bound = x + patrol_range
        self.direction.x = 1
        self.speed = 1.5
        self.chase_speed = 2
        self.state = 'patrol'      
        self.notice_radius = 250  
        self.give_up_radius = 400

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def get_distance_to_player(self, player):
        enemy_pos = pygame.math.Vector2(self.hitbox.center)
        player_pos = pygame.math.Vector2(player.hitbox.center)
        return enemy_pos.distance_to(player_pos)
    
    def update_state(self, player):
        """Quyết định chuyển trạng thái dựa trên khoảng cách tới người chơi."""
        distance = self.get_distance_to_player(player)

        if self.state == 'patrol' and distance <= self.notice_radius:
            self.state = 'chase'
        elif self.state == 'chase' and distance >= self.give_up_radius:
            self.state = 'patrol'

    def patrol(self):
        self.hitbox.x += self.direction.x * self.speed

        if self.hitbox.x <= self.patrol_left_bound:
            self.direction.x = 1
        elif self.hitbox.x >= self.patrol_right_bound:
            self.direction.x = -1

    def chase_player(self, player):
        """Di chuyển theo hướng người chơi (chỉ trục X, giữ đơn giản cho platformer)."""
        if player.hitbox.centerx > self.hitbox.centerx:
            self.direction = 1
        else:
            self.direction = -1

        self.hitbox.x += self.direction * self.chase_speed

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.hitbox.y += self.velocity_y

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
    
    def update(self, platforms, player):
        self.update_state(player)

        if self.state == 'patrol':
            self.patrol()
        elif self.state == 'chase':
            self.chase_player(player)

        self.apply_gravity()
        self.check_vertical_collisions(platforms)

    def draw(self, screen):
        # Màu đỏ nhạt = quái thường, có thể đổi màu tối hơn khi máu thấp (polish sau)
        pygame.draw.rect(screen, '#c23b3b', self.hitbox)

        # --- Thanh máu nhỏ phía trên đầu quái ---
        bar_width = self.hitbox.width
        bar_height = 6
        bar_x = self.hitbox.x
        bar_y = self.hitbox.y - bar_height - 4

        health_ratio = self.health / self.max_health
        pygame.draw.rect(screen, (60, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
