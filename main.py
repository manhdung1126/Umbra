import pygame
import sys
from player import Player
from enemy import Enemy
from main_menu import MainMenu

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

# Khởi tạo vật thể
player = None

platforms = [pygame.Rect(0, HEIGHT - 80, WIDTH, 80),
            pygame.Rect(300, 500, 200, 30),              
            pygame.Rect(600, 380, 200, 30),
            pygame.Rect(900, HEIGHT - 280, 40, 200)]


enemies = [Enemy(700, HEIGHT - 80 - 64)]

def start_game():
    global player, game_state
    player = Player(100, 100)
    game_state = 'playing'

while running:
    #Xứ lý ấn nút 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == 'menu':
            if main_menu.handle_event(event):
                start_game()
        elif game_state == 'playing':      
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:   
                    player.jump()
                if event.key == pygame.K_u:
                    player.attack('attack1')
                if event.key == pygame.K_i:
                    player.attack('attack2')
                if event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
                
    # Update
    if game_state == 'menu':
        main_menu.update()
    elif game_state == 'playing':
        player.update(platforms, WIDTH) 
        
        for enemy in enemies:
            if enemy.alive:
                enemy.update(platforms, player)

        # Kiểm tra va chạm đòn tấn công
        attack_hitbox = player.get_attack_hitbox()
        if attack_hitbox:
            for enemy in enemies:
                if (enemy.alive and 
                    attack_hitbox.colliderect(enemy.hitbox) and 
                    enemy not in player.enemies_hit_attack):
                    enemy.take_damage(10)
                    player.enemies_hit_attack.add(enemy)
        
        # Xóa enemy chết
        enemies[:] = [e for e in enemies if e.alive]

    if game_state == 'menu':
        main_menu.draw(screen)
    elif game_state == 'playing':
        screen.fill('#1c1c2e')
        for platform in platforms:
            pygame.draw.rect(screen, WHITE, platform)
        player.draw(screen)

    #Draw (Render)
    if game_state == 'menu':
        main_menu.draw(screen)
    elif game_state == 'playing':
        screen.fill('#1c1c2e')
        for platform in platforms:
            pygame.draw.rect(screen, WHITE, platform)
        
        player.draw(screen)
        for enemy in enemies:
            if enemy.alive:
                enemy.draw(screen)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()