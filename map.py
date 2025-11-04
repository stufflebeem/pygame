import pygame
from game_data import *
from random import randint
from player import *

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

# Creates a class called house
class House():
    def __init__(self,surface,type):
        self.type = type
        self.tile_size = 16
        self.house_width = 5
        self.house_height = 4

        for i in self.type:
            for x in range (self.type[i]['pos_x'][0],self.type[i]['pos_x'][1]):
                for y in range(self.type[i]['pos_y'][0],self.type[i]['pos_y'][1]):
                    surface_x = x * self.tile_size
                    surface_y = y * self.tile_size
                    surface.blit(pygame.image.load(self.type[i]['img']), (surface_x, surface_y))
        self.map_x = randint(0,map_width)*self.house_width
        self.map_y = randint(0,map_height)*self.house_width

    def draw(self, sprite_surface, screen_surface, camera_x, camera_y):
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        screen_surface.blit(sprite_surface, (screen_x, screen_y))
        