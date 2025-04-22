import random       #Generating random numbers
import sys          #sys.exit for terminating the program
import pygame
from pygame.locals import *

#Global variables:
FPS = 32
ScreenWidth = 289
ScreenHeight = 511
Screen = pygame.display.set_mode((ScreenWidth,ScreenHeight)) #Initializing the program window
GroundY= ScreenHeight*0.8 #Ground takes eighth of the total height
Game_Sprites={}
Game_Sounds={}
Player= 'Gallery/sprites/bird.png'
Background= 'Gallery/sprites/background.png'
Pipe= 'Gallery/sprites/pipe.png'
Message= 'Gallery/sprites/message.png'

def welcomeScreen():
    PlayerX= int(ScreenWidth/5)
    PlayerY= int((ScreenHeight - Game_Sprites['player'].get_height())/2)
    MessageX= int((ScreenWidth - Game_Sprites['message'].get_width())/2)
    MessageY= int(ScreenHeight*0.13)
    BaseX= 0
    while True:
        for event in pygame.event.get():
            #If user clicks cross button or presses esc, the game will close
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            #If user presses space or up arrow key, the game will start
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                Screen.blit(Game_Sprites['background'],(0,0))
                Screen.blit(Game_Sprites['player'],(PlayerX,PlayerY))
                Screen.blit(Game_Sprites['message'],(MessageX,MessageY))
                Screen.blit(Game_Sprites['base'],(BaseX,GroundY))
                pygame.display.update()
                FPSClock.tick(FPS)

def mainGame():
    score=0
    PlayerX= int(ScreenWidth/5)
    PlayerY= int((ScreenHeight - Game_Sprites['player'].get_height())/2)
    BaseX = 0

    newPipe1= getRandomPipe()
    newPipe2= getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': ScreenWidth+200, 'y':newPipe1[0]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': ScreenWidth+200, 'y':newPipe1[1]['y']},
        {'x': ScreenWidth+200+(ScreenWidth/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapVel= -8 #Velocity while flapping
    playerFlapped= False #True only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if PlayerY > 0:
                    playerVelY = playerFlapVel
                    playerFlapped= True
                    Game_Sounds['flap'].play()

        crashTest= isCollide(PlayerX, PlayerY, upperPipes, lowerPipes)
        if crashTest: return

        #check for score
        playerMidPos = PlayerX + Game_Sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + Game_Sprites['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                Game_Sounds['point'].play()

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = Game_Sprites['player'].get_height()
        PlayerY = PlayerY + min(playerVelY, GroundY - PlayerY - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -Game_Sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

         # Lets blit our sprites now
        Screen.blit(Game_Sprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            Screen.blit(Game_Sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            Screen.blit(Game_Sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        Screen.blit(Game_Sprites['base'], (BaseX, GroundY))
        Screen.blit(Game_Sprites['player'], (PlayerX, PlayerY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += Game_Sprites['numbers'][digit].get_width()
        Xoffset = (ScreenWidth - width)/2

        for digit in myDigits:
            Screen.blit(Game_Sprites['numbers'][digit], (Xoffset, ScreenHeight*0.12))
            Xoffset += Game_Sprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSClock.tick(FPS)
        
def isCollide(PlayerX, PlayerY, upperPipes, lowerPipes):
    if PlayerY> GroundY - 25  or PlayerY<0:
        Game_Sounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = Game_Sprites['pipe'][0].get_height()
        if(PlayerY < pipeHeight + pipe['y'] and abs(PlayerX - pipe['x']) < Game_Sprites['pipe'][0].get_width()):
            Game_Sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (PlayerY + Game_Sprites['player'].get_height() > pipe['y']) and abs(PlayerX - pipe['x']) < Game_Sprites['pipe'][0].get_width():
            Game_Sounds['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = Game_Sprites['pipe'][0].get_height()
    offset = ScreenHeight/3
    y2 = offset + random.randrange(0, int(ScreenHeight - Game_Sprites['base'].get_height() - 1.2 *offset))
    pipeX = ScreenWidth + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSClock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    Game_Sprites['numbers']=(
        pygame.image.load('Gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('Gallery/sprites/9.png').convert_alpha()
    )
    Game_Sprites['base']= pygame.image.load('Gallery/sprites/floor-sprite.png').convert_alpha()
    Game_Sprites['message']= pygame.image.load('Gallery/sprites/message.png').convert_alpha()
    Game_Sprites['background']= pygame.image.load(Background).convert()
    Game_Sprites['player']= pygame.image.load(Player).convert_alpha()
    Game_Sprites['pipe']=(pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(),180),
                          pygame.image.load(Pipe).convert_alpha())
    
    Game_Sounds['die'] = pygame.mixer.Sound('Gallery/sounds/die.mp3')
    Game_Sounds['flap'] = pygame.mixer.Sound('Gallery/sounds/flap.mp3')
    Game_Sounds['hit'] = pygame.mixer.Sound('Gallery/sounds/hit.mp3')
    Game_Sounds['point'] = pygame.mixer.Sound('Gallery/sounds/point.mp3')
    Game_Sounds['swosh'] = pygame.mixer.Sound('Gallery/sounds/swosh.mp3')

    while True:
        welcomeScreen()
        mainGame()