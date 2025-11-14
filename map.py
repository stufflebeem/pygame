import pygame
from random import *
from villager import *
from guard import *
from items import *

# Creates a class called tiles to create maps and backgrounds
class Tiles():
    def __init__(self):

        # loads three different types of grass for the background
        self.grass_1 = pygame.image.load(background['grass_1']['img']).convert_alpha()
        self.grass_2 = pygame.image.load(background['grass_2']['img']).convert_alpha()
        self.grass_3 = pygame.image.load(background['grass_3']['img']).convert_alpha()

        # creates a list containing a randomly generated series of tiles to be drawn as the background
        self.tile_map = []
        for _ in range(map_height):
            row = []
            for _ in range(map_width):
                if randint(1,100) <=10:
                    row.append(self.grass_3)
                if randint(1,100) <=30:
                    row.append(self.grass_2)
                else:
                    row.append(self.grass_1)
            self.tile_map.append(row)

    def draw(self,surface, camera_x, camera_y):
        """surface: game surface for the background to be blitted onto
           camera_x: camera x position on the visible screen
           camera_y: camera y position on the visible screen """
        for x in range(map_width):
            for y in range(map_height):
                tile = self.tile_map[y][x]
                screen_x = x * tile_size - camera_x
                screen_y = y * tile_size - camera_y
                surface.blit(tile, (screen_x,screen_y))

# Creates a class called house containing background homes
class House(pygame.sprite.Sprite):
    def __init__(self,type):

        """type: brick or stone houses"""
        pygame.sprite.Sprite.__init__(self)
        self.type = type

         # creates a transparent surface for the sprites
        self.house_width = 5
        self.house_height = 4
        self.image = pygame.Surface([self.house_width*16,self.house_height*16]).convert_alpha()
        self.rect = self.image.get_rect()

        # sequentially loads chosen house sprite from a dictionary and blits it to given positions
        for i in self.type:
            for x in range (self.type[i]['pos_x'][0],self.type[i]['pos_x'][1]):
                for y in range(self.type[i]['pos_y'][0],self.type[i]['pos_y'][1]):
                    self.image.blit(pygame.image.load(self.type[i]['img']), (x * tile_size, y * tile_size))

        # creates a random location of the map for the house to be located
        self.map_x = randrange(int(0+WIDTH/2),int(map_width*16-WIDTH/2-self.house_width*16),self.house_width*16)
        self.map_y = randrange(int(0+HEIGHT/2),int(map_height*16-HEIGHT/2-self.house_height*16),self.house_height*16*2)
        self.rect.topleft = (self.map_x, self.map_y)

    def draw(self, screen_surface, camera_x, camera_y):

        """screen_surface: game surface for the background to be blitted onto
           camera_x: camera x position on the visible screen
           camera_y: camera y position on the visible screen"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        screen_surface.blit(self.image, (screen_x, screen_y))

# Creates a class called tree containing trees that border the map
class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # creates transparant surface for the sprites
        self.trees_width = map_width
        self.trees_height = map_height
        self.image = pygame.Surface([self.trees_width*tile_size,self.trees_height*tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()

        # sequentially loads chosen tree sprite from a dictionary and blits it to given positions
        for x in range (self.trees_width):
            for y in range(self.trees_height):
                surface_x = x * tile_size
                surface_y = y * tile_size
                # creates a row of trees along the border of the map with a transparent middle for gameplay
                if x < 12 or x > (self.trees_width-12) or y < 9 or y > (self.trees_height-9):
                    self.image.blit(pygame.image.load(trees['tree_center']['img']),(surface_x, surface_y))
                if x == 12:
                    self.image.blit(pygame.image.load(trees['tree_left']['img']),(surface_x, surface_y))
                if x == self.trees_width-12:
                    self.image.blit(pygame.image.load(trees['tree_right']['img']),(surface_x, surface_y))
                if y == 9:
                    self.image.blit(pygame.image.load(trees['tree_bottom']['img']),(surface_x, surface_y))
                if y == self.trees_height-9:
                    self.image.blit(pygame.image.load(trees['tree_top']['img']),(surface_x, surface_y))

        # starts trees surface in the top left corner
        self.map_x = 0
        self.map_y = 0

    def draw(self, screen_surface, camera_x, camera_y):

        """screen_surface: game surface for the background to be blitted onto
           camera_x: camera x position on the visible screen
           camera_y: camera y position on the visible screen"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        screen_surface.blit(self.image, (screen_x, screen_y))

# Creates a class called castle containing background castle
class Castle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # creates transparant surface for the sprites
        self.castle_width = 12
        self.castle_height = 8
        self.image = pygame.Surface([self.castle_width*tile_size,self.castle_height*tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()
        
        # sequentially loads chosen tree sprite from a dictionary and blits it to given positions
        for i in castle:
            for x in range (castle[i]['pos_x'][0],castle[i]['pos_x'][1]):
                for y in range(castle[i]['pos_y'][0],castle[i]['pos_y'][1]):
                    self.image.blit(pygame.image.load(castle[i]['img']), (x * tile_size, y * tile_size))
        # creates a random location of the map for the house to be located
        self.map_x = randrange(int(0+WIDTH/2),int(map_width*tile_size-WIDTH/2-self.castle_width*tile_size),self.castle_width*tile_size)
        self.map_y = randrange(int(0+HEIGHT/2),int(map_height*tile_size-HEIGHT/2-self.castle_height*tile_size),self.castle_height*tile_size*2)
        self.rect.topleft = (self.map_x,self.map_y)

    def draw(self, screen_surface, camera_x, camera_y):
        
        """screen_surface: game surface for the background to be blitted onto
           camera_x: camera x position on the visible screen
           camera_y: camera y position on the visible screen"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        screen_surface.blit(self.image, (screen_x, screen_y))

# Function to create randomly generated homes and castle with villagers and guards
def create_buildings(building_group, villager_group, guard_group, speed):

    # creates a castle and guards
    castle = Castle()
    building_group.add(castle)
    num = 5
    for n in range(1,num+1):
        new_guard = Guard(speed, building_group,villager_group, castle.map_x, castle.map_y+(castle.castle_height+1)*tile_size)
        new_guard.map_x += tile_size * n
        guard_group.add(new_guard)

    # creates houses and villagers
    while len(building_group) < num_houses:
        new_house = House(brick_house)
        if not pygame.sprite.spritecollide(new_house, building_group, False) and not pygame.sprite.spritecollide(new_house, guard_group, False):
            building_group.add(new_house)
        num = randint(2,3)
        for n in range(1,num):
            new_villager = Villager(speed, building_group, new_house.map_x, new_house.map_y+(new_house.house_height+1)*tile_size)
            if n == 2:
                new_villager.map_x += tile_size
            villager_group.add(new_villager)

# Function to create randomly place items around the map that can be picked up
def create_items(item_group, building_group, villager_group, guard_group, player_group):
    num = 10
    for _ in range(num):
        new_item =Items(item_group, building_group, villager_group, guard_group, player_group)
        item_group.add(new_item)