import pygame
import sys
import math
import random

class Display:

    '''
    Display Constructor
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: creates a valid screen
    '''
    def __init__ (self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((1280,981))
        self.screen = screen
        global background
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))


    '''
    Parameters: N/A
    Returns: N/A
    Preconditions: Aliens must have reached a certain threshold on the screen for this to be called
    Postconditions: Displays "Game Over" on screen
    '''
    def gameOver(self):
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(text, (400, 250))

class Player:

    def __init__(self,xpos,ypos):
        self.x = x
        self.y = y
        GREEN = (54,223,42)
        global playerimg
        playerimg = pygame.Rect(x,y,30,30)
        pygame.draw.rect(screen,GREEN,playerimg,0) #current player is a square, add graphics later on

    def movement(self,x): # this function actually lets me change the value of x so the blits don't reset the player to the intial position
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_LEFT]: #if left key is pressed, move 15 pixels left
            if x >= 85:
                x -= 15
            print("left")
        if key_press[pygame.K_RIGHT]: #if right key is pressed, move 15 pixels right
            if x <= 1195:
                x += 15
            print("right")
        return x

    def player_action(self,x,y):
        self.x = x
        self.y = y
        playerimg = pygame.Rect(x,y,30,30) #reestablish the rectangle with the next x coordinate
        screen.blit(background,(0,0)) #redraws the background
        pygame.draw.rect(screen,(52,223,42),playerimg,0) #redraws the square with its new position
        pygame.display.flip() #updates the screen with all changes


class Alien:

    '''
    Alien Constructor
    Parameters: N/A
    Returns: N/A
    Preconditions: N/A
    Postconditions: creates multiple lists of aliens including their location and image
    '''

    def __init__ (self):
        self.alienX = []
        self.alienY = []
        self.alienNewX = []
        self.alienNewY = []
        self.alienImage = []
        self.numAliens = 5

        for i in range(self.numAliens):
            self.alienX.append(random.randint(0, 800))
            self.alienY.append(random.randint(0, 100))
            self.alienNewX.append(3)
            self.alienNewY.append(50)
            self.alienImage.append(pygame.image.load('alien.png'))



#display
mygame = Display()

#player
x = 640
y = 890
playership = Player(x,y)

#alien
alienShip = Alien()

running = True
while running:
    pygame.display.flip() #updates the visuals on the screen
    pygame.display.update()
    pygame.time.delay(10)

    screen.blit(background,(0,0))


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            x = playership.movement(x) #GETS NEW X VALUE
            playership.player_action(x,y) #reads what button you press
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()


    for i in range(5):

        #when aliens reach bottom of screen
        if (alienShip.alienY[i] > 800):
            mygame.gameOver()
            break

        #when aliens reach left part of screen they jump down a few and change directions
        alienShip.alienX[i] += alienShip.alienNewX[i]
        if (alienShip.alienX[i] <= 85):
            alienShip.alienNewX[i] = 3;
            alienShip.alienY[i] += alienShip.alienNewY[i]

        #when aliens reach right part of screen they jump down a few and change directions
        elif (alienShip.alienX[i] >= 1195):
            alienShip.alienNewX[i] = -3;
            alienShip.alienY[i] += alienShip.alienNewY[i]

        #displays alien
        screen.blit(alienShip.alienImage[i], (alienShip.alienX[i], alienShip.alienY[i]))


pygame.quit()




























#spce
