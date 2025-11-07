import pygame
from game_data import *

class Start():
    def __init__(self):
        self.silver = (168, 169, 174)
        self.black = (0, 0, 0)
        self.title_font = pygame.font.Font('fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        self.title_surface = self.title_font.render('Adventure Game', 1, self.silver)
        self.title_rect = self.title_surface.get_rect()
        self.title_rect.center = (WIDTH//2, HEIGHT//2)
        self.instructions_font = pygame.font.Font('fonts/LatinmodernmathRegular-z8EBa.otf', 24)
        self.birth_time = pygame.time.get_ticks()
        self.death_time = 5000
        self.image = pygame.Surface([WIDTH, HEIGHT],pygame.SRCALPHA)
        self.image.fill(self.black)
        self.rect = self.image.get_rect()
        self.presses = 0
        

    def update(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            self.presses += 1
    
    def draw(self, screen):
        if self.presses == 0:
            screen.blit(self.image, (0,0))
            birth_time = pygame.time.get_ticks()
            death_time = 10000 + birth_time
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/death_time
            alpha = 255 - current_age_percent * 255
            self.title_surface.set_alpha(alpha)
            screen.blit(self.title_surface, self.title_rect)
            if alpha == 0:
                self.presses += 3600
        if self.presses == 3600:
            screen.blit(self.image, (0,0))
            birth_time = pygame.time.get_ticks()
            death_time = 10000 + birth_time
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/death_time
            alpha = 255 - current_age_percent * 255
            for i in instructions:
                self.instructions_surface = self.instructions_font.render(i, 1, self.silver)
                self.instructions_rect = self.title_surface.get_rect()
                self.instructions_surface.set_alpha(alpha)
                self.instructions_rect.center = (WIDTH//2, HEIGHT//4 + instructions.index(i)*64)
                screen.blit(self.instructions_surface, self.instructions_rect)
                if alpha == 1:
                    self.presses += 3600
            
        if self.presses > 7200:
            birth_time = pygame.time.get_ticks()
            death_time = 10000 + birth_time
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/death_time
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

        self.score_font = pygame.font.Font('fonts/LatinmodernmathRegular-z8EBa.otf', 20)
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