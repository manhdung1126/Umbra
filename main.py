import pygame
import sys
from player import Player
from enemy import Enemy
from ui import UI
from main_menu import MainMenu, PauseMenu, GameOverMenu
from tilemap import build_solid_rect_from_csv, get_map_size, load_csv_map, build_tile_cache, draw_tile_layer

pygame.init()

HEIGHT = 900
WIDTH = 1440
LEVEL_WIDTH, LEVEL_HEIGHT = get_map_size('Map/level1_solid.csv')
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Umbra') 

world_surface = pygame.Surface((LEVEL_WIDTH,LEVEL_HEIGHT))

clock = pygame.time.Clock()
running = True

game_state = 'menu'

main_menu = MainMenu(WIDTH, HEIGHT)
pause_menu = PauseMenu(WIDTH, HEIGHT)
game_over_menu = GameOverMenu(WIDTH, HEIGHT)

ui = UI(WIDTH, HEIGHT)


# Khởi tạo vật thể
player = None
enemies = []
camera_x = 0

solid_platforms = build_solid_rect_from_csv('Map/level1_solid.csv')
one_way_platforms = build_solid_rect_from_csv('Map/level1_oneway.csv')
all_platforms = solid_platforms + one_way_platforms

solid_grid = load_csv_map('Map/level1_solid.csv')
one_way_grid = load_csv_map('Map/level1_oneway.csv')

tile_cache = build_tile_cache('Map/Snow platform tileset.png')

def start_game():
    global player, enemies, game_state, camera_x, camera_y
    player = Player(0,528)
    enemies = [Enemy(1536, 960), Enemy(2114,624), Enemy(3482, 864), Enemy(5224,528)]
    camera_x = 0
    camera_y = 0
    game_state = 'playing'

def draw_game_scene(screen):
    world_surface.fill('#1c1c2e')
    draw_tile_layer(world_surface, solid_grid, tile_cache)
    draw_tile_layer(world_surface, one_way_grid, tile_cache)
    player.draw(world_surface)
    for enemy in enemies:
        enemy.draw(world_surface)
    screen.blit(world_surface,(-int(camera_x), -int(camera_y)))

def get_camera_offset(player, level_width, level_height, screen_width, screen_height):
    #Tính camera theo player và giữ camera trong biên level.
    camera_x = player.hitbox.centerx - screen_width // 2
    camera_y = player.hitbox.centery - screen_height // 2

    max_camera_x = max(0, level_width - screen_width)
    max_camera_y = max(0, level_height - screen_height)

    camera_x = max(0, min(camera_x, max_camera_x))
    camera_y = max(0, min(camera_y, max_camera_y))

    return camera_x, camera_y

while running:
    #Xứ lý ấn nút 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == 'menu':
            action = main_menu.handle_event(event)
            if action == 'start':
                start_game()
            elif action == 'quit':
                running = False

        elif game_state == 'playing':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                    player.jump()
                if event.key == pygame.K_u:
                    player.attack('attack1')
                if event.key == pygame.K_i:
                    player.attack('attack2')
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
                if event.key == pygame.K_j:
                    player.dash()
                if event.key == pygame.K_p:
                    game_state = 'paused'

        elif game_state == 'paused':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                game_state = 'playing'

            action = pause_menu.handle_event(event)
            if action == 'resume':
                game_state = 'playing'
            elif action == 'quit':
                game_state = 'menu'

        elif game_state == 'game_over':
            action = game_over_menu.handle_event(event)
            if action == 'restart':
                start_game()
            elif action == 'quit':
                game_state = 'menu'
                
    # Update
    if game_state == 'menu':
        main_menu.update()
    elif game_state == 'playing':
        
        # Player
        player.update(solid_platforms, all_platforms, LEVEL_WIDTH)
        if not player.alive:
            for enemy in enemies:
                enemy.state = 'patrol'
                enemy.attacking = False
            if player.frame_index >= len(player.animations['death']) - 1:
                game_state = 'game_over'


        # Enemies
        for enemy in enemies[:]:   
            enemy.update(solid_platforms, all_platforms, player)
            
            if not enemy.alive and enemy.status == 'death' and enemy.frame_index >= len(enemy.animations.get('death', [])) - 2:
                if enemy in enemies:
                    enemies.remove(enemy)

        # Camera 
        target_x, target_y = get_camera_offset(player, LEVEL_WIDTH, LEVEL_HEIGHT, WIDTH, HEIGHT)

        camera_x += (target_x - camera_x) * 0.12
        camera_y += (target_y - camera_y) * 0.12

        # Kiểm tra va chạm đòn tấn công
        if player.alive:
            attack_hitbox = player.get_attack_hitbox()
            if attack_hitbox:
                for enemy in enemies:
                    if (enemy.alive and 
                        attack_hitbox.colliderect(enemy.hitbox) and 
                        enemy not in player.enemies_hit_attack):
                        enemy.take_damage(10)
                        player.enemies_hit_attack.add(enemy)

        for enemy in enemies:
            if enemy.alive:
                enemy_attack_hitbox = enemy.get_attack_hitbox()
                if enemy_attack_hitbox and not enemy.player_already_hit:
                    if enemy_attack_hitbox.colliderect(player.hitbox):
                        player.take_damage(enemy.attack_damage)
                        enemy.player_already_hit = True
        
        # Xóa enemy chết
        # enemies[:] = [e for e in enemies if e.alive]
    elif game_state == 'paused':
        pause_menu.update()

    elif game_state == 'game_over':
        game_over_menu.update()

    #Draw (Render)
    if game_state == 'menu':
        main_menu.draw(screen)
    elif game_state == 'playing':
        draw_game_scene(screen)
        ui.draw_health_bar(screen, player.health, player.max_health)
    elif game_state == 'paused':
        draw_game_scene(screen)
        pause_menu.draw(screen)

    elif game_state == 'game_over':
        draw_game_scene(screen)
        game_over_menu.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()