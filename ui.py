import pygame

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 20, bold=True) 
        scale = 2

        # player health bar
        p_bar = pygame.image.load('graphics/ui/player_bar.png').convert_alpha()
        p_health = pygame.image.load('graphics/ui/player_health.png').convert_alpha()
        
        self.p_total_w = p_bar.get_width() * scale
        self.p_total_h = p_bar.get_height() * scale
        self.p_bar = pygame.transform.scale(p_bar, (self.p_total_w, self.p_total_h))
        self.p_health = pygame.transform.scale(p_health, (self.p_total_w, self.p_total_h))
        
        self.player_pos = (20, 20)
        self.p_empty_offset = int(self.p_health.get_width() * 0.28)

        # lives
        heart_bg = pygame.image.load('graphics/ui/background.png').convert_alpha()
        heart_border = pygame.image.load('graphics/ui/border.png').convert_alpha()
        heart_full = pygame.image.load('graphics/ui/heart.png').convert_alpha()
        heart_w = heart_bg.get_width() * scale
        heart_h = heart_bg.get_height() * scale

        self.heart_background = pygame.transform.scale(heart_bg, (heart_w, heart_h))
        self.heart_border = pygame.transform.scale(heart_border, (heart_w, heart_h))
        self.heart_full = pygame.transform.scale(heart_full, (heart_w, heart_h))

        self.heart_size = (heart_w, heart_h)
        self.heart_spacing = 8
        self.lives_pos = (
            self.player_pos[0] + 60,
            self.player_pos[1] + self.p_total_h,
        )

        # boss health bar
        b_bar = pygame.image.load('graphics/ui/bossbar.png').convert_alpha()
        b_health = pygame.image.load('graphics/ui/bosshealth.png').convert_alpha()
        
        self.b_total_w = b_bar.get_width() * scale
        self.b_total_h = b_bar.get_height() * scale
        self.b_bar = pygame.transform.scale(b_bar, (self.b_total_w, self.b_total_h))
        self.b_health = pygame.transform.scale(b_health, (self.b_total_w, self.b_total_h))
        
        self.boss_pos = (self.width - self.b_total_w - 20, 20)
        
        # Tỉ lệ khu vực của thanh máu rồng
        self.b_head_ratio = 0.18
        self.b_bar_ratio = 0.78

    def draw_health_bar(self, screen, current_health, max_health):
        ratio = max(current_health / max_health, 0)
        screen.blit(self.p_bar, self.player_pos)
        
        total_w = self.p_health.get_width()
        total_h = self.p_health.get_height()
        
        # Tính toán khu vực cần cắt của lớp máu xanh ngọc
        fillable_w = total_w - self.p_empty_offset # Lọc bỏ phần trống của trái tim
        crop_width = self.p_empty_offset + int(fillable_w * ratio) # Tổng pixel ngang cần giữ lại
        
        if crop_width > 0:
            crop_rect = pygame.Rect(0, 0, crop_width, total_h)
            cropped_img = self.p_health.subsurface(crop_rect)
            screen.blit(cropped_img, self.player_pos)
            
        health_text = f"HP: {int(current_health)}/{int(max_health)}"
        text_surf = self.font.render(health_text, True, (75, 180, 165))
        text_rect = text_surf.get_rect(midleft=(self.player_pos[0] + total_w + 10, self.player_pos[1] + total_h // 2))
        screen.blit(text_surf, text_rect)

    def draw_lives(self, screen, current_lives, lives):
        x, y = self.lives_pos
        heart_w = self.heart_size[0]

        for i in range(lives):
            heart_x = x + i * (heart_w + self.heart_spacing)

            screen.blit(self.heart_background, (heart_x, y))
            if i < current_lives:
                screen.blit(self.heart_full, (heart_x, y))
            screen.blit(self.heart_border, (heart_x, y))

    def draw_boss_health(self, screen, current_health, max_health):
        screen.blit(self.b_bar, self.boss_pos)
        ratio = max(current_health / max_health, 0)
        head_w = int(self.b_total_w * self.b_head_ratio)
        red_w = int(self.b_total_w * self.b_bar_ratio * ratio)
        crop_width = head_w + red_w 
        
        if crop_width > 0:
            crop_rect = pygame.Rect(0, 0, crop_width, self.b_total_h)
            cropped_img = self.b_health.subsurface(crop_rect)
            screen.blit(cropped_img, self.boss_pos)
            
        health_text = f"HP: {int(current_health)}/{int(max_health)}"
        text_surf = self.font.render(health_text, True, (255, 100, 100))
        text_rect = text_surf.get_rect(midright=(self.boss_pos[0] - 10, self.boss_pos[1] + self.b_total_h // 2))
        screen.blit(text_surf, text_rect)