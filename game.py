import pygame
from player import *
from map import *
from user_interface import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("Adventure Game")
pygame.mouse.set_visible(False)

# creates spritesheet to gather sprites
sprite_sheet = pygame.image.load('characters/sprites/roguelikeChar_transparent.png').convert_alpha()

# creates a surface that can be modified for zoom function
game_surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()

# creates background
grass = Tiles()

# create a border of trees around the map
tree = Tree() 

# create a variety of buildings on the map
building_group = pygame.sprite.Group()
villager_group = pygame.sprite.Group()
guard_group = pygame.sprite.Group()
create_buildings(building_group, villager_group, guard_group, player_speed)

# creates player centered in the map
player = Player(player_speed, building_group)
player_group = pygame.sprite.Group()
player_group.add(player)

# creates items
item_group = pygame.sprite.Group()
create_items(item_group, building_group, villager_group, guard_group, player_group)

start = Start()
score = Score()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('black')
   
    # RENDER YOUR GAME HERE

    # creates a camera function to keep player centered and move other sprites and backgrounds
    camera_x = player.map_x - WIDTH/2
    camera_y = player.map_y - HEIGHT/2

    # changes the surface size based on the zoom scale and blits it to the screen.
    zoomed_surface = pygame.transform.scale(game_surface, (int(WIDTH * zoom_level), int(HEIGHT * zoom_level)))
    zoom_rect = zoomed_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(zoomed_surface, zoom_rect)
    
    # functions
    player.keys()

    # drawing
    grass.draw(game_surface, camera_x, camera_y)
    tree.draw(game_surface, camera_x, camera_y)
    for building in building_group:
        building.draw(game_surface, camera_x, camera_y)
    for villager in villager_group:
        villager.draw(game_surface, camera_x, camera_y)
        villager.update(player_group, villager_group, guard_group)
    for guard in guard_group:
        guard.draw(game_surface, camera_x, camera_y)
        guard.update(player_group, guard_group)
    for items in item_group:
        items.draw(game_surface, camera_x, camera_y)
        items.update()
    player.draw(game_surface)
    player.update()

    # title
    score.draw(screen)
    score.update_score(player.score)
    start.update()
    start.draw(screen)
    
    # flip() the display to put your work on the screen
    pygame.display.flip()
    
    # limits FPS to 60
    clock.tick(60)

pygame.quit()