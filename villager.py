import pygame
from game_data import *
from map import *
from player import *
from random import *

# creates a class of sprite Player for the user to control
class Villager(pygame.sprite.Sprite):
    def __init__(self, items, speed, building_group, map_x, map_y):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = map_x
        self.map_y = map_y
        self.speed = speed
        self.items = items
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
            r = randint(1,2)
            if r == 1:
                dress = randint(1,4)
                villager_dress = (f"dress_{dress}")
                villager_dress_top = (f"dress_top_{dress}")
                villager_shirt = 'none'
                villager_pants = 'none'
            else:
                villager_dress = 'none'
                villager_dress_top = 'none'
                pants = randint(1,8)
                villager_pants = (f"pants_{pants}")
                shirt = randint(1,143)
                if shirt in female_shirt:
                    villager_shirt = 'none'
                else:
                    villager_shirt = (f"shirt_{shirt}")
                
        else:
            villager_dress = 'none'
            villager_dress_top = 'none'
            pants = randint(1,8)
            villager_pants = (f"pants_{pants}")
            shirt = randint(1,143)
            if shirt in female_shirt:
                villager_shirt = 'none'
            else:
                villager_shirt = (f"shirt_{shirt}")

        # blits the player sprite onto transparant surface
        blit_list = [villager_model, villager_hair, villager_dress, villager_dress_top, villager_pants, villager_shirt]
        for b in blit_list:
           sprite = self.items.load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

        # adjusts spawn location in case of spawning in building
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x += 100
            self.map_y += 100
            self.rect.topleft = (self.map_x, self.map_y)
    def update(self, player_group):
        self.player_group = player_group
        self.rect.topleft = (self.map_x, self.map_y)
        player = self.player_group.sprites()[0]

        if pygame.sprite.spritecollide(self, self.player_group, False):
            push = 16
            self.map_x += player.last_dx*push
            self.map_y += player.last_dy*push
               # checks ability to move in the x direction based on collision
            
        
    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))
        
    # takes keystroke inputs and changes the position of the sprite on the map relative to the speed

    """self.map_x += player.last_dx * push
            self.rect.topleft = (self.map_x, self.map_y)
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_x -= player.last_dx * push
                self.rect.topleft = (self.map_x, self.map_y)

            # checks ability to move in the y direction based on collision
            self.map_y += player.last_dy * push
            self.rect.topleft = (self.map_x, self.map_y)
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_y -= player.last_dy * push
                self.rect.topleft = (self.map_x, self.map_y)
            self.rect.topleft = (self.map_x, self.map_y)"""
        