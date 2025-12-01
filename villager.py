import pygame
from game_data import *
from map import *
from player import *
from random import *
from items import *

# creates a class of sprite Villager
class Villager(pygame.sprite.Sprite):
    def __init__(self, building_group, villager_group, guard_group, orc_group):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        
        # initializes movement
        self.map_x = 0
        self.map_y = 0
        self.dx = 0
        self.dy = 0

        # creates villager stats
        self.speed = 1
        self.defense = 1
        self.health = 3

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

        # villager items
        model = randint(1,6)
        villager_model = (f"model_{model}")
        hair = randint(1,80)

        # function assigns gender based on hair
        villager_hair = (f"hair_{hair}")
        if hair in female_hair:
            dress = randint(1,4)
            villager_dress = (f"dress_{dress}")
            villager_dress_top = (f"dress_top_{dress}")
            villager_shirt = 'none'
            villager_pants = 'none'
            villager_boots = 'none'
        else:
            villager_dress = 'none'
            villager_dress_top = 'none'
            pants = randint(1,8)
            villager_pants = (f"pants_{pants}")
            boots = randint(1,8)
            villager_boots = (f"boots_{boots}")
            shirt = randint(1,120)
            if shirt in female_shirt:
                villager_shirt = 'none'
            else:
                villager_shirt = (f"shirt_{shirt}")

        # blits the player sprite onto transparant surface
        self.items = {'model': villager_model, 'pants' : villager_pants, 'boots' : villager_boots, 'shirt' : villager_shirt,
                'hair' : villager_hair, 'dress' : villager_dress, 'dress_top' : villager_dress_top}
        blit_list = [villager_model, villager_hair, villager_dress, villager_dress_top, villager_pants, villager_boots, villager_shirt]
        for b in blit_list:
            sprite = load_items(b)
            self.image.blit(sprite["sprite"],(0,0))

        # adjusts spawn location in case of spawning in object
        safe = False
        while safe == False:
            self.map_x = randint(int(0 + 12 * tile_size), int(map_width * tile_size - 13 * tile_size))
            self.map_y = randint(int(0 + 9 * tile_size), int(map_height * tile_size - 10 * tile_size))
            self.rect.topleft = (self.map_x, self.map_y)

            collision = [other for other in self.villager_group if other != self and self.rect.colliderect(other.rect)]
            if pygame.sprite.spritecollide(self, self.building_group, False):
                safe = False
            elif collision:
                safe = False
            elif pygame.sprite.spritecollide(self, self.guard_group, False):
                safe = False
            elif pygame.sprite.spritecollide(self, self.orc_group, False):
                safe = False
            else:
                safe = True
            
        # records safe spawning position
        self.last_map_x = self.map_x
        self.last_map_y = self.map_y
        
    # needs to create an automatically updating system for villagers to move and ineract with the world around them
    def update(self, player_group):
        """player_group: player_group"""
        self.player_group = player_group
        try:
            player = self.player_group.sprites()[0]
        except IndexError:
            return None
        
        # checks health
        if self.health <= 0:
            self.villager_group.remove(self)

        # records last collison free position
        self.last_map_x = self.map_x
        self.last_map_y = self.map_y

        # flag if orc detected
        target = False

        # loops over every orc to see if any are in a 7 tile radius
        closest_orc = None
        closest_distance = 5*tile_size
        for orc in self.orc_group: 
            distance = ((orc.map_x - self.map_x)**2 + (orc.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_orc = orc
                target = True
        
        # controls movement if orc has detected a villager
        if target == True:
            self.dx = -1 if closest_orc.map_x > self.map_x else 1
            self.dy = -1 if closest_orc.map_y > self.map_y else 1


        # creates movement at random intervals, every 10 seconds a villager should move at least once if no orc is detected
        else:
            movement = randint(1,600)
            if movement == 1:
                self.dx = 1 if randint(0,1) == 0 else -1
            if movement == 2:
                self.dy = 1 if randint(0,1) == 0 else -1

            # stops villagers after around 2 seconds of movement
            if movement > 580:
                self.dx = 0
                self.dy = 0

        # updates position
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)

        # detects collisions between villager and buildings
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_x += 12*tile_size

        # detects collisions between villager and other villagers
        collision = [other for other in self.villager_group if other != self and self.rect.colliderect(other.rect)]
        
        if collision:
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detects collisions between villager and guards
        if pygame.sprite.spritecollide(self, self.guard_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detect collisions between villager and orcs
        if pygame.sprite.spritecollide(self, self.orc_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detects collisions between villager and player
        if pygame.sprite.spritecollide(self, self.player_group, False):
            self.map_x += player.dx
            self.map_y += player.dy
            self.rect.topleft = (self.map_x, self.map_y)

            # detects collisions between villager and other villagers
            collision = [other for other in self.villager_group if other != self and self.rect.colliderect(other.rect)]
            
            if collision:
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0

            # detects collisions between villager and guards
            if pygame.sprite.spritecollide(self, self.guard_group, False):
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0

            # detect collisions between villager and orcs
            if pygame.sprite.spritecollide(self, self.orc_group, False):
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0    
                
            # detects collisions between villager and buildings
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0

        # defines world borders for villager
        if self.map_x < 0 + 12 * tile_size or self.map_x > map_width * tile_size - 13 * tile_size:
            self.map_x = self.last_map_x
            self.dx = 0
        if  self.map_y > map_height * tile_size - 10 * tile_size or self.map_y < 0 + 9 * tile_size:
             self.map_y = self.last_map_y
             self.dy = 0

    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))
        