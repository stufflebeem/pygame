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
        

    def update(self, presses):
        self.presses = presses
    
    def draw(self, screen):
        if self.presses <= 1:
            screen.blit(self.image, (0,0))
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/self.death_time
            alpha = 255 - current_age_percent * 255
            self.title_surface.set_alpha(alpha)
            screen.blit(self.title_surface, self.title_rect)
            if alpha < 1:
                self.presses += 3
        if self.presses == 2:
            screen.blit(self.image, (0,0))
            for i in instructions:
                self.instructions_surface = self.instructions_font.render(i, 1, self.silver)
                self.instructions_rect = self.title_surface.get_rect()
                self.instructions_rect.center = (WIDTH//2, HEIGHT//4 + instructions.index(i)*64)
                screen.blit(self.instructions_surface, self.instructions_rect)
            
        if self.presses > 2:
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
    
    def update_score(self, level, game_over):
        if game_over.game_over == False:
            self.score_time = int(pygame.time.get_ticks()/5400)
        self.score_level = level * 100
        self.score = self.score_time + self.score_level
        self.score_surface = self.score_font.render(f"{self.score}", 1, self.black)
    
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
        self.score_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 50)
        self.game_over_surface = self.game_over_font.render('You Died', 1, self.red)
        self.game_over_rect = self.game_over_surface.get_rect()
        self.game_over_rect.center = (WIDTH//2, HEIGHT//2)
        self.image = pygame.Surface([WIDTH, HEIGHT],pygame.SRCALPHA)
        self.image.fill(self.black)
        self.rect = self.image.get_rect()
        self.game_over = False
        self.stopped = False
        
    def update(self, player_group, villager_group):
        self.player_group = player_group
        player = self.player_group.sprites()[0]
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
        if self.game_over == True:
            pygame.mixer.music.stop()
            screen.blit(self.image, (0,0))
            current_age = pygame.time.get_ticks() - self.birth_time
            current_age_percent = current_age/self.death_time
            alpha = current_age_percent * 255
            self.game_over_surface = self.game_over_font.render('You Died', 1, self.red)
            self.game_over_surface.set_alpha(alpha)
            self.score_surface = self.score_font.render(f'Score: {score.score}', 1, self.red)
            self.score_surface.set_alpha(alpha)
            self.score_rect = self.game_over_surface.get_rect()
            self.score_rect.center = (WIDTH//2, 3*HEIGHT//4)
            screen.blit(self.game_over_surface, self.game_over_rect)
            screen.blit(self.score_surface, self.score_rect)

def pause(paused, screen):
    if paused:
        silver = (168, 169, 174)
        paused_font = pygame.font.Font('ui_pack/fonts/LatinmodernmathRegular-z8EBa.otf', 80)
        paused_surface = paused_font.render('𝕻𝖆𝖚𝖘𝖊𝖉', 1, silver)
        paused_rect = paused_surface.get_rect()
        paused_rect.center = (WIDTH//2, HEIGHT//2)
        screen.blit(paused_surface, paused_rect)