import pygame
from game_data import *
from random import *
from player import *

# Creates a class called tiles to create maps and backgrounds
class Tiles():
    def __init__(self):
        """initializes the tile, creates variables for the map"""

        self.grass_1 = pygame.image.load(background['grass_1']['img']).convert_alpha()
        self.grass_2 = pygame.image.load(background['grass_2']['img']).convert_alpha()
        self.grass_3 = pygame.image.load(background['grass_3']['img']).convert_alpha()

        self.tile_map = []
        for y in range(map_height):
            row = []
            for x in range(map_width):
                if randint(1,100) <=10:
                    row.append(self.grass_3)
                if randint(1,100) <=30:
                    row.append(self.grass_2)
                else:
                    row.append(self.grass_1)
            self.tile_map.append(row)

    def draw(self,surface, camera_x, camera_y):
        """draws the tiles on a surface the size of the map and shows the area visible on the screen"""
        for x in range(map_width):
            for y in range(map_height):
                tile = self.tile_map[y][x]
                screen_x = x * tile_size - camera_x
                screen_y = y * tile_size - camera_y
                surface.blit(tile, (screen_x,screen_y))

# Creates a class called house
class House(pygame.sprite.Sprite):
    def __init__(self,type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.house_width = 5
        self.house_height = 4
        self.image = pygame.Surface([self.house_width*16,self.house_height*16]).convert_alpha()
        self.rect = self.image.get_rect()

        for i in self.type:
            for x in range (self.type[i]['pos_x'][0],self.type[i]['pos_x'][1]):
                for y in range(self.type[i]['pos_y'][0],self.type[i]['pos_y'][1]):
                    surface_x = x * tile_size
                    surface_y = y * tile_size
                    self.image.blit(pygame.image.load(self.type[i]['img']), (surface_x, surface_y))
        self.map_x = randrange(int(0+WIDTH/2),int(map_width*16-WIDTH/2-self.house_width*16),self.house_width*16)
        self.map_y = randrange(int(0+HEIGHT/2),int(map_height*16-HEIGHT/2-self.house_height*16),self.house_height*16*2)
        if [self.map_x,self.map_x] in locations:
            'none'
        else:
            locations.append([self.map_x,self.map_x])

    def draw(self, screen_surface, camera_x, camera_y):
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        if [screen_x, screen_y] not in locations:
            screen_surface.blit(self.image, (screen_x, screen_y))

class Tree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.trees_width = map_width
        self.trees_height = map_height
        self.image = pygame.Surface([self.trees_width*tile_size,self.trees_height*tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()

        for x in range (self.trees_width):
            for y in range(self.trees_height):
                surface_x = x * tile_size
                surface_y = y * tile_size
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
        self.map_x = 0
        self.map_y = 0

    def draw(self, screen_surface, camera_x, camera_y):
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        if [screen_x, screen_y] not in locations:
            screen_surface.blit(self.image, (screen_x, screen_y))

class Castle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.castle_width = 12
        self.castle_height = 9
        self.image = pygame.Surface([self.castle_width*tile_size,self.castle_height*tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()

        for i in castle:
            for x in range (castle[i]['pos_x'][0],castle[i]['pos_x'][1]):
                for y in range(castle[i]['pos_y'][0],castle[i]['pos_y'][1]):
                    surface_x = x * tile_size
                    surface_y = y * tile_size
                    self.image.blit(pygame.image.load(castle[i]['img']), (surface_x, surface_y))
        self.map_x = randrange(int(0+WIDTH/2),int(map_width*tile_size-WIDTH/2-self.castle_width*tile_size),self.castle_width*tile_size)
        self.map_y = randrange(int(0+HEIGHT/2),int(map_height*tile_size-HEIGHT/2-self.castle_height*tile_size),self.castle_height*tile_size*2)
        if [self.map_x,self.map_x] in locations:
            'none'
        else:
            locations.append([self.map_x,self.map_x])

    def draw(self, screen_surface, camera_x, camera_y):
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        screen_surface.blit(self.image, (screen_x, screen_y))
        