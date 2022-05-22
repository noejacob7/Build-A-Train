from enum import Flag
import pygame
import time
from pygame.locals import KEYDOWN, K_RIGHT, K_LEFT, K_UP, K_DOWN, K_ESCAPE
from pygame.locals import QUIT
import os

from game import Game
from game import Background


def base_path(path):
    """
    Param path: The path of the file needed for the game.
    Returns the relative path of the file according to the current directory

    This function takes in the path of the file needed and adds the absolute pathname of the program (main.py)
    """
    basedir =  os.path.abspath(os.path.dirname(__file__))
    return os.path.join(basedir, path)

# Set variables for the pygame RGB colours
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
orange = pygame.Color(204,85,0)

# Loading the background image
background = pygame.image.load(base_path('images/background.png'))
# Creating background class
BackGround = Background(background, [0,0])

# Loading the Cover image
cover = pygame.image.load(base_path('images/Cover_Image.png'))
# Creating Cover class
Cover = Background(cover, [0,0])

# Loading the Game Over image
game_over = pygame.image.load(base_path('images/Game_over.jpeg'))
# Creating Game_over class
Game_over = Background(game_over, [0,0])

# Initialize the game class and all the settings required
game = Game()
rect_len = game.settings.rect_len
train = game.train
pygame.init()
fpsClock = pygame.time.Clock()

# Set the screen size
screen = pygame.display.set_mode((game.settings.width * 15, game.settings.height * 15))

# Set the game caption
pygame.display.set_caption('Build the Train')

# Read in each sound files
crash_sound = pygame.mixer.Sound(base_path('sound/crash2.wav'))
drift_sound = pygame.mixer.Sound(base_path('sound/tokyo_drift.wav'))
turn_drift = pygame.mixer.Sound(base_path('sound/turn_drift.wav'))
background_music = pygame.mixer.Sound(base_path('sound/Background_music.wav'))


def text_objects(text, font, color=black):
    """
    Param text: The String to be displayed
    Param Font: The Font to be used
    Param Color: The colour to be used

    Returns the source of the image and the destination of the image to be drawn in the game window.
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color=black):
    """
    Param text: The string to be written in the screen
    Param x,y: The coordinates where the message should be displayed
    Param color: The color of the message
    
    The function displays the message with the given parameters in the game window.
    """
    large_text = pygame.font.SysFont('cambria', 70)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (x, y)
    screen.blit(text_surf, text_rect)
    pygame.display.update()


def button(msg, x, y, w, h, inactive_color, active_color, action=None, parameter=None):
    """
    Param msg: The string to be displayed in the button
    Param x,y: Coordinates of where to display the button
    Param w,h: The dimentions of the button box
    Param inactive_color: The colour when when the position of the mouse is outside the box
    Param active_color: The colour when when the position of the mouse is inside the box
    Param action: The function to run if the player clicks the button
    Param parameter: the parameter to be passed into the action function if the player clicks the button

    Returns True if the function runs successfully

    The function displays the buttons and checks if the player pressed the button.
    If the player pressed the button runs the function to start the game.
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    flag = False
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, w, h))
        if click[0] == 1 and action != None:
            if parameter != None:
                action(parameter)
                flag = True
            else:
                action()
                flag = True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, w, h))

    # Creating the button elements
    smallText = pygame.font.SysFont('cambria', 30)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = (x + (w / 2), y + (h / 2))

    # Displaying the button
    screen.blit(TextSurf, TextRect)
    return flag


def quitgame():
    """Quits the pygame window and closes the program."""
    pygame.quit()
    quit()


def crash():
    """
    Stops all the other sounds and plays the crash sound.
    Displays that the player has crashed
    Clears the screen and put up the lobby image.
    """
    # Stop the background sound immediately after the player crashes
    pygame.mixer.Sound.stop(drift_sound)
    pygame.mixer.Sound.play(crash_sound)
    message_display('Crashed', game.settings.width / 2 * 15, game.settings.height / 3 * 15, white)
    time.sleep(0.4)

    # Game Over screen
    screen.fill(white)
    screen.blit(Game_over.image, Game_over.rect)
    message_display('Your Score: ' + str(train.score), game.settings.width / 2 * 15, game.settings.height / 3 * 30, orange)
    time.sleep(2)

    # Change to cover image
    screen.fill(white)
    screen.blit(Cover.image, Cover.rect)


def initial_interface():
    """
    This function displays the lobby page of the game and refreshes at 15 fps.
    The background music is played on repeat until the game starts.
    """
    
    intro = True

    # Display the Cover image
    screen.fill(white)
    screen.blit(Cover.image, Cover.rect)

    # Initialize the timer
    timer = 0
    flag = False
    
    while intro:

        # Check if the player wants to quit the game.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # Check if the player has played the game before.
        if flag == True:
            flag = False
            timer = 0

        # Background Music
        if timer == 0:
            pygame.mixer.Sound.play(background_music)
            pygame.mixer.Sound.set_volume(background_music,0.35)
            timer = 6045
        timer -=1

        # Buttons for starting the game and quitting it. 
        flag = button('Go!', 700, 220, 100, 50, green, bright_green, game_loop, 'human')
        button('Quit', 850, 220, 100, 50, red, bright_red, quitgame)
        
        # Update the screen.
        pygame.display.update()
        pygame.time.Clock().tick(15)


def game_loop(player, fps=10):
    """
    The functions loops through the game logic to display each frame of the game.
    """

    pygame.mixer.Sound.stop(background_music)

    # Reset the game settings
    game.restart_game()
    timer = 0
    which_turn = "right"

    # The game loop
    while not game.game_end():

        pygame.event.pump()
        
        # Play the Background music on repeat
        if timer == 0:
            pygame.mixer.Sound.set_volume(drift_sound,0.35)
            pygame.mixer.Sound.play(drift_sound)
            timer = 1000
        
        timer -=1
        
        # Play a sound whenever the player turns.
        if which_turn != train.facing:
            pygame.mixer.Sound.stop(turn_drift)
            which_turn = train.facing
            pygame.mixer.Sound.play(turn_drift)

        # Gets the input from the user to make the player move
        move = human_move()

        # The frequency at which the game screen updates
        fps = 6

        # Make the train move according to the input from the user
        game.do_move(move)

        # Add the screen background
        screen.fill(white)
        screen.blit(BackGround.image, BackGround.rect)

        # Display the train 
        game.train.blit(rect_len, screen)
        game.person.blit(screen)
        game.blit_score(white, screen)

        pygame.display.flip()

        fpsClock.tick(fps)

    crash()


def human_move():
    """
    Returns a number which corresponds to the direction in which the train should move.
    The keyboard inputs are taken to change the direction of the train.
    Th escape key is quits the game.
    """
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

    # Change the current working directory of the file
    os.chdir(base_path(''))

    # Start the game
    initial_interface()
