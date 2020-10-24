import pygame
import sys
import math
import time

class Display:

    def __init__ (self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((1280,981))
        self.screen = screen
        global background
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))

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
        if key_press[pygame.K_RIGHT]: #if right key is pressed, move 15 pixels right
            if x <= 1195:
                x += 15
        return x

    def player_action(self,x,y):
        self.x = x
        self.y = y
        playerimg = pygame.Rect(x,y,30,30) #reestablish the rectangle with the next x coordinate
        screen.blit(background,(0,0)) #redraws the background
        pygame.draw.rect(screen,(52,223,42),playerimg,0) #redraws the square with its new position
        pygame.display.flip() #updates the screen with all changes

    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Bullet:

    __position__ = [0,0] # bullet keeps track of its location via a 2 element array (x,y)

    def __init__(self, x, y): # initializer for the bullet, allowing specification of its starting location and its speed
        self.__position__[0]= x
        self.__position__[1] = y

    def setPosition(self, x, y): # sets the x and y coordinates of the bullet
        self.__position__[0] = x
        self.__position__[1] = y
    def getPosition(self): # returns the 2D array of the bullet's coordinates
        return self.__position__

    def bullet_action(self,x,y):
        self.__position__[0] = x
        self.__position__[1] = y
        for i in range(455):
            bulletimg = pygame.Rect(x,y-(2*i),5,10) #reestablish the rectangle with the next x coordinate
            screen.blit(background,(0,0)) #redraws the background
            pygame.draw.rect(screen,(255,0,0),bulletimg,0) #redraws the square with its new position
            pygame.display.flip() #updates the screen with all changes
            time.sleep(.0001)

mygame = Display()
x = 640
y = 890
playership = Player(x,y)
running = True
while running:
    pygame.display.flip() #updates the visuals on the screen
    pygame.display.update()
    pygame.time.delay(10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            x = playership.movement(x) #GETS NEW X VALUE
            playership.player_action(x,y) #reads what button you press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_x = playership.getX()
                start_y = playership.getY()
                bullet = Bullet(start_x,start_y)
                bullet.bullet_action(start_x,start_y)
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()
pygame.quit()
