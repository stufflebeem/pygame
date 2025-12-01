import pygame
from game_data import *

class Start():
    def __init__(self):

        # creates variables for text
        self.silver = (168, 169, 174)
        self.black = (0, 0, 0)
        self.title_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        self.instructions_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 24)

        # creates a title surface and a rectangle
        self.title_surface = self.title_font.render('𝕬𝖉𝖛𝖊𝖓𝖙𝖚𝖗𝖊 𝕲𝖆𝖒𝖊', 1, self.silver)
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.center = (WIDTH//2, HEIGHT//2)

        # creates a rectangle and image to blit
        self.image = pygame.Surface([WIDTH, HEIGHT],pygame.SRCALPHA)
        self.image.fill(self.black)
        self.rect = self.image.get_rect()

        # creates variables for effects
        self.presses = 0
        self.birth_time = pygame.time.get_ticks()
        self.death_time = 3600
        

    def update(self, presses):
        """presses: number of times the space bar is pressed"""
        self.presses = presses
    
    def draw(self, screen):
        """screen: blit location for text"""

        # start screen with adventure game text
        if self.presses <= 1:
            screen.blit(self.image, (0,0))
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/self.death_time
            alpha = 255 - current_age_percent * 255
            self.title_surface.set_alpha(alpha)
            screen.blit(self.title_surface, self.title_rect)
            if alpha < 1:
                self.presses += 3
        
        # instruction screen with instructions text
        if self.presses == 2:
            screen.blit(self.image, (0,0))
            for i in instructions:
                self.instructions_surface = self.instructions_font.render(i, 1, self.silver)
                self.instructions_rect = self.title_surface.get_rect()
                self.instructions_rect.center = (WIDTH//2, HEIGHT//4 + instructions.index(i)*64)
                screen.blit(self.instructions_surface, self.instructions_rect)
        
        # black screen fading into game
        if self.presses > 2:
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/(self.death_time*3)
            alpha = 255 - current_age_percent * 255
            self.image.set_alpha(alpha)
            screen.blit(self.image, (0,0))        

class Score():
    def __init__ (self):

        # creates variables for text
        self.black = (0, 0, 0)
        self.score_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 20)
        self.score_width = 3
        self.score_height = 1

        # creates surface and image for text
        self.score_surface = self.score_font.render('0', 1, self.black)
        self.image = pygame.Surface([self.score_width*ui_tile_size,self.score_height*ui_tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))

        # sequentially loads chosen ribbon sprite from a dictionary and blits it to given positions
        for i in user_interface['score']:
            for x in range (user_interface['score'][i]['pos_x'][0],user_interface['score'][i]['pos_x'][1]):
                for y in range(user_interface['score'][i]['pos_y'][0],user_interface['score'][i]['pos_y'][1]):
                    self.image.blit(pygame.image.load(user_interface['score'][i]['img']), (x * tile_size, y * tile_size))
    
    def update_score(self, level, game_over):
        """level = current number of orcs that spawned, reflected in score
            game_over: bolean that determines gamestate"""
        
        # logic to stop increasing score if gameover
        if game_over.game_over == False:
            self.score_time = int(pygame.time.get_ticks()/5400)
        
        # displays score surface and calculates score
        self.score_level = level * 100
        self.score = self.score_time + self.score_level
        self.score_surface = self.score_font.render(f"{self.score}", 1, self.black)
    
    def draw(self, screen_surface):
        """screen_surface: game surface for the background to be blitted onto"""
        screen_x = 17
        screen_y = 17
        screen_surface.blit(self.image, (screen_x, screen_y))
        screen_surface.blit(self.score_surface, (32,22))

class Game_over():
    def __init__ (self):

        # creates variables for text
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.game_over_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        self.score_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 50)

        # creates surface, rectangle, and image for game over
        self.game_over_surface = self.game_over_font.render('You Died', 1, self.red)
        self.game_over_rect = self.game_over_surface.get_rect()
        self.game_over_rect.center = (WIDTH//2, HEIGHT//2)
        self.image = pygame.Surface([WIDTH, HEIGHT],pygame.SRCALPHA)
        self.image.fill(self.black)
        self.rect = self.image.get_rect()

        # starts game
        self.game_over = False
        self.stopped = False
        
    def update(self, player_group, villager_group):
        """player_group: player in list
            villager_group: list of all villagers"""
        self.player_group = player_group
        player = self.player_group.sprites()[0]

        # ends the game if villagers are all dead or player health drops to zero.
        if self.stopped == False:
            if player.health <= 0:
                self.stopped = True
                self.birth_time = pygame.time.get_ticks()
                self.death_time = 3600
                self.game_over = True
            if len(villager_group)<= 0:
                self.stopped = True
                self.birth_time = pygame.time.get_ticks()
                self.death_time = 3600
                self.game_over = True
        else:
            return
    
    
    def draw(self, screen, score):
        """screen: location for blit text
            score: score obtained by player"""
        
        if self.game_over == True:
            pygame.mixer.music.stop()

            # makes screen black
            screen.blit(self.image, (0,0))

            # fading in function
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/self.death_time
            alpha = current_age_percent * 255
            self.game_over_surface = self.game_over_font.render('You Died', 1, self.red)
            self.game_over_surface.set_alpha(alpha)
            self.score_surface = self.score_font.render(f'Score: {score.score}', 1, self.red)
            self.score_surface.set_alpha(alpha)
            self.score_rect = self.game_over_surface.get_rect()
            self.score_rect.center = (WIDTH//2, 3*HEIGHT//4)

            # draws text on screen
            screen.blit(self.game_over_surface, self.game_over_rect)
            screen.blit(self.score_surface, self.score_rect)

def pause(paused, screen):
    if paused:
        # writes paused on the screen if the game is paused
        silver = (168, 169, 174)
        paused_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        paused_surface = paused_font.render('𝕻𝖆𝖚𝖘𝖊𝖉', 1, silver)
        paused_rect = paused_surface.get_rect()
        paused_rect.center = (WIDTH//2, HEIGHT//2)
        screen.blit(paused_surface, paused_rect)