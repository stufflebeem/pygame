import pygame
from game_data import *
from map import *

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
    def __init__(self, items, world_x, world_y, speed, building_group,):
        """items: list of items dictionary
           world_x: the x coordinate of the sprite on the map
           world_y: the y coordinate of the sprite on the map
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.world_x = world_x
        self.world_y = world_y
        self.speed = speed
        self.items = items
        self.building_group = building_group
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(center=(self.world_x, self.world_y))

        # blits the player sprite onto
        blit_list = [model, pants,boots,shirt, hair, helmet, 
                     shield, weapon]
        for b in blit_list:
           sprite = self.items.load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn
           screen_x: the x coordinate of the sprite on the screen
           screen_y: the y coordinate of the sprite on the screen"""
        surface.blit(self.image, (WIDTH/2, HEIGHT/2))
        
    
    def keys(self):
        """takes keystroke inputs and changes the position of the sprite on the map relative to
        the speed"""
        keys = pygame.key.get_pressed()
        self.zoom_level = zoom_level
        
        self.map_width = map_width * tile_size
        self.map_height = map_height * tile_size

        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.world_x > 0 + WIDTH/(2*zoom_level)+10:
            self.world_x -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.world_x < self.map_width - WIDTH/(2*zoom_level)-10:
            self.world_x += self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.world_y < self.map_height - HEIGHT/(2*zoom_level)-10:
            self.world_y += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.world_y > 0 + HEIGHT/(2*zoom_level)+10:
            self.world_y -= self.speed

            # changes the speed of the sprite based on LSHIFT and LCRTL inputs
        if keys[pygame.K_LSHIFT]:
            self.speed += 0.1
        if keys[pygame.K_LCTRL]:
            self.speed -= 0.1
        self.speed = abs(self.speed)
        

# creates a class of Items for the Player and others to wear and use
class Items():
    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
    def load_items(self, name):
        data = item_data[name]
        x,y = data["pos"]
        sprite = get_sprite(self.sprite_sheet, x, y, 16, 16)
        return {"name":name, "sprite":sprite,"category":data["category"], "stats":data["stats"]}
    

    
