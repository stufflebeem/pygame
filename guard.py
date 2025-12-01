import pygame
from game_data import *
from map import *
from player import *
from items import *

# creates a class of sprite Player for the user to control
class Guard(pygame.sprite.Sprite):
    def __init__(self, building_group, guard_group, villager_group, orc_group):
        """items: list of items dictionary
           speed: the number of pixles the sprite moves per frame
           building_group: sprites in the buildings"""
        pygame.sprite.Sprite.__init__(self)
        
        # initializes movement
        self.map_x = 0
        self.map_y = 0
        self.dx = 0
        self.dy = 0

        # creates guard stats
        self.speed = 1
        self.defense = 1
        self.attack = 0
        self.range = 1
        self.health = 3
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
        self.items = {'model': guard_model, 'pants' : guard_pants, 'boots' : guard_boots, 'shirt' : guard_shirt,
                'hair' : "none", 'helmet' : guard_helmet, 'shield' : "none", 'weapon' : guard_weapon}
        blit_list = [guard_model,  guard_shirt, guard_pants, guard_boots, guard_helmet, guard_weapon]
        for b in blit_list:
           sprite = load_items(b)
           self.image.blit(sprite["sprite"],(0,0))

        
        # adjusts spawn location in case of spawning in object
        safe = False
        while safe == False:
            self.map_x = randint(int(0 + 12 * tile_size), int(map_width * tile_size - 13 * tile_size))
            self.map_y = randint(int(0 + 9 * tile_size), int(map_height * tile_size - 10 * tile_size))
            self.rect.topleft = (self.map_x, self.map_y)

            collision = [other for other in self.guard_group if other != self and self.rect.colliderect(other.rect)]
            if pygame.sprite.spritecollide(self, self.building_group, False):
                safe = False
            elif collision:
                safe = False
            elif pygame.sprite.spritecollide(self, self.villager_group, False):
                safe = False
            elif pygame.sprite.spritecollide(self, self.orc_group, False):
                safe = False
            else:
                safe = True
            
        # records safe spawning position
        self.last_map_x = self.map_x
        self.last_map_y = self.map_y
        
    # needs to create an automatically updating system for guards to move and ineract with the world around them
    def update(self,player_group):
        """player_group: player_group"""
        self.player_group = player_group
        try:
            player = self.player_group.sprites()[0]
        except IndexError:
            return None

        # checks health
        if self.health <= 0:
            self.guard_group.remove(self)


        # records last collison free position
        self.last_map_x = self.map_x
        self.last_map_y = self.map_y

        # flag to determine if the guard has detected a target orc
        target = False

        # loops over every orc to see if any are in a 80 tile radius
        closest_orc = None
        closest_distance = 800*tile_size
        for orc in self.orc_group: 
            distance = ((orc.map_x - self.map_x)**2 + (orc.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_orc = orc
                target = True
        
        # controls movement if guard has detected a orc
        if target == True:
            self.dx = 1 if closest_orc.map_x > self.map_x else -1
            self.dy = 1 if closest_orc.map_y > self.map_y else -1

        # creates movement at random intervals, every 10 seconds a guard should move at least once if no orc is detected
        else:
            movement = randint(1,600)
            if movement == 1:
                self.dx = 1 if randint(0,1) == 0 else -1
            if movement == 2:
                self.dy = 1 if randint(0,1) == 0 else -1

            # stops guards after around 2 seconds of movement
            if movement > 580:
                self.dx = 0
                self.dy = 0

        # updates position
        self.map_x += self.dx
        self.map_y += self.dy
        self.rect.topleft = (self.map_x, self.map_y)

        # detects collisions between guard and buildings
        if pygame.sprite.spritecollide(self, self.building_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_x += 12*tile_size

        # detects collisions between guard and other guards
        collision = [other for other in self.guard_group if other != self and self.rect.colliderect(other.rect)]
        
        if collision:
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detects collisions between guard and villagers
        if pygame.sprite.spritecollide(self, self.villager_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

        # detect collisions between guard and orcs
        if pygame.sprite.spritecollide(self, self.orc_group, False):
            self.map_x = self.last_map_x
            self.map_y = self.last_map_y
            self.rect.topleft = (self.map_x, self.map_y)
            self.dx = 0
            self.dy = 0

            # detects collisions between guard and player
        if pygame.sprite.spritecollide(self, self.player_group, False):
            self.map_x += player.dx
            self.map_y += player.dy
            self.rect.topleft = (self.map_x, self.map_y)

            # detects collisions between guard and other guards
            collision = [other for other in self.guard_group if other != self and self.rect.colliderect(other.rect)]
            
            if collision:
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0

            # detects collisions between guard and villagers
            if pygame.sprite.spritecollide(self, self.villager_group, False):
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0

            # detect collisions between guard and orcs
            if pygame.sprite.spritecollide(self, self.orc_group, False):
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0    
                
            # detects collisions between guard and buildings
            if pygame.sprite.spritecollide(self, self.building_group, False):
                self.map_x = self.last_map_x
                self.map_y = self.last_map_y
                self.rect.topleft = (self.map_x, self.map_y)
                self.dx = 0
                self.dy = 0
            
        # defines world borders for guard
        if self.map_x < 0 + 12 * tile_size or self.map_x > map_width * tile_size - 13 * tile_size:
            self.map_x = self.last_map_x
            self.dx = 0
        if  self.map_y > map_height * tile_size - 10 * tile_size or self.map_y < 0 + 9 * tile_size:
             self.map_y = self.last_map_y
             self.dy = 0

        # attack orcs
        target = False
        closest_orc = None
        closest_distance = self.range * tile_size
        for orc in self.orc_group: 
            distance = ((orc.map_x - self.map_x)**2 + (orc.map_y - self.map_y)**2)**0.5 
            if distance < closest_distance:
                closest_distance = distance
                closest_orc = orc
                target = True
        if target == True and self.reload_time < pygame.time.get_ticks():
            closest_orc.health -= self.attack * (1/closest_orc.defense)
            closest_orc.dx = -self.dx
            closest_orc.dy = -self.dy
            self.reload_time = pygame.time.get_ticks() + self.reload * 60

    def draw(self, surface, camera_x, camera_y):
        """surface: the screen on which the sprite is drawn"""
        screen_x = self.map_x - camera_x
        screen_y = self.map_y - camera_y
        surface.blit(self.image, (screen_x, screen_y))
        