# Example file showing a basic pygame "game loop"|
import pygame

# pygame setup
pygame.init()
WIDTH = 600
HEIGHT = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# creates the spritesheet from roguelikeChar_transparent.png and allows you to pick different elements of 
sprite_sheet = pygame.image.load("roguelikeChar_transparent.png").convert_alpha()
def get_sprite(sheet, x, y, width, height):
    """extracts sprites from a spritesheet where:
    sheet: loaded sprite image sheet
    x: X coordinate of top-left corner of sprite
    y: Y coordinate of top-left corner of sprite
    width: Width of the sprite
    height: Height of the sprite"""
    # creates surface space for the sprite
    sprite_image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    # blits desired sprite onto the new surface
    sprite_image.blit(sheet, (0,0), (x, y, width, height))
    return sprite_image
# establishes the player sprite frame
player_frame = get_sprite(sprite_sheet, 0, 0, 16, 16)
#creates initial player x and y
player_x = int(WIDTH/2)
player_y = int(HEIGHT/2)
player_speed = 3
def player(x,y):
    screen.blit(player_frame, (player_x, player_y))

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE

    # Creates input for all input keys
    keys = pygame.key.get_pressed()
   
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player_y -= player_speed
    
    player(player_x,player_y)

    # flip() the display to put your work on the screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()