import pygame
from game_data import *
from map import *
from player import *
from items import *

# creates a class of sprite Player for the user to control
class Guard(pygame.sprite.Sprite):
    def __init__(self, speed, building_group, villager_group, map_x, map_y):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        self.map_x = map_x
        self.map_y = map_y
        self.speed = speed
        self.building_group = building_group
        self.villager_group = villager_group
        self.dx = 0
        self.dy = 0

        # creates a transparent surface for the sprite
        self.image = pygame.Surface([tile_size,tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect(topleft=(self.map_x, self.map_y))

        # guard items
        model = randint(1,6)
        guard_model = (f"model_{model}")
        guard_shirt = ("shirt_75")
        guard_pants = ("pants_3")
        guard_boots = ("boots_3")
        guard_helmet = ("helmet_1")
        weapon = randint(0, len(guard_weapons)-1)
        guard_weapon = (f"weapon_{guard_weapons[weapon]}")

        # blits the player sprite onto transparant surface
        blit_list = [guard_model,  guard_shirt, guard_pants, guard_boots, guard_helmet, guard_weapon]
        for b in blit_list:
           sprite = load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

        # adjusts spawn location in case of spawning in building
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x += 100
            self.map_y += 100
            self.rect.topleft = (self.map_x, self.map_y)
            if self.dx == 0 and self.dy == 0:
                self.map_x += -10
                self.map_y += 10
        
    # needs to create an automatically updating system for guards to move and ineract with the world around them
    def update(self, player_group, guard_group):
        """player_group: player_group"""
        self.player_group = player_group
        self.guard_group = guard_group
        self.rect.topleft = (self.map_x, self.map_y)
        player = self.player_group.sprites()[0]

        # creates movement at random intervals, every 10 seconds a guard should move at least once
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
        
        # stops guards after around 2 seconds of movement
        if movement > 580:
            self.dx = 0
            self.dy = 0
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)

         # detects collisions between guard and buildings
        if pygame.sprite.spritecollide(self, self.building_group, False) :
            self.dx = -self.dx
            self.dy = -self.dy
            self.map_x += self.dx
            self.map_y += self.dy
            self.rect.topleft = (self.map_x, self.map_y)
            if self.dx == 0 and self.dy == 0:
                self.map_x += -20
                self.map_y += 20
        # detects collisions between guard and other guards
        for other in self.guard_group:
            if other != self and self.rect.colliderect(other.rect):
                self.dx = -self.dx
                self.dy = -self.dy
                self.map_x += self.dx
                self.map_y += self.dy
                self.rect.topleft = (self.map_x, self.map_y)
                if self.dx == 0 and self.dy == 0:
                    self.map_x += 16
                    self.map_y += 16
                # detects collisions between guard and villagers
        if  pygame.sprite.spritecollide(self, self.villager_group, False):
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
                    self.map_x += self.dx
                    self.map_y += self.dy
                    self.rect.topleft = (self.map_x, self.map_y)
    
        # defines world borders for guards
        if self.map_x < 0 + WIDTH/4+10:
            self.dx = -self.dx
        if self.map_x > map_width * tile_size - WIDTH/4-10:
            self.dx = -self.dx
        if  self.map_y > map_height * tile_size - HEIGHT/4-10:
             self.dy = -self.dy
        if self.map_y < 0 + HEIGHT/4+10:
             self.dy = -self.dy
    

    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))
        