import pygame
from player import *
from orc import *
from map import *
from user_interface import *

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
paused = False
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
orc_group = pygame.sprite.Group()
create_buildings(building_group, villager_group, guard_group, orc_group)
create_orcs(building_group, villager_group, guard_group, orc_group)

# creates player centered in the map
player = Player(building_group, villager_group, guard_group, orc_group)
player_group = pygame.sprite.Group()
player_group.add(player)

# creates items
item_group = pygame.sprite.Group()
create_items(item_group, building_group, player_group)
start = Start()
score = Score()
game_over = Game_over()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
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
    if not paused:
        player.keys()
        if len(orc_group) == 0:
            level += 1
            create_orcs(building_group, villager_group, guard_group, orc_group)
            print(f"Level {level}")
        for villager in villager_group:
            villager.update(player_group)
        for guard in guard_group:
            guard.update(player_group) 
        for items in item_group:
            items.update()
        for orcs in orc_group:
            orcs.update(player_group)
        player.update()

    # drawing
    grass.draw(game_surface, camera_x, camera_y)
    tree.draw(game_surface, camera_x, camera_y)
    for building in building_group:
        building.draw(game_surface, camera_x, camera_y)
    for villager in villager_group:
        villager.draw(game_surface, camera_x, camera_y)
    for guard in guard_group:
        guard.draw(game_surface, camera_x, camera_y) 
    for items in item_group:
        items.draw(game_surface, camera_x, camera_y)
    for orcs in orc_group:
        orcs.draw(game_surface, camera_x, camera_y)
    player.draw(game_surface)


    # title
    score.draw(screen)
    score.update_score(player.score)
    start.update()
    start.draw(screen)
    pause(paused, screen)
    game_over.update(player_group)
    game_over.draw(screen)
    
    # flip() the display to put your work on the screen
    pygame.display.flip()
    
    # limits FPS to 60
    clock.tick(60)

pygame.quit()