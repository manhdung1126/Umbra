import pygame

class Spell:
    def __init__(self, x, ground_y, animations, damage, hit_frames, width, height):
        self.animations = animations
        self.frame_index = 0
        self.hit_frames = hit_frames
        self.animation_speed = 0.3
        self.finished = False
        self.player_already_hit = False
        self.damage = damage

        self.x = x
        self.ground_y = ground_y
        self.width = width
        self.height = height
        self.image = self.animations[0]
        self.rect = self.image.get_rect(midbottom=(self.x, self.ground_y))

    def get_hitbox(self):
        current_frames = int(self.frame_index)
        if current_frames not in self.hit_frames:
            return None
        hitbox = pygame.Rect(0, 0, self.width, self.height)
        hitbox.midbottom = (self.x, self.ground_y)
        return hitbox

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations):
            self.finished = True
            return
        self.image = self.animations[int(self.frame_index)]
        self.rect = self.image.get_rect(midbottom=(self.x, self.ground_y))

    def draw(self, screen, cam_x, cam_y):
        draw_rect = self.rect.move(-cam_x, -cam_y)
        screen.blit(self.image, draw_rect)

    