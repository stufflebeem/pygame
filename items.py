import pygame
from random import *
from game_data import *


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

# loads items from the dictionary based on name
def load_items(name):
        """name: dictionary key name for what item is to be loaded"""
        sprite_sheet = pygame.image.load('characters/sprites/roguelikeChar_transparent.png').convert_alpha()
        data = item_data[name]
        x,y = data["pos"]
        sprite = get_sprite(sprite_sheet, x, y, 16, 16)
        return {"name":name, "sprite":sprite,"category":data["category"], "stats":data["stats"]}

# creates a class of Items for the Player and others to wear and use
class Items(pygame.sprite.Sprite):
    def __init__(self, item_group, building_group, player_group, item='none', type ='none'):
        super().__init__()
        """sprite_sheet: the png sheet with extractable sprites"""
        self.item_group = item_group
        self.building_group = building_group
        self.player_group = player_group
        self.player = self.player_group.sprites()[0]
        self.birth_time = pygame.time.get_ticks()

        if item == 'none':
            self.map_x = randint(int(0 + 12 * tile_size), int(map_width * tile_size - 13 * tile_size))
            self.map_y = randint(int(0 + 9 * tile_size), int(map_height * tile_size - 10 * tile_size))
            num = randint(0,2)
            if num == 0:
                self.type = item_list[5]
            else:
                self.type = item_list[randint (0,4)]
            if self.type == 'helmet':
                self.num = randint(1,36)
            elif self.type == 'pants':
                self.num = randint(1,8)
            elif self.type == 'boots':
                self.num = randint(1,8)
            elif self.type == 'shirt':
                self.num = randint(1,120)
                if self.num in female_shirt:
                    self.num = 1
            elif self.type == 'shield':
                self.num = randint(1,71)
            elif self.type == 'weapon':
                self.num = randint(1,110)
            sprite = load_items(f"{self.type}_{self.num}")
        else:
            self.item = item
            self.type = type
            sprite = load_items(self.item)
            player = self.player_group.sprites()[0]
            self.map_x = player.map_x + tile_size
            self.map_y = player.map_y + tile_size
        
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))
        self.image.blit(sprite["sprite"],(0,0))
        
        # detects collisions between sprites and buildings
        while pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x += 10
            self.map_y += 10
            self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))

    def update(self):
        player = self.player_group.sprites()[0]
        keys = pygame.key.get_pressed()
        if (pygame.time.get_ticks())/(self.birth_time+14400) > 1:
            new_item =Items(self.item_group, self.building_group, self.player_group)
            self.item_group.add(new_item)
            self.image.blit(load_items("none")["sprite"],(0,0))
            self.item_group.remove(self)
        if pygame.sprite.spritecollide(self, self.player_group, False) and keys[pygame.K_TAB]:
            item = player_items[self.type]
            new_item =Items(self.item_group, self.building_group, self.player_group, item, self.type)
            self.item_group.add(new_item)
            try:
                player_items[self.type] = f"{self.type}_{self.num}"
            except AttributeError:
                player_items[self.type] = self.item
            self.item_group.remove(self)
            player.speed = 2
            player.defense = 0
            player.attack = 0
            player.range = 1
            player.reload = 0
            player.reload_time = 0
            player.health = 5
            for key, item in player_items.items():
                if item == "none":
                    continue
                player.defense += load_items(item)["stats"]["defense"]
                player.speed += load_items(item)["stats"]["speed"]
                player.attack += load_items(item)["stats"]["attack"]
                player.reload += load_items(item)["stats"]["reload"]
                player.range += load_items(item)["stats"]["range"]

    def draw(self, surface, camera_x, camera_y):
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))

# Function to create randomly place items around the map that can be picked up
def create_items(item_group, building_group, player_group):
    num = 20
    for _ in range(num):
        new_item =Items(item_group, building_group, player_group)
        item_group.add(new_item)