import pygame
from item_data import *
from util_params import *

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
class Player():
    def __init__(self, items, world_x, world_y, speed, sprite_sheet, x, y):
        """world_x: the x coordinate of the sprite on the map
           world_y: the y coordinate of the sprite on the map
           speed: the number of pixles the sprite moves per frame
           sprite_sheet: the sheet where the sprite is located
           x: the x coordinate of the sprite on the sprite sheet
           y: the y coordinate of the sprite on the sprite sheet"""
        self.world_x = world_x
        self.world_y = world_y
        self.speed = speed
        self.items = items
        self.sprite = get_sprite(sprite_sheet, x, y, 16, 16)

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn
           screen_x: the x coordinate of the sprite on the screen
           screen_y: the y coordinate of the sprite on the screen"""
        # blits the player sprite onto
        surface.blit(self.sprite, (WIDTH/2,HEIGHT/2))
        player_pants = self.items.load_items(pants)
        player_boots = self.items.load_items(boots)
        player_shirt = self.items.load_items(shirt)
        player_hair = self.items.load_items(hair)
        player_helmet = self.items.load_items(helmet)
        player_shield = self.items.load_items(shield)
        player_weapon = self.items.load_items(weapon)
        surface.blit(player_pants["sprite"],(WIDTH/2,HEIGHT/2))
        surface.blit(player_boots["sprite"],(WIDTH/2,HEIGHT/2))
        surface.blit(player_shirt["sprite"],(WIDTH/2,HEIGHT/2))
        surface.blit(player_helmet["sprite"],(WIDTH/2,HEIGHT/2))
        surface.blit(player_hair["sprite"],(WIDTH/2,HEIGHT/2))
        surface.blit(player_shield["sprite"],(WIDTH/2,HEIGHT/2))
        surface.blit(player_weapon["sprite"],(WIDTH/2,HEIGHT/2))

    def keys(self, tiles):
        """takes keystroke inputs and changes the position of the sprite on the map relative to
        the speed"""
        keys = pygame.key.get_pressed()

        map_width = tiles.map_width * tiles.tile_size
        map_height = tiles.map_height * tiles.tile_size
        sprite_size = 16

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.world_x > 0 + WIDTH/2:
            self.world_x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.world_x < map_width - WIDTH/2:
            self.world_x += self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.world_y < map_height - HEIGHT/2:
            self.world_y += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.world_y > 0 + HEIGHT/2:
            self.world_y -= self.speed
            """changes the speed of the sprite based on LSHIFT and LCRTL inputs"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed += 0.1
        if keys[pygame.K_LCTRL]:
            self.speed -= 0.1
        self.speed = abs(self.speed)
        

# Creates a class called tiles to create maps and backgrounds
class Tiles():
    def __init__(self, tile):
       """initializes the tile, creates variables for the map"""
       self.image = pygame.image.load(tile).convert_alpha()
       self.tile_size = 16
       self.map_width = 80
       self.map_height = 80

    def draw(self,surface, camera_x, camera_y):
        """draws the tiles on a surface the size of the map and shows the area visible on the screen"""
        for x in range(self.map_width):
            for y in range(self.map_height):
                tile_world_x = x * self.tile_size
                tile_world_y = y * self.tile_size
                screen_x = tile_world_x - camera_x
                screen_y = tile_world_y - camera_y
                surface.blit(self.image, (screen_x,screen_y))

# creates a class of Items for the Player and others to wear and use
class Items():
    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
    def load_items(self, name):
        data = item_data[name]
        x,y = data["pos"]
        sprite = get_sprite(self.sprite_sheet, x, y, 16, 16)
        return {"name":name, "sprite":sprite,"category":data["category"], "stats":data["stats"]}