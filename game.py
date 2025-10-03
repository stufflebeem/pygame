# Example file showing a basic pygame "game loop"|
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()
running = True

sprite_sheet = pygame.image.load("roguelikeChar_transparent.png").convert_alpha()
def get_sprite(sheet, x, y, width, height):
    """extracts sprites from the roguelikeChar_transparent.png where
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
# creates a class of sprite called Player
class Player(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
# positions the player sprite and loads him
player_sprite = Player(player_frame, 300, 200)
all_sprites = pygame.sprite.Group(player_sprite)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    # RENDER YOUR GAME HERE
    all_sprites.draw(screen)
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()