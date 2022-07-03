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

if __name__ == "__main__":
    # This will be the main point from where our game will start
    FPSCLOCK = pygame.time.Clock()
    
    GAME_SPRITES['dumplings'] = pygame.image.load(DUMPLINGS).convert_alpha()
    icon = pygame.image.load('gallery/sprites/dumplings.png')
    pygame.display.set_icon(icon)
    
    pygame.display.set_caption('Dumpling Rush')
    
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] =pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['bamboo'] =(pygame.transform.rotate(pygame.image.load( BAMBOO).convert_alpha(), 180), 
    pygame.image.load(BAMBOO).convert_alpha())
    GAME_SPRITES['rock'] =(pygame.transform.rotate(pygame.image.load(ROCK).convert_alpha(), 180), 
    pygame.image.load(ROCK).convert_alpha())
    GAME_SPRITES['fire'] =(pygame.transform.rotate(pygame.image.load(FIRE).convert_alpha(), 180), 
    pygame.image.load(FIRE).convert_alpha())
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    
    # Game sounds
    GAME_SOUNDS['welcome1'] = pygame.mixer.Sound('gallery/audio/welcome1.mp3')
    GAME_SOUNDS['hit1'] = pygame.mixer.Sound('gallery/audio/hit1.mp3')
    GAME_SOUNDS['bgm1'] = pygame.mixer.Sound('gallery/audio/bgm1.mp3')
