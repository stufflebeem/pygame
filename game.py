# Example file showing a basic pygame "game loop"|
import pygame
from sprites import get_sprite, Player, Items, Tiles

# pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# loads sprite sheet
sprite_sheet = pygame.image.load('characters/sprites/roguelikeChar_transparent.png').convert_alpha()

# creates player robert
robert = Player(int(WIDTH/2), int(HEIGHT/2), 1)
robert.player_frame(sprite_sheet, 0, 0)

# creates background
grass = Tiles()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
    # RENDER YOUR GAME HERE

    # functions
    robert.adjust_speed()
    robert.keys()
    camera_x = robert.world_x - WIDTH/2
    camera_y = robert.world_y - HEIGHT/2

    # drawing
    grass.draw(screen, camera_x, camera_y)
    robert.draw(screen, WIDTH/2, HEIGHT/2)

    # flip() the display to put your work on the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()