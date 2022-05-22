# -*- coding: utf-8 -*-
"""
Created on Wed May 16 15:22:20 2018

@author: zou
"""

import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
import os, sys

from game import Game
from game import Background

def base_path(path):
    basedir =  os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, path)

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

green = pygame.Color(0, 200, 0)
bright_green = pygame.Color(0, 255, 0)
red = pygame.Color(200, 0, 0)
bright_red = pygame.Color(255, 0, 0)
blue = pygame.Color(32, 178, 170)
bright_blue = pygame.Color(32, 200, 200)
yellow = pygame.Color(255, 205, 0)
bright_yellow = pygame.Color(255, 255, 0)

# Loading the background
background = pygame.image.load(base_path('images/background.png'))
# Creating background class
BackGround = Background(background, [0,0])

#Loading the Cover image
cover = pygame.image.load(base_path('images/Cover_Image.jpeg'))
#creating Cover image
Cover = Background(cover, [0,0])

game = Game()
rect_len = game.settings.rect_len
train = game.train
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))
pygame.display.set_caption('Gluttonous')

crash_sound = pygame.mixer.Sound(base_path('sound/crash2.wav'))
drift_sound = pygame.mixer.Sound(base_path('sound/tokyo_drift.wav'))
turn_drift = pygame.mixer.Sound(base_path('sound/turn_drift.wav'))
background_music = pygame.mixer.Sound(base_path('sound/Background_music.wav'))


def text_objects(text, font, color=black):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    large_text = pygame.font.SysFont('ヒラキノ角コシックw3', 100)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
            else:
                action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    smallText = pygame.font.SysFont('comicsansms', 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))
    screen.blit(TextSurf, TextRect)
    return True


def quitgame():
    pygame.quit()
    quit()


def crash():
    # Stop the background sound immediately after the player crashes
    pygame.mixer.Sound.stop(drift_sound)
    pygame.mixer.Sound.play(crash_sound)
    message_display('Crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(2)
    screen.fill(white)
    screen.blit(Cover.image, Cover.rect)


def initial_interface():
    
    intro = True
    screen.fill(white)
    screen.blit(Cover.image, Cover.rect)
    timer = 0
    flag = False
    
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        if flag == True:
            flag = True
            timer = 0

        # Background Music
        if timer == 0:
            pygame.mixer.Sound.play(background_music)
            pygame.mixer.Sound.set_volume(background_music,0.35)
            timer = 6045
        timer -=1

        message_display('Gluttonous',  game.settings.width / 2 * 20,  game.settings.height / 4 * 5, color=(100,100,100))

        flag = button('Go!', 510, 340, 100, 50, green, bright_green, game_loop, 'human')
        button('Quit', 670, 340, 100, 50, red, bright_red, quitgame)
        
        #adjusted the position of the buttons for the new screen size
        
        pygame.display.update()
        pygame.time.Clock().tick(15)


def game_loop(player, fps=10):
    pygame.mixer.Sound.stop(background_music)
    game.restart_game()
    timer = 0
    which_turn = "right"

    while not game.game_end():

        pygame.event.pump()
        
        # Play the Background music on repeat
        if timer == 0:
            pygame.mixer.Sound.set_volume(drift_sound,0.35)
            pygame.mixer.Sound.play(drift_sound)
            timer = 172
        
        timer -=1
        
        # Turn Sound
        if which_turn != train.facing:
            pygame.mixer.Sound.stop(turn_drift)
            which_turn = train.facing
            pygame.mixer.Sound.play(turn_drift)

        move = human_move()
        #changing the fps to 6, as the game runs best at this fps, when compared with other 
        #values
        fps = 6

        game.do_move(move)

        # Add the screen background
        screen.fill(white)
        screen.blit(BackGround.image, BackGround.rect)

        game.train.blit(rect_len, screen)
        game.person.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    direction = train.facing

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        elif event.type == KEYDOWN:
            if event.key == K_RIGHT or event.key == ord('d'):
                direction = 'right'
            if event.key == K_LEFT or event.key == ord('a'):
                direction = 'left'
            if event.key == K_UP or event.key == ord('w'):
                direction = 'up'
            if event.key == K_DOWN or event.key == ord('s'):
                direction = 'down'
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    move = game.direction_to_int(direction)
    return move


if __name__ == "__main__":
    os.chdir(base_path(''))
    initial_interface()
