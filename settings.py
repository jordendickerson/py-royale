# Game Settings
import random
import pygame as pg
import os

#set directories
game_Folder = os.path.dirname(__file__)
assets_Folder = os.path.join(game_Folder, "assets")
img_Folder = os.path.join(assets_Folder, "imgs")
audio_Folder = os.path.join(assets_Folder, "audio")

font_name = pg.font.match_font('Impact')

print(img_Folder)

#High score file
HS_FILE = "highscore.txt"

#Spritesheet file
SPRITESHEET = "spritesheet_jumper.png"


# game title
TITLE = "Runner" #Sets title
FONT_NAME = 'arial'

# screen size
WIDTH = 450 #sets width of screen
HEIGHT = 800 #sets height of screen

#Troop settings
TROOP_SIZE = 25
TROOP_SPEED = .45
TROOP_HP = 100
TROOP_DAMAGE = 25
AVOID_RADIUS = 20

#King tower settings
KING_SIZE = 75
KING_HP = 1000

#Archer Tower Settings
ARCHER_SIZE = 75
ARCHER_HP = 500


#Arrow settings
ARROW_SPEED = 4
ARROW_DAMAGE = 15

#player properties
PLAYER_ACC = 1
PLAYER_FRICTION = -.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game Properties


# clock speed
FPS = 60 #sets frames per second (clock tick)

# difficulty
diff = "Normal" #sets difficulty


# Colors (R,G,B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BROWN = (255,200,100)
GREEN = (0, 255 ,0)
BLUE = (0, 0 ,255)
YELLOW = (255, 255, 0)
skyBlue = (135,206,235)
darkBlue = (86, 105, 184)
cfBlue = (100, 149, 237)