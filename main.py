import pygame
import sys
from player import Player

pygame.init()

HEIGHT = 720
WIDTH = 1280
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Frostbound: The Last Vanguard') 

clock = pygame.time.Clock()
running = True

# Khởi tạo vật thể
player = Player(100, 100)

platforms = [pygame.Rect(0, HEIGHT - 80, WIDTH, 80),
            pygame.Rect(300, 500, 200, 30),              
            pygame.Rect(600, 380, 200, 30),
            pygame.Rect(900, HEIGHT - 280, 40, 200)]

while running:
    #Xứ lý ấn nút 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_u:
                player.attack()
                
    player.update(platforms, WIDTH)
    #RENDER
    screen.fill('#1c1c2e')
    for platform in platforms :
        pygame.draw.rect(screen, WHITE, platform)
    
    player.draw(screen)

    

    pygame.display.update()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()