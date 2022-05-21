# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 15:19:25 2018

@author: zou
"""
import pygame, random
import numpy as np

class Settings:
    def __init__(self):
        #changed first 2 value, to make the screen bigger
        self.width = 80
        self.height = 50
        #changing the rect length to accomodate the new sprite image
        self.rect_len = 40

class Background(pygame.sprite.Sprite):
    #new class to add a background image
    def __init__(self, image_file, location):
        #call Sprite initializer
        pygame.sprite.Sprite.__init__(self)  
        self.image = image_file
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Train:
    def __init__(self):
        #loading the required images for the sprites head
        self.image_left = pygame.image.load('images/trainHeadLeft.png')
        self.image_right = pygame.image.load('images/trainHeadRight.png')
        #loading the required image for the sprites tail
        self.tail = pygame.image.load('images/trainTail.png')

        #variable used to cycle through images for the train body
        self.num = 0
        

        self.initialize()

    def initialize(self):
        #initial position of the train
        self.position = [6, 6]
        #to fix the bug that cause the game to end if the train crashes on the left
        self.facing = "right"
        #the positions of each part of the train, the length of this list is the length of the train
        self.segments = [[6 - i, 6] for i in range(3)]
        self.score = 0

    def blit_body(self, x, y, screen):
        #loading the different coloured images of the train
        train_image = 'images/trainBody' + str(self.num % 8) + '.png'
        self.image_body = pygame.image.load(train_image)
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
        #so as the train continues moving downwards, the correct image is still displayed

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
        self.blit_head(self.segments[0][0]*(rect_len), self.segments[0][1]*(rect_len), screen)

        for position in self.segments[1:-1]:
            self.blit_body(position[0]*(rect_len), position[1]*(rect_len), screen)
        self.blit_tail(self.segments[-1][0]*(rect_len), self.segments[-1][1]*(rect_len), screen)                
             
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
        
class Person():
    def __init__(self, settings):
        self.settings = settings
        
        self.image = pygame.image.load('images/human.png')      
        self.initialize()
        
    def random_pos(self, train):
        self.image = pygame.image.load('images/human.png')          

        #the range of the random.randint has been changed to start at 1
        #this makes sure the person does not form on the edge

        ##new change the random int values are now in this range, based on tested values, 
        ## due to the change in rect_len
        self.position[0] = random.randint(1, 28)
        self.position[1] = random.randint(1, 17)
    
       #following block of code was causing a bug, spawning the food items only in a small section of the 
       #map
        
        if self.position in train.segments:
            self.random_pos(train)

    def blit(self, screen):
        screen.blit(self.image, [p * (self.settings.rect_len) for p in self.position])
   
    def initialize(self):
        self.position = [15, 10]
      
        
class Game:
    """
    """
    def __init__(self):
        self.settings = Settings()
        self.train = Train()
        self.person = Person(self.settings)
        self.move_dict = {0 : 'up',
                          1 : 'down',
                          2 : 'left',
                          3 : 'right'}       
        
    def restart_game(self):
        self.train.initialize()
        self.person.initialize()

    def current_state(self):         
        state = np.zeros((self.settings.width+2, self.settings.height+2, 2))
        expand = [[0, 1], [0, -1], [-1, 0], [1, 0], [0, 2], [0, -2], [-2, 0], [2, 0]]
        
        for position in self.train.segments:
            state[position[1], position[0], 0] = 1
        
        state[:, :, 1] = -0.5        

        state[self.person.position[1], self.person.position[0], 1] = 0.5
        for d in expand:
            state[self.person.position[1]+d[0], self.person.position[0]+d[1], 1] = 0.5
        return state
    
    def direction_to_int(self, direction):
        direction_dict = {value : key for key,value in self.move_dict.items()}
        return direction_dict[direction]
        
    def do_move(self, move):
        move_dict = self.move_dict
        
        change_direction = move_dict[move]
        
        #change if to elif, less number of checks and make the movement a bit more smooth
        if change_direction == 'right' and not self.train.facing == 'left':
            self.train.facing = change_direction
        elif change_direction == 'left' and not self.train.facing == 'right':
            self.train.facing = change_direction
        elif change_direction == 'up' and not self.train.facing == 'down':
            self.train.facing = change_direction
        elif change_direction == 'down' and not self.train.facing == 'up':
            self.train.facing = change_direction

        self.train.update()
    
        if self.train.position == self.person.position:
            self.person.random_pos(self.train)
            reward = 1
            self.train.score += 1
        else:
            self.train.segments.pop()
            reward = 0
                
        if self.game_end():
            return -1
                    
        return reward
    
    def game_end(self):
        end = False
        #hardcoding the values, based on the tested value outputs  
        if self.train.position[0] >= 30 or self.train.position[0] < 0:
            end = True
            #making sure the train re initializes facing right, fixing bug where it crashes 
            #on spawn

        if self.train.position[1] >= 19 or self.train.position[1] < 0:
            #making sure the train re initializes facing right, fixing bug where it crashes 
            #on spawn
            end = True

        if self.train.segments[0] in self.train.segments[1:]:
            #making sure the train re initializes facing right, fixing bug where it crashes 
            #on spawn
            end = True



        return end
    
    def blit_score(self, color, screen):
        font = pygame.font.SysFont(None, 25)
        text = font.render('Score: ' + str(self.train.score), True, color)
        screen.blit(text, (0, 0))

