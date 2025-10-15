# Example file showing a basic pygame "game loop"|
import pygame
from sprites import get_sprite, Player

# pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# loads sprite sheet
sprite_sheet = pygame.image.load('characters/sprites/roguelikeChar_transparent.png').convert_alpha()
player_speed = 1

# creates player robert
robert = Player(int(WIDTH/2), int(HEIGHT/2),  player_speed)
robert.player_frame(sprite_sheet, 0, 0)
robert.draw(screen)

# creates background
grass_tile_location = pygame.image.load('town/tiles/tile_0001.png').convert_alpha()
grass_tile = get_sprite(grass_tile_location,0,0,16,16)
background = pygame.Surface((WIDTH,HEIGHT))

# repeats tile for every tile length
for x in range(0,WIDTH,16):
    for y in range(0,HEIGHT,16):
        background.blit(grass_tile,(x,y))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

     # render background to clear last frame
    screen.blit(background,(0,0))

    # RENDER YOUR GAME HERE

    # render character
    robert.keys()
    robert.speed()
    robert.draw(screen)
    
    # flip() the display to put your work on the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()