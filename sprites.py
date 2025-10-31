import pygame
from game_data import *

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
    def __init__(self, items, world_x, world_y, speed):
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

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn
           screen_x: the x coordinate of the sprite on the screen
           screen_y: the y coordinate of the sprite on the screen"""
        # blits the player sprite onto
        blit_list = [model, pants,boots,shirt, hair, helmet, 
                     shield, weapon]
        for b in blit_list:
           sprite = self.items.load_items(b)
           surface.blit(sprite["sprite"],(WIDTH/2,HEIGHT/2))

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
       self.map_width = map_width
       self.map_height = map_height

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
    
# create a house
class House():
    def __init__(self):

        self.tile_size = 16
        self.house_width = 5
        self.house_height = 4
        self.wall = pygame.image.load("town/tiles/building_brick/tile_0073.png")
        self.wall_left = pygame.image.load("town/tiles/building_brick/tile_0072.png")
        self.wall_right = pygame.image.load("town/tiles/building_brick/tile_0075.png")
        self.door = pygame.image.load("town/tiles/building_brick/tile_0085.png")
        self.roof_top = pygame.image.load("town/tiles/roof_stone/tile_0049.png")
        self.roof_bottom = pygame.image.load("town/tiles/roof_stone/tile_0061.png")
        self.roof_left = pygame.image.load("town/tiles/roof_stone/tile_0060.png")
        self.roof_right = pygame.image.load("town/tiles/roof_stone/tile_0062.png")
        self.roof_left_corner = pygame.image.load("town/tiles/roof_stone/tile_0048.png")
        self.roof_right_corner = pygame.image.load("town/tiles/roof_stone/tile_0050.png")
        self.roof_arch = pygame.image.load("town/tiles/roof_stone/tile_0063.png")

    def draw_surface(self, surface):
        def draw_wall(surface):
            for x in range (1, self.house_width-1):
                for y in range(2, self.house_height):
                    surface_x = x * self.tile_size
                    surface_y = y * self.tile_size
                    surface.blit(self.wall, (surface_x, surface_y))
        def draw_wall_left(surface):
            for y in range(2, self.house_height):
                surface_x = 0 * self.tile_size
                surface_y = y * self.tile_size
                surface.blit(self.wall_left, (surface_x, surface_y))
        def draw_wall_right(surface):
            for y in range(2, self.house_height):
                surface_x = (self.house_width-1) * self.tile_size
                surface_y = y * self.tile_size
                surface.blit(self.wall_right, (surface_x, surface_y))
        def draw_door(surface):
            surface_x = (self.house_width-3) * self.tile_size
            surface_y = (self.house_height-1) * self.tile_size
            surface.blit(self.door, (surface_x, surface_y))
        def draw_roof_top(surface):
            for x in range (1, self.house_width-1):
                surface_x = x * self.tile_size
                surface_y = 0 * self.tile_size
                surface.blit(self.roof_top, (surface_x, surface_y))
        def draw_roof_bottom(surface):
            for x in range (1, self.house_width-1):
                surface_x = x * self.tile_size
                surface_y = 1 * self.tile_size
                surface.blit(self.roof_bottom, (surface_x, surface_y))
        def draw_roof_left(surface):
            surface_x = 0 * self.tile_size
            surface_y = 1 * self.tile_size
            surface.blit(self.roof_left, (surface_x, surface_y))
        def draw_roof_right(surface):
            surface_x = (self.house_width-1) * self.tile_size
            surface_y = 1 * self.tile_size
            surface.blit(self.roof_right, (surface_x, surface_y))
        def draw_roof_arch(surface):
            surface_x = (self.house_width-3) * self.tile_size
            surface_y = (self.house_height-3) * self.tile_size
            surface.blit(self.roof_arch, (surface_x, surface_y))
        def draw_roof_left_corner(surface):
            surface_x = 0 * self.tile_size
            surface_y = 0 * self.tile_size
            surface.blit(self.roof_left_corner, (surface_x, surface_y))
        def draw_roof_right_corner(surface):
            surface_x = (self.house_width-1) * self.tile_size
            surface_y = 0 * self.tile_size
            surface.blit(self.roof_right_corner, (surface_x, surface_y))
        
        draw_wall(surface)
        draw_wall_left(surface)
        draw_wall_right(surface)
        draw_door(surface)
        draw_roof_top(surface)
        draw_roof_bottom(surface)
        draw_roof_left(surface)
        draw_roof_right(surface)
        draw_roof_arch(surface)
        draw_roof_left_corner(surface)
        draw_roof_right_corner(surface)

    def draw(self, sprite_surface, screen_surface, map_x, map_y, camera_x, camera_y):
        screen_x = map_x - camera_x
        screen_y = map_y - camera_y
        screen_surface.blit(sprite_surface, (screen_x, screen_y))
        
    
