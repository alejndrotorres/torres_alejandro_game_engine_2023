# This file was created by: Alejandro Torres
#  Content from Chris Bradfield; Kids Can Code
# KidsCanCode - Game Development with Pygame video series
# Video link: https://youtu.be/OmlQ0XCvIn0 

# game settings 
WIDTH = 800 #width of screen
HEIGHT = 600 #height of screen
FPS = 30

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5 
global PLAYER_FRIC
PLAYER_FRIC = 0.2

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)

GROUND = (0, HEIGHT - 40, WIDTH, 40, "normal") #position of ground
PLATFORM_LIST = [ #position of platforms and its quantities: WIDTH, HEIGHT, moving/still
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20,"moving"),
                 (125, HEIGHT - 350, 100, 20, "moving"),
                 (222, 200, 100, 20, "moving"),
                 (175, 100, 50, 20, "moving")] 