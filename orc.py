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
        self.defense = 0
        self.dx = 1
        self.dy = 1

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
        self.items = {'model': orc_model, 'pants' : orc_pants, 'boots' : orc_boots, 'shirt' : orc_shirt,
                'hair' : "none", 'helmet' : orc_helmet, 'shield' : "none", 'weapon' : orc_weapon}
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
        player = self.player_group.sprites()[0]
        self.rect.topleft = (self.map_x, self.map_y)

        # flag to determine if the orc has detected a target villager
        target = False

        # loops over every villager to see if any are in a 15 tile radius
        closest_villager = None
        closest_distance = 15*tile_size
        for villager in self.villager_group: 
            distance = ((villager.map_x - self.map_x)**2 + (villager.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_villager = villager
                target = True 
        
        # controls movement if orc has detected a villager
        if target == True:
            self.dx = 1 if closest_villager.map_x > self.map_x else -1
            self.dy = 1 if closest_villager.map_y > self.map_y else -1

        # creates movement at random intervals, every 10 seconds a orc should move at least once if no villager is detected
        else:
            movement = randint(1,600)
            if movement == 1:
                self.dx = 1 if randint(0,1) == 0 else 1
            if movement == 2:
                self.dy = 1 if randint(0,1) == 0 else 1

        # detects collisions between orc and buildings
        last_x = self.map_x
        self.map_x += self.dx
        self.rect.topleft = (self.map_x, self.map_y)

        if pygame.sprite.spritecollide(self, self.building_group, False) :
            self.map_x = last_x
            self.dx = 0
            self.rect.topleft = (self.map_x, self.map_y)
        
        last_y = self.map_y
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)
        if pygame.sprite.spritecollide(self, self.building_group, False) :
            self.map_y = last_y
            self.dy = 0
            self.rect.topleft = (self.map_x, self.map_y)
            
        # detects collisions between orcs and guards
        if  pygame.sprite.spritecollide(self, self.guard_group, False):
            self.dx = -self.dx
            self.dy = -self.dy
            self.map_x += self.dx
            self.map_y += self.dy
            self.rect.topleft = (self.map_x, self.map_y)  

        # detects collisions between orcs and player
        if pygame.sprite.spritecollide(self, self.player_group, False):
            if player.dx and player.dy == 0:
                player.map_x += 10
                player.map_y += 10
            else:
                player.dx = -player.dx
                player.dy = -player.dy
        
         # defines world borders for villagers
        if self.map_x < 0 + WIDTH/4+10 or self.map_x > map_width * tile_size - WIDTH/4-10:
            self.dx = -self.dx
        if  self.map_y > map_height * tile_size - HEIGHT/4-10 or self.map_y < 0 + HEIGHT/4+10:
             self.dy = -self.dy

    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))

def create_orcs(building_group, villager_group, guard_group, orc_group):
    num = 10
    map_x = randint(int(0+ WIDTH/4 + 10) ,int(map_width*tile_size - WIDTH/4 - 10))
    map_y = randint(int(0+ HEIGHT/4 + 10) ,int(map_height*tile_size - HEIGHT/4 -10))
    print(f"{map_x},{map_y}")
    for _ in range(num):
        map_x += tile_size * 2
        new_orc = Orc(orc_group, building_group, villager_group, guard_group, orc_group, map_x, map_y)
        orc_group.add(new_orc)
    for orc in orc_group:
        for key, item in orc.items.items():
            if item == "none":
                    continue
            orc.defense += load_items(item)["stats"]["defense"]