import pygame
import sys
from player import Player
from enemy import Enemy

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

# Khởi tạo vật thể
player = Player(100, 100)

platforms = [pygame.Rect(0, HEIGHT - 80, WIDTH, 80),
            pygame.Rect(300, 500, 200, 30),              
            pygame.Rect(600, 380, 200, 30),
            pygame.Rect(900, HEIGHT - 280, 40, 200)]

enemies = [Enemy(700, HEIGHT - 80 - 64)]

while running:
    #Xứ lý ấn nút 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_u:
                player.attack('attack1')
            if event.key == pygame.K_i:
                player.attack('attack2')
                
    player.update(platforms, WIDTH)
    for enemy in enemies:
        if enemy.alive:
            enemy.update(platforms, player)

    attack_hitbox = player.get_attack_hitbox()
    if attack_hitbox:
        for enemy in enemies:
            already_hit = enemy in player.enemies_hit_attack
            if enemy.alive and attack_hitbox.colliderect(enemy.hitbox) and not already_hit:
                enemy.take_damage(10)
                player.enemies_hit_attack.add(enemy)

    
    enemies = [e for e in enemies if e.alive]

    #RENDER
    screen.fill('#1c1c2e')
    for platform in platforms :
        pygame.draw.rect(screen, WHITE, platform)
    
    for enemy in enemies:
        enemy.draw(screen)
    
    player.draw(screen)

    

    pygame.display.update()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()