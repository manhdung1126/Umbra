import pygame
import sys
from player import Player
from enemy import Enemy
from main_menu import MainMenu, PauseMenu, GameOverMenu

pygame.init()

HEIGHT = 900
WIDTH = 1440
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Umbra') 

clock = pygame.time.Clock()
running = True

game_state = 'menu'

main_menu = MainMenu(WIDTH, HEIGHT)
pause_menu = PauseMenu(WIDTH, HEIGHT)
game_over_menu = GameOverMenu(WIDTH, HEIGHT)

# Khởi tạo vật thể
player = None

platforms = [pygame.Rect(0, HEIGHT - 80, WIDTH, 80),
            pygame.Rect(300, 500, 200, 30),              
            pygame.Rect(600, 480, 200, 30),
            pygame.Rect(900, HEIGHT - 180, 40, 100)]


enemies = [Enemy(600,HEIGHT - 90*4), Enemy(500,HEIGHT - 90*4)]

def start_game():
    global player, enemies, game_state
    player = Player(100, 100)
    enemies = [Enemy(600, HEIGHT - 90*4), Enemy(500, HEIGHT - 90*4)]
    game_state = 'playing'

def draw_game_scene(screen):
    screen.fill('#1c1c2e')
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

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
        player.update(platforms, WIDTH)
        if not player.alive:
            for enemy in enemies:
                enemy.state = 'patrol'
                enemy.attacking = False
            if player.frame_index >= len(player.animations['death']) - 1:
                game_state = 'game_over'


        # Enemies
        for enemy in enemies[:]:   
            enemy.update(platforms, player)
            
            if not enemy.alive and enemy.status == 'death' and enemy.frame_index >= len(enemy.animations.get('death', [])) - 2:
                if enemy in enemies:
                    enemies.remove(enemy)

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