import pygame
from game_data import *
from map import *

# fuction to extracts sprites from spritesheet
def get_sprite(sheet, x, y, width, height):
    """extracts sprites from a spritesheet where:
    sheet: loaded sprite image sheet
    x: X coordinate of top-left corner of sprite
    y: Y coordinate of top-left corner of sprite
    width: width of the sprite
    height: height of the sprite"""
   
    # creates surface space for the sprite
    sprite_image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
   
    # blits desired sprite onto the new surface
    sprite_image.blit(sheet, (0,0), (x, y, width, height))
    
    return sprite_image

# creates a class of sprite Player for the user to control
class Player(pygame.sprite.Sprite):
    def __init__(self, items, speed, building_group):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.world_x = (map_width*tile_size)/2
        self.world_y = (map_height*tile_size)/2
        self.speed = speed
        self.items = items
        self.building_group = building_group

        # creates a transparent surface for the sprite
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(center=(self.world_x, self.world_y))

        # blits the player sprite onto transparant surface
        blit_list = [model, pants,boots,shirt, hair, helmet, 
                     shield, weapon]
        for b in blit_list:
           sprite = self.items.load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

        # adjusts spawn location in case of spawning in building
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.world_x += 100
            self.world_y += 100
            self.rect.center = (self.world_x, self.world_y)

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn"""
        surface.blit(self.image, (WIDTH/2, HEIGHT/2))
        
    # takes keystroke inputs and changes the position of the sprite on the map relative to the speed
    def keys(self):

        # detects and saves a key input
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        # acts based on key input to move the sprite around the screen with WASD and arrows
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.world_x > 0 + WIDTH/(2*zoom_level)+10:
            if (keys[pygame.K_LSHIFT]):
                dx -= self.speed+1
            else:
                dx -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.world_x < map_width * tile_size - WIDTH/(2*zoom_level)-10:
            if (keys[pygame.K_LSHIFT]):
                dx += self.speed+1
            else:
                dx += self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.world_y < map_height * tile_size - HEIGHT/(2*zoom_level)-10:
            if (keys[pygame.K_LSHIFT]):
                dy += self.speed+1
            else:
                dy += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.world_y > 0 + HEIGHT/(2*zoom_level)+10:
            if (keys[pygame.K_LSHIFT]):
               dy -= self.speed+1
            else:
                dy -= self.speed

        # checks ability to move in the x direction
        self.world_x += dx
        self.rect.center = (self.world_x, self.world_y)
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.world_x -= dx
            self.rect.center = (self.world_x, self.world_y)

        # checks ability to move in the y direction
        self.world_y += dy
        self.rect.center = (self.world_x, self.world_y)
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.world_y -= dy
            self.rect.center = (self.world_x, self.world_y)
        

# creates a class of Items for the Player and others to wear and use
class Items():
    def __init__(self, sprite_sheet):
        """sprite_sheet: the png sheet with extractable sprites"""
        self.sprite_sheet = sprite_sheet
    def load_items(self, name):
        """name: dictionary key name for what item is to be loaded"""
        data = item_data[name]
        x,y = data["pos"]
        sprite = get_sprite(self.sprite_sheet, x, y, 16, 16)
        return {"name":name, "sprite":sprite,"category":data["category"], "stats":data["stats"]}
    

    
