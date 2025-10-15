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
    def __init__(self, player_x, player_y, player_speed):
        """player_x: the x coordinate of the sprite
           player_y: the y coordinate of the sprite
           player_speed: the number of pixles the sprite moves per frame"""
        self.player_x = player_x
        self.player_y = player_y
        self.player_speed = player_speed

    def player_frame(self,sprite_sheet, sprite_sheet_x, sprite_sheet_y):
        """sprite_sheet: the sheet where the sprite is located
           sprite_sheet_x: the x coordinate of the sprite on the sprite sheet
           sprite_sheet_y: the y coordinate of the sprite on the sprite sheet"""
        self.player_frame = get_sprite(sprite_sheet, sprite_sheet_x, sprite_sheet_y, 16, 16)
        self.sprite_sheet_x = sprite_sheet_x
        self.sprite_sheet_y = sprite_sheet_y

    def draw(self, surface):
        "surface: the screen on which the sprite is drawn"
        surface.blit(self.player_frame, (self.player_x, self.player_y))

    def keys(self):
        """takes keystroke inputs and changes the position of the sprite on the screen relative to
        the player_speed"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_y += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_y -= self.player_speed
    def speed(self):
        speed = pygame.key.get_pressed()
        if speed[pygame.K_LSHIFT]:
            self.player_speed += 0.1
        if speed[pygame.K_LCTRL]:
            self.player_speed -= 0.1
        if self.player_speed < 0:
            self.player_speed = abs(self.player_speed)

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
        self.dress_purple = get_sprite(self.prite_sheet, 51, 170, 16, 16)
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