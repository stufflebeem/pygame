# Example file showing a basic pygame "game loop"|
import pygame
from util_params import *
from item_data import *
from sprites import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# creates spritesheet to gather sprites
sprite_sheet = pygame.image.load('characters/sprites/roguelikeChar_transparent.png').convert_alpha()
items = Items(sprite_sheet)

# creates player robert
robert = Player(items, (WIDTH/2), (HEIGHT/2), 1, sprite_sheet, 0, 0)

# creates background
grass = Tiles('town/tiles/grass_green/tile_0001.png')

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
   
    # RENDER YOUR GAME HERE
    camera_x = robert.world_x - WIDTH/2
    camera_y = robert.world_y - HEIGHT/2
    
    # functions  
    robert.keys(grass)
  
    # drawing
    grass.draw(screen, camera_x, camera_y)
    robert.draw(screen)
    

    # flip() the display to put your work on the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()