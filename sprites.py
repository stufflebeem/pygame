import pygame

def get_sprite(sheet, x, y, width, height):
    """extracts sprites from a spritesheet where:
    sheet: loaded sprite image sheet
    x: X coordinate of top-left corner of sprite
    y: Y coordinate of top-left corner of sprite
    width: Width of the sprite
    height: Height of the sprite"""
    # creates surface space for the sprite
    sprite_image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    # blits desired sprite onto the new surface
    sprite_image.blit(sheet, (0,0), (x, y, width, height))
    return sprite_image

# creates a class of sprite Player for the user to control
class Player():
    def __init__(self, world_x, world_y, speed):
        """world_x: the x coordinate of the sprite on the map
           world_y: the y coordinate of the sprite on the map
           speed: the number of pixles the sprite moves per frame"""
        self.world_x = world_x
        self.world_y = world_y
        self.speed = speed
        
    def player_frame(self,sprite_sheet, x, y):
        """sprite_sheet: the sheet where the sprite is located
           x: the x coordinate of the sprite on the sprite sheet
           y: the y coordinate of the sprite on the sprite sheet"""
        self.sprite = get_sprite(sprite_sheet, x, y, 16, 16)

    def draw(self, surface, screen_x, screen_y):
        """surface: the screen on which the sprite is drawn
           screen_x: the x coordinate of the sprite on the screen
           screen_y: the y coordinate of the sprite on the screen"""
        self.screen_x = screen_x
        self.screen_y = screen_y
        surface.blit(self.sprite, (self.screen_x, self.screen_y))
    
    def keys(self):
        """takes keystroke inputs and changes the position of the sprite on the map relative to
        the speed"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.world_x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.world_x += self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.world_y += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.world_y -= self.speed

    def adjust_speed(self):
        """changes the speed of the sprite based on LSHIFT and LCRTL inputs"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed += 0.1
        if keys[pygame.K_LCTRL]:
            self.speed -= 0.1
        self.speed = abs(self.speed)

# Creates a class called tiles to create maps and backgrounds
class Tiles():
    def __init__(self):
       """initializes the tile, creates variables for the map"""
       self.image = pygame.image.load('town/tiles/tile_0001.png').convert_alpha()
       self.tile_size = 16
       self.map_width = 80
       self.map_height = 80

    def draw(self,surface, camera_x, camera_y):
        """draws the tiles on a surface the size of the map and shows the area visible on the screen"""
        for x in range(self.map_width):
            for y in range(self.map_height):
                tile_world_x = x * self.tile_size
                tile_world_y = y * self.tile_size
                screen_x = tile_world_x - camera_x
                screen_y = tile_world_y - camera_y
                surface.blit(self.image, (screen_x,screen_y))

# creates a class of Items for the Player and others to wear and use
class Items():
    def __init__(self, sprite_sheet):
        self.sprite_sheet = sprite_sheet
    def pants_black(self):
        self.pants_black = get_sprite(self.sprite_sheet, 51, 0, 16, 16)
    def pants_brown(self):
        self.pants_brow = get_sprite(self.sprite_sheet, 51, 17, 16, 16)
    def pants_iron(self):
        self.pants_iron = get_sprite(self.sprite_sheet, 51, 34, 16, 16)
    def pants_leather(self):
        self.pants_leather = get_sprite(self.sprite_sheet, 51, 51, 16, 16)
    def pants_red(self):
        self.pants_leather = get_sprite(self.sprite_sheet, 51, 85, 16,16)
    def pants_blue(self):
        self.pants_blue = get_sprite(self.sprite_sheet, 51, 102, 16,16)
    def pants_purple(self):
        self.pants_purple = get_sprite(self.sprite_sheet, 51, 119, 16, 16)
    def pants_green(self):
        self.pants_green = get_sprite(self.sprite_sheet, 51, 136, 16, 16)
    def dress_blue(self):
        self.pants_green = get_sprite(self.sprite_sheet, 51, 68, 16, 16)
    def dress_brown(self):
        self.dress_brown = get_sprite(self.sprite_sheet, 51, 170, 16, 16)
    def dress_red(self):
        self.dress_red = get_sprite(self.sprite_sheet, 68, 68, 16, 16)
    def dress_purple(self):
        self.dress_purple = get_sprite(self.sprite_sheet, 51, 170, 16, 16)
    def boots_black(self):
        self.boots_black = get_sprite(self.sprite_sheet, 85, 0, 16, 16)
    def boots_brown(self):
        self.boots_brown = get_sprite(self.sprite_sheet, 85, 17, 16, 16)
    def boots_iron(self):
        self.boots_iron = get_sprite(self.sprite_sheet, 85, 34, 16, 16)
    def boots_leather(self):
        self.boots_iron = get_sprite(self.sprite_sheet, 85, 51, 16, 16)
    def boots_red(self):
        self.boots_red = get_sprite(self.sprite_sheet, 85, 85, 16, 16)
    def boots_blue(self):
        self.boots_blue = get_sprite(self.sprite_sheet, 85, 102, 16, 16)
    def boots_purple(self):
        self.boots_purple = get_sprite(self.sprite_sheet, 85, 119, 16, 16)
    def boots_green(self):
        self.boots_green = get_sprite(self.sprite_sheet, 85, 136, 16, 16)