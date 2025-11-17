import pygame
from game_data import *
from map import *
from player import *
from items import *

# creates a class of sprite orc as an enemy of the player and orcs
class Orc(pygame.sprite.Sprite):
    def __init__(self, speed, building_group, villager_group, guard_group, orc_group, map_x, map_y):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = map_x
        self.map_y = map_y
        self.speed = speed
        self.building_group = building_group
        self.villager_group = villager_group
        self.guard_group = guard_group
        self.orc_group = orc_group
        self.dx = 0
        self.dy = 0

        # creates a transparent surface for the sprite
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))

        # orc items
        type_orc = randint(1,10)
        if type_orc == 10:
            model = randint(1,2)
            orc_model = (f"orc_{model}")
            orc_shirt = ("shirt_90")
            orc_pants = ("pants_1")
            orc_boots = ("boots_1")
            orc_helmet = ("helmet_16")
            weapon = randint(0, len(guard_weapons)-1)
            orc_weapon = (f"weapon_{guard_weapons[weapon]}")
        elif type_orc >= 3:
            model = randint(1,2)
            orc_model = (f"orc_{model}")
            shirt_1 = randint(8,11)
            shirt_2 = randint(6,10)
            if shirt_2 == 10:
                shirt_2 = 0
            orc_shirt = (f"shirt_{shirt_1}{shirt_2}")
            if orc_shirt == "shirt_88":
                orc_shirt = ("none")
            orc_pants = ("pants_1")
            orc_boots = ("boots_1")
            orc_helmet = ("none")
            weapon = randint(0, len(guard_weapons)-1)
            orc_weapon = (f"weapon_{guard_weapons[weapon]}")
        else:
            model = randint(1,2)
            orc_model = (f"orc_{model}")
            orc_shirt = ("none")
            orc_pants = ("pants_1")
            orc_boots = ("boots_1")
            orc_helmet = ("none")
            weapon = randint(0, len(guard_weapons)-1)
            orc_weapon = (f"weapon_{guard_weapons[weapon]}")
            

        # blits the player sprite onto transparant surface
        blit_list = [orc_model,  orc_shirt, orc_pants, orc_boots, orc_helmet, orc_weapon]
        for b in blit_list:
           sprite = load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

        # adjusts spawn location in case of spawning in building
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x += 100
            self.map_y += 100
            self.rect.topleft = (self.map_x, self.map_y)
        
    # needs to create an automatically updating system for orcs to move and ineract with the world around them
    def update(self, player_group):
        """player_group: player_group"""
        self.player_group = player_group
        self.rect.topleft = (self.map_x, self.map_y)
        player = self.player_group.sprites()[0]

        # creates movement at random intervals, every 10 seconds a orc should move at least once
        movement = randint(1,600)
        if movement == 1:
            if self.dx == 0:
                r = randint(0,1)
                if r == 0:
                    self.dx = 1
                else:
                    self.dx = -1
            else:
                self.dx = 0
        if movement == 2:
            if self.dy == 0:
                r = randint(0,1)
                if r == 0:
                    self.dy = 1
                else:
                    self.dy = -1
            else:
                self.dy = 0
        
        # stops orcs after around 2 seconds of movement
        if movement > 580:
            self.dx = 0
            self.dy = 0
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)

         # detects collisions between orc and buildings
        if pygame.sprite.spritecollide(self, self.building_group, False) :
            self.dx = -self.dx
            self.dy = -self.dy
            self.map_x += self.dx
            self.map_y += self.dy
            self.rect.topleft = (self.map_x, self.map_y)
            if self.dx == 0 and self.dy == 0:
                self.map_x += -20
                self.map_y += 20
        # detects collisions between orc and other orcs
        for other in self.orc_group:
            if other != self and self.rect.colliderect(other.rect):
                self.dx = -self.dx
                self.dy = -self.dy
                self.map_x += self.dx
                self.map_y += self.dy
                self.rect.topleft = (self.map_x, self.map_y)
                if self.dx == 0 and self.dy == 0:
                    self.map_x += 16
                    self.map_y += 16
        # detects collisions between orc and villagers
        if  pygame.sprite.spritecollide(self, self.villager_group, False):
            self.dx = -self.dx
            self.dy = -self.dy
            self.map_x += self.dx
            self.map_y += self.dy
            self.rect.topleft = (self.map_x, self.map_y)
            if self.dx == 0 and self.dy == 0:
                self.map_x += 16
                self.map_y += 16   
        # detects collisions between orcs and guards
        if  pygame.sprite.spritecollide(self, self.guard_group, False):
            self.dx = -self.dx
            self.dy = -self.dy
            self.map_x += self.dx
            self.map_y += self.dy
            self.rect.topleft = (self.map_x, self.map_y)
            if self.dx == 0 and self.dy == 0:
                self.map_x += 16
                self.map_y += 16   

        # detects collisions between villager and player
        if pygame.sprite.spritecollide(self, self.player_group, False):
                    self.dx = player.dx
                    self.dy = player.dy

    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))

def create_orcs(building_group, villager_group, guard_group, orc_group):
    num = 20
    map_x = randint(0,map_width*tile_size)
    map_y = randint(0,map_height*tile_size)
    print(f"{map_x},{map_y}")
    for _ in range(num):
        map_x += 16
        new_orc = Orc(orc_group, building_group, villager_group, guard_group, orc_group, map_x, map_y)
        orc_group.add(new_orc)