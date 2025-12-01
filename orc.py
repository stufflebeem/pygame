import pygame
from game_data import *
from map import *
from player import *
from items import *

# creates a class of sprite orc as an enemy of the player and orcs
class Orc(pygame.sprite.Sprite):
    def __init__(self, building_group, villager_group, guard_group, orc_group):
        """items: list of items dictionary
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = 0
        self.map_y = 0
        self.dx = 1
        self.dy = 1

        # creates orc stats
        self.speed = 1
        self.defense = 1
        self.attack = 0
        self.range = 1
        self.health = 2
        self.reload = 0
        self.reload_time = 0

        # initializes groups
        self.villager_group = villager_group
        self.guard_group = guard_group
        self.orc_group = orc_group
        self.building_group = building_group

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

       # adjusts spawn location in case of spawning in object
        safe = False
        while safe == False:
            self.map_x = randint(int(0 + 12 * tile_size), int(map_width * tile_size - 13 * tile_size))
            self.map_y = randint(int(0 + 9 * tile_size), int(map_height * tile_size - 10 * tile_size))
            self.rect.topleft = (self.map_x, self.map_y)

            collision = [other for other in self.orc_group if other != self and self.rect.colliderect(other.rect)]
            if pygame.sprite.spritecollide(self, self.building_group, False):
                safe = False
            elif collision:
                safe = False
            elif pygame.sprite.spritecollide(self, self.guard_group, False):
                safe = False
            elif pygame.sprite.spritecollide(self, self.villager_group, False):
                safe = False
            else:
                safe = True
        
        # records safe spawning position
        self.last_map_x = self.map_x
        self.last_map_y = self.map_y
        
    # needs to create an automatically updating system for orcs to move and ineract with the world around them
    def update(self, player_group):
        """player_group: player_group"""
        self.player_group = player_group
        player = self.player_group.sprites()[0]

        # checks health
        if self.health <= 0:
            self.orc_group.remove(self)

        # records last collison free position
        self.last_map_x = self.map_x
        self.last_map_y = self.map_y
    
        # flag to determine if the orc has detected a target villager
        target = False

        # loops over every villager to see if any are in a 7 tile radius
        closest_enemy = None
        closest_distance = 7*tile_size
        for villager in self.villager_group: 
            distance = ((villager.map_x - self.map_x)**2 + (villager.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = villager
                target = True
        for guard in self.guard_group: 
            distance = ((guard.map_x - self.map_x)**2 + (guard.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = guard
                target = True
        distance = ((player.map_x - self.map_x)**2 + (player.map_y - self.map_y)**2)**0.5
        if distance < closest_distance:
                closest_distance = distance
                closest_enemy = player
                target = True
        
        # controls movement if orc has detected a villager
        if target == True:
            self.dx = 1 if closest_enemy.map_x > self.map_x else -1
            self.dy = 1 if closest_enemy.map_y > self.map_y else -1

        # creates movement at random intervals, every 10 seconds a orc should move at least once if no villager is detected
        else:
            movement = randint(1,600)
            if movement == 1:
                self.dx = 1 if randint(0,1) == 0 else -1
            if movement == 2:
                self.dy = 1 if randint(0,1) == 0 else -1

        # updates position
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)

        # detects collisions between orc and buildings
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_x += 12*tile_size

        # detects collisions between orc and other orcs
        collision = [other for other in self.orc_group if other != self and self.rect.colliderect(other.rect)]
        
        if collision:
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detects collisions between orc and guards
        if pygame.sprite.spritecollide(self, self.guard_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detect collisions between orc and villagers
        if pygame.sprite.spritecollide(self, self.villager_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detects collisions between orc and player
        if pygame.sprite.spritecollide(self, self.player_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0
        
        # defines world borders for orc
        if self.map_x < 0 + 12 * tile_size or self.map_x > map_width * tile_size - 13 * tile_size:
            self.map_x = self.last_map_x
            self.dx = 0
        if  self.map_y > map_height * tile_size - 10 * tile_size or self.map_y < 0 + 9 * tile_size:
             self.map_y = self.last_map_y
             self.dy = 0

        # attack villagers, guards, and player
        target = False
        closest_enemy = None
        closest_distance = self.range * tile_size
        for villager in self.villager_group: 
            distance = ((villager.map_x - self.map_x)**2 + (villager.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = villager
                target = True
        for guard in self.guard_group: 
            distance = ((guard.map_x - self.map_x)**2 + (guard.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = guard
                target = True
        distance = ((player.map_x - self.map_x)**2 + (player.map_y - self.map_y)**2)**0.5
        if distance < closest_distance:
                closest_distance = distance
                closest_enemy = player
                target = True
        
        if target == True and self.reload_time < pygame.time.get_ticks():
            closest_enemy.health -= self.attack * (1/closest_enemy.defense)
            closest_enemy.dx = -self.dx
            closest_enemy.dy = -self.dy
            self.reload_time = pygame.time.get_ticks() + self.reload * 60

    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))

def create_orcs(building_group, villager_group, guard_group, orc_group):
    num = 5 + level
    for _ in range(num):
        new_orc = Orc(building_group, villager_group, guard_group, orc_group)
        orc_group.add(new_orc)
    for orc in orc_group:
        for key, item in orc.items.items():
            if item == "none":
                    continue
            orc.defense += load_items(item)["stats"]["defense"]
            orc.speed += load_items(item)["stats"]["speed"]
            orc.attack += load_items(item)["stats"]["attack"]
            orc.reload += load_items(item)["stats"]["reload"]
            orc.range += load_items(item)["stats"]["range"]