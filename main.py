import pygame
import sys
from player import Player
from main_menu import MainMenu

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

game_state = 'menu'

main_menu = MainMenu(WIDTH, HEIGHT)

# Khởi tạo vật thể
player = None

platforms = [pygame.Rect(0, HEIGHT - 80, WIDTH, 80),
            pygame.Rect(300, 500, 200, 30),              
            pygame.Rect(600, 380, 200, 30),
            pygame.Rect(900, HEIGHT - 280, 40, 200)]

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.jump()
            if event.key == pygame.K_u:
                player.attack()
            if event.key == pygame.K_ESCAPE:
                game_state = 'menu'
                
    if game_state == 'menu':
        main_menu.update()
    elif game_state == 'playing':
        player.update(platforms, WIDTH)

    if game_state == 'menu':
        main_menu.draw(screen)
    elif game_state == 'playing':
        screen.fill('#1c1c2e')
        for platform in platforms:
            pygame.draw.rect(screen, WHITE, platform)
        player.draw(screen)

    # player.update(platforms, WIDTH)
    # #RENDER
    # screen.fill('#1c1c2e')
    # for platform in platforms :
    #     pygame.draw.rect(screen, WHITE, platform)
    
    # player.draw(screen)

    

    pygame.display.update()
    
    clock.tick(FPS)

pygame.quit()
sys.exit()