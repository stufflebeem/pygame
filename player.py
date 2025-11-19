import pygame
from random import *
from game_data import *
from items import *

# creates a class of sprite Player for the user to control
class Player(pygame.sprite.Sprite):
    def __init__(self, building_group):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = (map_width*tile_size)/2
        self.map_y = (map_height*tile_size)/2
        self.building_group = building_group
        self.last_dx = 0
        self.last_dy = 0

        # creates player stats
        self.speed = 2
        self.defense = 0
        self.attack = 0
        self.range = 0
        self.health = 100

        # creates a transparent surface for the sprite
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))
        self.items = player_items

        # adjusts spawn location in case of spawning in building
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x += 100
            self.map_y += 100
            self.rect.topleft = (self.map_x, self.map_y)
        
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

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn"""
        # blits the player sprite onto transparant surface
        self.image.fill((0,0,0,0))
        for k, v in self.items.items():
           sprite = load_items(v)
           self.image.blit(sprite["sprite"],(0,0))
        surface.blit(self.image, (WIDTH/2, HEIGHT/2))