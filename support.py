import pygame

def import_sprite_sheet(path, frame_width, frame_heigth, scale = 1):
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_heigth = sheet.get_size()

    frame_count = sheet_width // frame_width
    frames = []

    for i in range(frame_count):
        x = i * frame_width
        frame_rect = pygame.Rect(x, 0, frame_width, frame_heigth)
        frame_surface = sheet.subsurface(frame_rect).copy()

        if scale != 1:
            new_size = (frame_width * scale, frame_heigth * scale)
            frame_surface = pygame.transform.scale(frame_surface, new_size)
        
        frames.append(frame_surface)

    return frames