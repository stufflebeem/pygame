import pygame
from game_data import *
from map import *
from villager import *

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
    def __init__(self, items, speed, building_group, villager_group):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = (map_width*tile_size)/2
        self.map_y = (map_height*tile_size)/2
        self.speed = speed
        self.items = items
        self.building_group = building_group
        self.villager_group = villager_group
        self.last_dx = 0
        self.last_dy = 0

        # creates a transparent surface for the sprite
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))

        # blits the player sprite onto transparant surface
        blit_list = [model, pants, boots, shirt, hair, helmet, 
                     shield, weapon]
        for b in blit_list:
           sprite = self.items.load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

        # adjusts spawn location in case of spawning in building
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x += 100
            self.map_y += 100
            self.rect.topleft = (self.map_x, self.map_y)

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn"""
        surface.blit(self.image, (WIDTH/2, HEIGHT/2))
        
    # takes keystroke inputs and changes the position of the sprite on the map relative to the speed
    def keys(self):

        # detects and saves a key input
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0
        
        # acts based on key input to move the sprite around the screen with WASD and arrows
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.map_x > 0 + WIDTH/4+10:
            if (keys[pygame.K_LSHIFT]):
                self.dx -= self.speed+1
            else:
                self.dx -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.map_x < map_width * tile_size - WIDTH/4-10:
            if (keys[pygame.K_LSHIFT]):
                self.dx += self.speed+1
            else:
                self.dx += self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.map_y < map_height * tile_size - HEIGHT/4-10:
            if (keys[pygame.K_LSHIFT]):
                self.dy += self.speed+1
            else:
                self.dy += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.map_y > 0 + HEIGHT/4+10:
            if (keys[pygame.K_LSHIFT]):
               self.dy -= self.speed+1
            else:
                self.dy -= self.speed
    def update(self):
        # checks ability to move in the x and y direction based on collision
        self.score = int(pygame.time.get_ticks()/10800)
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x -= self.dx
            self.last_dx = self.dx
            self.map_y -= self.dy
            self.last_dy = self.dy
            self.rect.topleft = (self.map_x, self.map_y)


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
    

    
