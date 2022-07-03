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

def welcomeScreen():
    """
    Shows welcome images on the screen
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                GAME_SOUNDS['welcome1'].stop()
                GAME_SOUNDS['bgm1'].play()
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))        
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                GAME_SOUNDS['welcome1'].play()
                GAME_SOUNDS['welcome1'].set_volume(0.5)
                FPSCLOCK.tick(FPS)
                
def getRandomObstacle():
    obstacles = ["bamboo","rock","fire"]
    obstacle = random.choice(obstacles)
    return obstacle

def getRandomPipe(choice):
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """

    pipeHeight = GAME_SPRITES[choice][0].get_height()
    offset = SCREENHEIGHT/3.2
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

def mainGame():
    
    global score
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    obs1=getRandomObstacle()
    obs2=getRandomObstacle()
    newPipe1 = getRandomPipe(obs1)
    newPipe2 = getRandomPipe(obs2)

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+300, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+300+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+300, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+300+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlyV = -8 # velocity while flying
    playerFly = False # It is true only when the bird is flying 
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlyV
                    playerFly = True
                   

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes,obs1, obs2) # This function will return true if the player is crashed
        if crashTest:       
            return show_score(textx, texty)
        
        
        #check for score
        
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES[getRandomObstacle()][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
        
        if playerVelY <playerMaxVelY and not playerFly:
            playerVelY += playerAccY

        if playerFly:
            playerFly = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
            
         # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe(getRandomObstacle())
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES[obs1][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES[obs2][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES[obs1][1], (lowerPipe['x'], lowerPipe['y']))    
            
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes, obs1, obs2):
    
    if playery<0:
        GAME_SOUNDS['bgm1'].stop()
        GAME_SOUNDS['hit1'].play()
        return True
    
    
    
            
            
            

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
    
    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
