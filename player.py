import pygame
from random import *
from game_data import *
from items import *

# creates a class of sprite Player for the user to control
class Player(pygame.sprite.Sprite):
    def __init__(self, building_group, villager_group, guard_group, orc_group):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = (map_width*tile_size)/2
        self.map_y = (map_height*tile_size)/2

        # defines groups
        self.building_group = building_group
        self.villager_group = villager_group
        self.guard_group = guard_group
        self.orc_group = orc_group

        # creates player stats
        self.speed = 2
        self.defense = 1
        self.attack = 0
        self.range = 1
        self.reload = 0
        self.reload_time = 0
        self.health = 5

        # creates a transparent surface for the sprite
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))
        self.items = player_items

        # adjusts spawn location in case of spawning in object
        while True:
            collision = pygame.sprite.spritecollide(self, self.building_group, False)
            collision += pygame.sprite.spritecollide(self, self.villager_group, False)
            collision += pygame.sprite.spritecollide(self, self.guard_group, False)
            collision += pygame.sprite.spritecollide(self, self.orc_group, False)
            if not collision:
                break
            self.map_x += randint(-10,10)
            self.map_y += randint(-10,10)
            self.rect.topleft = (self.map_x, self.map_y)
        
    # takes keystroke inputs and changes the position of the sprite on the map relative to the speed
    def keys(self):

        # detects and saves a key input
        keys = pygame.key.get_pressed()
        self.dx = 0
        self.dy = 0
        
        # acts based on key input to move the sprite around the screen with WASD and arrows
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.map_x > 0 + 12 * tile_size:
            if (keys[pygame.K_LSHIFT]):
                self.dx -= self.speed+1
            else:
                self.dx -= self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.map_x < map_width * tile_size - 13 * tile_size:
            if (keys[pygame.K_LSHIFT]):
                self.dx += self.speed+1
            else:
                self.dx += self.speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.map_y < map_height * tile_size - 10 * tile_size:
            if (keys[pygame.K_LSHIFT]):
                self.dy += self.speed+1
            else:
                self.dy += self.speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.map_y > 0 + 9 * tile_size:
            if (keys[pygame.K_LSHIFT]):
               self.dy -= self.speed+1
            else:
                self.dy -= self.speed

    def update(self):

        self.score = int(pygame.time.get_ticks()/10800)
        
        # updates player position
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)

        # detects collisions between player and buildings
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x -= self.dx
            self.map_y -= self.dy

        # detects collisions between player and guards
        if pygame.sprite.spritecollide(self, self.guard_group, False):
            self.map_x -= self.dx
            self.map_y -= self.dy

        # detect collisions between player and villagers
        if pygame.sprite.spritecollide(self, self.villager_group, False):
            self.map_x -= self.dx
            self.map_y -= self.dy

        # detects collisions between player and orcs
        if pygame.sprite.spritecollide(self, self.orc_group, False):
            self.map_x -= self.dx
            self.map_y -= self.dy
    def attack(self):
        # loops over every orc to see if any are in the range
        target = False
        closest_orc = None
        closest_distance = self.range * tile_size
        for orc in self.orc_group: 
            distance = ((orc.map_x - self.map_x)**2 + (orc.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_orc = orc
                target = True
        # if orcs are in range subtracts health from the nearest one and starts cooldown
        if target == True and self.reload_time < pygame.time.get_ticks():
            closest_orc.health -= self.attack * (1/closest_orc.defense)
            closest_orc.dx = -self.dx
            closest_orc.dy = -self.dy
            self.reload_time = pygame.time.get_ticks() + self.reload * 60

    def draw(self, surface):
        """surface: the screen on which the sprite is drawn"""
        # blits the player sprite onto transparant surface
        self.image.fill((0,0,0,0))
        for k, v in self.items.items():
           sprite = load_items(v)
           self.image.blit(sprite["sprite"],(0,0))
        surface.blit(self.image, (WIDTH/2, HEIGHT/2))