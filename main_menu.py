import pygame
from main_menu_animation import MenuBackgroundAnimation


def load_scaled(path, box):
    img = pygame.image.load(path).convert_alpha()
    box_w, box_h = box
    img_w, img_h = img.get_size()
    scale = min(box_w / img_w, box_h / img_h)
    new_size = (max(1, int(img_w * scale)), max(1, int(img_h * scale)))
    return pygame.transform.scale(img, new_size)


def draw_button(screen, img, rect, is_hovering, hover_scale):
    if is_hovering:
        w = int(img.get_width() * hover_scale)
        h = int(img.get_height() * hover_scale)
        scaled_img = pygame.transform.scale(img, (w, h))
        scaled_rect = scaled_img.get_rect(center=rect.center)
        screen.blit(scaled_img, scaled_rect)
    else:
        screen.blit(img, rect)


class MainMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.background = MenuBackgroundAnimation(width, height)

        start_box = (213, 45)
        quit_box = (171, 51)

        self.start_button_img = load_scaled(
            'graphics/main_menu/Start Button.png', start_box
        )
        self.quit_button_img = load_scaled(
            'graphics/main_menu/Quit Button.png', quit_box
        )

        self.start_button_rect = self.start_button_img.get_rect(
            center=(self.width // 2, self.height // 2 + 100)
        )
        self.quit_button_rect = self.quit_button_img.get_rect(
            center=(self.width // 2, self.height // 2 + 180)
        )

        self.hover_scale = 1.1
        self.is_hovering_start = False
        self.is_hovering_quit = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.start_button_rect.collidepoint(event.pos):
                    return 'start'
                if self.quit_button_rect.collidepoint(event.pos):
                    return 'quit'
        return None

    def update(self):
        self.background.update()

        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering_start = self.start_button_rect.collidepoint(mouse_pos)
        self.is_hovering_quit = self.quit_button_rect.collidepoint(mouse_pos)

    def draw(self, screen):
        self.background.draw(screen)

        draw_button(screen, self.start_button_img, self.start_button_rect, self.is_hovering_start, self.hover_scale)
        draw_button(screen, self.quit_button_img, self.quit_button_rect, self.is_hovering_quit, self.hover_scale)


class PauseMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        resume_box = (255, 45)
        quit_box = (171, 51)

        self.resume_button_img = load_scaled(
            'graphics/main_menu/Resume Button.png', resume_box
        )
        self.quit_button_img = load_scaled(
            'graphics/main_menu/Quit Button.png', quit_box
        )

        self.resume_button_rect = self.resume_button_img.get_rect(
            center=(width // 2, height // 2 - 70)
        )
        self.quit_button_rect = self.quit_button_img.get_rect(
            center=(width // 2, height // 2 + 10)
        )

        self.hover_scale = 1.1
        self.is_hovering_resume = False
        self.is_hovering_quit = False

        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.resume_button_rect.collidepoint(event.pos):
                    return 'resume'
                if self.quit_button_rect.collidepoint(event.pos):
                    return 'quit'
        return None

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering_resume = self.resume_button_rect.collidepoint(mouse_pos)
        self.is_hovering_quit = self.quit_button_rect.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        draw_button(screen, self.resume_button_img, self.resume_button_rect, self.is_hovering_resume, self.hover_scale)
        draw_button(screen, self.quit_button_img, self.quit_button_rect, self.is_hovering_quit, self.hover_scale)

class GameOverMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        restart_box = (297, 45)
        quit_box = (171, 51)

        self.restart_button_img = load_scaled(
            'graphics/main_menu/Restart Button.png', restart_box
        )
        self.quit_button_img = load_scaled(
            'graphics/main_menu/Quit Button.png', quit_box
        )

        self.restart_button_rect = self.restart_button_img.get_rect(
            center=(width // 2, height // 2 - 70)
        )
        self.quit_button_rect = self.quit_button_img.get_rect(
            center=(width // 2, height // 2 + 10)
        )

        self.hover_scale = 1.1
        self.is_hovering_restart = False
        self.is_hovering_quit = False

        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.restart_button_rect.collidepoint(event.pos):
                    return 'restart'
                if self.quit_button_rect.collidepoint(event.pos):
                    return 'quit'
        return None

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering_restart = self.restart_button_rect.collidepoint(mouse_pos)
        self.is_hovering_quit = self.quit_button_rect.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.blit(self.overlay, (0, 0))
        draw_button(screen, self.restart_button_img, self.restart_button_rect, self.is_hovering_restart, self.hover_scale)
        draw_button(screen, self.quit_button_img, self.quit_button_rect, self.is_hovering_quit, self.hover_scale)