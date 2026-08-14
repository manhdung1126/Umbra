import pygame
from enemy import Enemy

class Boss(Enemy):
    def __init__(self, x, y, max_health=1000):
        super().__init__(x, y, patrol_range=0)
        self.max_health = max_health
        self.health = self.max_health
        self.give_up_radius = float('inf')

        self.max_poise = 200
        self.poise = self.max_poise
        self.poise_recovery_time = 0 
        self.poise_cooldown = 3000

    def patrol(self):
        pass

    def take_damage(self, amount, poise_damage=35):
        self.health -= amount
        
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.status = 'death'
            self.attacking = False
            if hasattr(self, 'casting'):
                self.casting = False
            return 

        self.poise -= poise_damage
        self.poise_recovery_time = pygame.time.get_ticks()

        if self.poise <= 0:
            self.hurt = True
            self.attacking = False
            if hasattr(self, 'casting'):
                self.casting = False
            self.frame_index = 0
            self.state = 'idle'
            self.poise = self.max_poise

    def update_poise(self):
        if self.poise < self.max_poise and not self.hurt:
            current_time = pygame.time.get_ticks()
            if current_time - self.poise_recovery_time > self.poise_cooldown:
                self.poise = self.max_poise

    def update(self, solid_platforms, all_platforms, player):
        if not self.alive:
            self.animate()
            return

        self.check_vertical_collisions(all_platforms)
        self.apply_gravity()

        self.update_poise()
    
    def draw(self, screen, cam_x, cam_y):
        draw_rect = self.rect.move(-cam_x, -cam_y)
        screen.blit(self.image, draw_rect)
        
        if self.alive:
            draw_hitbox = self.hitbox.move(-cam_x, -cam_y)
            pygame.draw.rect(screen, (255, 0, 0), draw_hitbox, 2) 

            center_x = self.hitbox.centerx - cam_x
            center_y = self.hitbox.centery - cam_y
            pygame.draw.circle(screen, (0, 255, 100, 80), (center_x, center_y), self.attack_range, 2)

            attack_hitbox = self.get_attack_hitbox()
            if attack_hitbox:
                draw_attack_hitbox = attack_hitbox.move(-cam_x, -cam_y)
                pygame.draw.rect(screen, (255, 255, 0), draw_attack_hitbox, 3)

        self.draw_boss_health_bar(screen)

    def draw_boss_health_bar(self, screen):
        if self.health <= 0 and not self.alive:
            return

        bar_width = 600
        bar_height = 20
        x = (screen.get_width() - bar_width) // 2
        y = screen.get_height() - 50

        health_ratio = max(0, self.health / self.max_health)

        # Viền ngoài
        pygame.draw.rect(screen, (50, 50, 50), (x - 4, y - 4, bar_width + 8, bar_height + 8))
        # Phần máu đã mất (Nền xám/đen)
        pygame.draw.rect(screen, (30, 30, 30), (x, y, bar_width, bar_height))
        # Phần máu hiện tại (Màu đỏ sẫm)
        pygame.draw.rect(screen, (200, 20, 20), (x, y, bar_width * health_ratio, bar_height))