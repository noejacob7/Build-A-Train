# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np
import os, sys


def base_path(path):
    if getattr(sys, 'frozen', None):
        basedir = sys._MEIPASS
    else:
        basedir =  os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, path)


class Settings:
    def __init__(self):
        
        # Change the width and height to make a bigger screen
        self.width = 80
        self.height = 50
        #changing the rect length to accomodate the new sprite image
        self.rect_len = 40
        
# Created a new class to account for an external background image
class Background(pygame.sprite.Sprite):
    #new class to add a background image
    def __init__(self, image_file, location):
        #call Sprite initializer
        pygame.sprite.Sprite.__init__(self)  
        self.image = image_file
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Snake:
    def __init__(self):
        #loading the required images for the sprites head
        self.image_left = pygame.image.load(base_path('images/trainHeadLeft.png'))
        self.image_right = pygame.image.load(base_path('images/trainHeadRight.png'))
        #loading the required image for the sprites tail
        self.tail = pygame.image.load(base_path('images/trainTail.png'))

        #variable used to cycle through images for the train body
        self.num = 0
        

        self.initialize()

    def initialize(self):
        self.position = [6, 6]
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0
        self.facing = "right"

    def blit_body(self, x, y, screen):
        #loading the different coloured images of the train
        train_image = 'images/trainBody' + str(self.num % 8) + '.png'
        self.image_body = pygame.image.load(base_path(train_image))
        #incrementing the number to cycle through the images
        self.num += 1
        #displaying the required image and the coordinates of the train
        screen.blit(self.image_body, (x, y))
        
    def blit_head(self, x, y, screen):
        #the position of the second and third part of the sprite
        #done to know the correct orientation sprite head, as will be shown later in the code
        second_elem = self.segments[1]
        third_elem = self.segments[2]

        #if left display left image
        if self.facing == "left":
            screen.blit(self.image_left, (x, y))  

        #if right face display right
        elif self.facing == "right":
            screen.blit(self.image_right, (x, y))

        #self.carry_on remembers the current image of the sprites head
        #so as the train continues moving downwards or upwards, the correct image is still displayed

        #direction is downward, and the sprite was previously moving right
        #the orientation of the head of the sprite remains right
        elif self.facing == "down" and second_elem[0] > third_elem[0] and second_elem[1] == third_elem[1]:
            screen.blit(self.image_right, (x, y))
            self.carry_on = self.image_right
        
        #direction is upward, and the sprite was previously moving right
        #the orientation of the head of the sprite remains right
        elif self.facing == "up" and second_elem[0] > third_elem[0] and second_elem[1] == third_elem[1]:
            screen.blit(self.image_right, (x, y))
            self.carry_on = self.image_right

        #direction is downward, and the sprite was previously moving left
        #the orientation of the head of the sprite remains left
        elif self.facing == "down" and second_elem[0] < third_elem[0] and second_elem[1] == third_elem[1]:
            screen.blit(self.image_left, (x, y))
            self.carry_on = self.image_left
        
        #direction is upward, and the sprite was previously moving left
        #the orientation of the head of the sprite remains left
        elif self.facing == "up" and second_elem[0] < third_elem[0] and second_elem[1] == third_elem[1]:
            screen.blit(self.image_left, (x, y))
            self.carry_on = self.image_left
        
        #the sprite already turned and is continues to move downwards
        elif self.facing == "down":
            screen.blit(self.carry_on, (x, y))
        
        #sprite already turned and continues to move upward
        elif self.facing == "up":
            screen.blit(self.carry_on, (x, y)) 
            
     def blit_tail(self, x, y, screen):
        #subtracting the last and second last segments x and y coordinates, and based
        #on that the direction of the tail of train changes
        tail_direction = [self.segments[-2][i] - self.segments[-1][i] for i in range(2)]
        if tail_direction == [0, -1]:
            screen.blit(self.tail, (x, y))
        elif tail_direction == [0, 1]:
            screen.blit(self.tail, (x, y))  
        elif tail_direction == [-1, 0]:
            screen.blit(self.tail, (x, y))  
        else:
            screen.blit(self.tail, (x, y)) 
    
    def blit(self, rect_len, screen):
        self.blit_head(self.segments[0][0]*rect_len, self.segments[0][1]*rect_len, screen)                
        for position in self.segments[1:-1]:
            self.blit_body(position[0]*rect_len, position[1]*rect_len, screen)
        self.blit_tail(self.segments[-1][0]*rect_len, self.segments[-1][1]*rect_len, screen)                
            
    
    def update(self):
        if self.facing == 'right':
            self.position[0] += 1
        if self.facing == 'left':
            self.position[0] -= 1
        if self.facing == 'up':
            self.position[1] -= 1
        if self.facing == 'down':
            self.position[1] += 1
        self.segments.insert(0, list(self.position))
        
class Strawberry():
    def __init__(self, settings):
        self.settings = settings
        
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load(base_path('images/food' + str(self.style) + '.bmp'))
        self.initialize()
        
    def random_pos(self, snake):
        self.style = str(random.randint(1, 8))
        self.image = pygame.image.load(base_path('images/food' + str(self.style) + '.bmp'))
        
        self.position[0] = random.randint(0, self.settings.width-1)
        self.position[1] = random.randint(0, self.settings.height-1)
    
#         It is causing the food/ collectable to spawn in a small area.
#         self.position[0] = random.randint(9, 19)
#         self.position[1] = random.randint(9, 19)
        
        if self.position in snake.segments:
            self.random_pos(snake)

    def blit(self, screen):
        screen.blit(self.image, [p * self.settings.rect_len for p in self.position])
   
    def initialize(self):
        self.position = [15, 10]
      
        
class Game:
    """
    """
    def __init__(self):
        self.settings = Settings()
        self.snake = Snake()
        self.strawberry = Strawberry(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
        
    def restart_game(self):
        self.snake.initialize()
        self.strawberry.initialize()

    def current_state(self):         
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.snake.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.strawberry.position[1], self.strawberry.position[0], 1] = 0.5
        for d in expand:
            state[self.strawberry.position[1]+d[0], self.strawberry.position[0]+d[1], 1] = 0.5
        return state
    
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    def do_move(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        if change_direction == 'right' and not self.snake.facing == 'left':
            self.snake.facing = change_direction
        if change_direction == 'left' and not self.snake.facing == 'right':
            self.snake.facing = change_direction
        if change_direction == 'up' and not self.snake.facing == 'down':
            self.snake.facing = change_direction
        if change_direction == 'down' and not self.snake.facing == 'up':
            self.snake.facing = change_direction

        self.snake.update()
        
        if self.snake.position == self.strawberry.position:
            self.strawberry.random_pos(self.snake)
            reward = 1
            self.snake.score += 1
        else:
            self.snake.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward
    
    def game_end(self):
        end = False
        if self.snake.position[0] >= self.settings.width or self.snake.position[0] < 0:
            end = True
        if self.snake.position[1] >= self.settings.height or self.snake.position[1] < 0:
            end = True
        if self.snake.segments[0] in self.snake.segments[1:]:
            end = True

        return end
    
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.snake.score), True, color)
        screen.blit(text, (0, 0))

