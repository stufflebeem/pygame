import pygame
from game_data import *

class Start():
    def __init__(self):
        self.silver = (168, 169, 174)
        self.black = (0, 0, 0)
        self.title_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        self.title_surface = self.title_font.render('𝕬𝖉𝖛𝖊𝖓𝖙𝖚𝖗𝖊 𝕲𝖆𝖒𝖊', 1, self.silver)
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.center = (WIDTH//2, HEIGHT//2)
        self.instructions_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 24)
        self.image = pygame.Surface([WIDTH, HEIGHT],pygame.SRCALPHA)
        self.image.fill(self.black)
        self.rect = self.image.get_rect()
        self.presses = 0
        self.birth_time = pygame.time.get_ticks()
        self.death_time = 3600
        

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            self.presses += 1
    
    def draw(self, screen):
        if self.presses < 3:
            screen.blit(self.image, (0,0))
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/self.death_time
            alpha = 255 - current_age_percent * 255
            self.title_surface.set_alpha(alpha)
            screen.blit(self.title_surface, self.title_rect)
            if alpha < 1:
                self.presses += 3
        if self.presses >= 3 and self.presses < 6:
            screen.blit(self.image, (0,0))
            for i in instructions:
                self.instructions_surface = self.instructions_font.render(i, 1, self.silver)
                self.instructions_rect = self.title_surface.get_rect()
                self.instructions_rect.center = (WIDTH//2, HEIGHT//4 + instructions.index(i)*64)
                screen.blit(self.instructions_surface, self.instructions_rect)
            
        if self.presses > 6:
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/(self.death_time*3)
            alpha = 255 - current_age_percent * 255
            self.image.set_alpha(alpha)
            screen.blit(self.image, (0,0))

        
        
        

class Score():
    def __init__ (self):
        self.black = (0, 0, 0)
        self.score_width = 3
        self.score_height = 1
        self.image = pygame.Surface([self.score_width*ui_tile_size,self.score_height*ui_tile_size],pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0,0,0,0))

        self.score_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 20)
        self.score_surface = self.score_font.render('0', 1, self.black)
        
        # sequentially loads chosen tree sprite from a dictionary and blits it to given positions
        for i in user_interface['score']:
            for x in range (user_interface['score'][i]['pos_x'][0],user_interface['score'][i]['pos_x'][1]):
                for y in range(user_interface['score'][i]['pos_y'][0],user_interface['score'][i]['pos_y'][1]):
                    self.image.blit(pygame.image.load(user_interface['score'][i]['img']), (x * tile_size, y * tile_size))
    
    def update_score(self, score):
        self.score_surface = self.score_font.render(f"{score}", 1, self.black)
    
    def draw(self, screen_surface):
        """screen_surface: game surface for the background to be blitted onto
           camera_x: camera x position on the visible screen
           camera_y: camera y position on the visible screen"""
        screen_x = 17
        screen_y = 17
        screen_surface.blit(self.image, (screen_x, screen_y))
        screen_surface.blit(self.score_surface, (32,22))

class Game_over():
    def __init__ (self):
        self.black = (0,0,0)
        self.red = (255,0,0)
        self.game_over_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        self.game_over_surface = self.game_over_font.render('You Died', 1, self.red)
        self.title_rect = self.game_over_surface.get_rect()
        self.title_rect.center = (WIDTH//2, HEIGHT//2)
        self.instructions_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 24)
        self.image = pygame.Surface([WIDTH, HEIGHT],pygame.SRCALPHA)
        self.image.fill(self.black)
        self.rect = self.image.get_rect()
        self.game_over = False
        
    def update(self, player_group):
        player = player_group.sprites()[0]
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_e]):
            self.birth_time = pygame.time.get_ticks()
            self.death_time = 3600
            self.game_over = True
        if player.health <=0:
            self.birth_time = pygame.time.get_ticks()
            self.death_time = 3600
            self.game_over = True
    
    def draw(self, screen):
        if self.game_over == True:
            screen.blit(self.image, (0,0))
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/self.death_time
            alpha = current_age_percent * 255
            self.game_over_surface.set_alpha(alpha)
            screen.blit(self.game_over_surface, self.title_rect)