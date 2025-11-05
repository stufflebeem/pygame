# Example file showing a basic pygame "game loop"|
import pygame
from game_data import *
from player import *
from map import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Adventure Game")

# creates spritesheet to gather sprites
sprite_sheet = pygame.image.load('characters/sprites/roguelikeChar_transparent.png').convert_alpha()
items = Items(sprite_sheet)

# creates a surface that can be modified for zoom function
game_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()

# creates background
grass = Tiles()
fortress = Castle()


# creates player robert centered in the map
robert = Player(items, (map_width*tile_size)/2, (map_height*tile_size)/2, player_speed)

# create a variety of houses on the map
houses_group = pygame.sprite.Group()
for _ in range (5):
     houses_group.add(House(brick_house))
for _ in range (5):
     houses_group.add(House(stone_house))
tree = Tree() 

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
   
    # RENDER YOUR GAME HERE

    # creates a camera function to keep player centered and move other sprites and backgrounds
    camera_x = robert.world_x - WIDTH/2
    camera_y = robert.world_y - HEIGHT/2

    # changes the surface size based on the zoom scale and blits it to the screen.
    zoomed_surface = pygame.transform.scale(game_surface, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))
    zoom_rect = zoomed_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(zoomed_surface, zoom_rect)
    
    # functions
    robert.keys()

    # allows the zoom to be changed by using the + and - keys
   
    
    # drawing
    grass.draw(game_surface, camera_x, camera_y)
    tree.draw(game_surface, camera_x, camera_y)
    for house in houses_group:
        house.draw(game_surface, camera_x, camera_y)
    fortress.draw(game_surface, camera_x, camera_y)
    robert.draw(game_surface)
    
    # flip() the display to put your work on the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()