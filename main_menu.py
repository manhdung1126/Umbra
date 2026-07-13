import pygame
from main_menu_animation import MenuBackgroundAnimation


class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.background = MenuBackgroundAnimation(width, height)

        self.start_button_img = pygame.image.load('graphics/main_menu/Start Button.png').convert_alpha()
        self.start_button_img = pygame.transform.scale(self.start_button_img, (400, 200))

        self.start_button_rect = self.start_button_img.get_rect(
            center=(self.width // 2, self.height // 2 + 100)
        )

        self.hover_scale = 1.1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.start_button_rect.collidepoint(event.pos):
                    return True
        return False

    def update(self):
        self.background.update()

        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering = self.start_button_rect.collidepoint(mouse_pos)

    def draw(self, screen):
        self.background.draw(screen)

        if getattr(self, 'is_hovering', False):
            w = int(self.start_button_img.get_width() * self.hover_scale)
            h = int(self.start_button_img.get_height() * self.hover_scale)
            scaled_img = pygame.transform.scale(self.start_button_img, (w, h))
            scaled_rect = scaled_img.get_rect(center=self.start_button_rect.center)
            screen.blit(scaled_img, scaled_rect)
        else:
            screen.blit(self.start_button_img, self.start_button_rect)