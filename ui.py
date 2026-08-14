import pygame

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('arial', 28)
        self.font_large = pygame.font.SysFont('arial', 64)

        self.health_bar_width = 300
        self.health_bar_height = 30
        self.health_bar_pos = (20, 20)
        

    def draw_health_bar(self, screen, current_health, max_health):
        x, y = self.health_bar_pos
        health_ratio = max(current_health / max_health, 0)

        pygame.draw.rect(screen, (60, 0, 0), (x, y, self.health_bar_width, self.health_bar_height))
        pygame.draw.rect(screen, (200, 30, 30), (x, y, self.health_bar_width * health_ratio, self.health_bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, self.health_bar_width, self.health_bar_height), 3)

        health =  f"{int(current_health)}/{int(max_health)}"
        text_surf = self.font.render(health, True, (255, 255, 255))
        text_rect = text_surf.get_rect(midleft=(x + self.health_bar_width + 15, y + self.health_bar_height // 2))
        screen.blit(text_surf, text_rect)
