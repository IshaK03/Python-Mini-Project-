import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

pygame.init()
pygame.font.init()

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/panda.png'
BACKGROUND = 'gallery/sprites/background.png'
BAMBOO = 'gallery/sprites/bamboo.png'
ROCK= 'gallery/sprites/rock.png'
FIRE = 'gallery/sprites/fire.png'
DUMPLINGS = 'gallery/sprites/dumplings.png'
score=0

