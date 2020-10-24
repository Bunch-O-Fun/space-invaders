import pygame
import sys
import math
import time

Screen_Height = 981
Screen_Width = 1290
Right_Border = Screen_Width - 85
Left_Border = 85

class Display:

    def __init__ (self):
        pygame.init()
        global screen
        screen = pygame.display.set_mode((Screen_Width, Screen_Height))
        global background
        background = pygame.image.load('background.png')
        pygame.display.set_caption("Space Invaders!")
        screen.blit(background,(0,0))

class Player:

    def __init__(self,xpos,ypos):
        self.x = xpos
        self.y = ypos
       
        self.direction = 0
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        #current player is a square, add graphics later on
    
    def move(self):
        if (self.x + self.direction * 5 > Left_Border) and (self.x + self.direction * 5 < Right_Border):
            self.x = self.x + self.direction * 5

    def render(self):
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        pygame.draw.rect(screen,(54,223,42),self.hitbox,0)

class Alien:
    def __init__(self,xpos,ypos, xsize, ysize):
        self.x = xpos
        self.y = ypos
        self.yold = ypos
        self.direction = 1
        self.xsize = xsize
        self.ysize = ysize
        self.hitbox = pygame.Rect(self.x,self.y,self.xsize,self.ysize)
        #current player is a square, add graphics later on
    
    def move(self):
        if(self.direction != 2):
            self.x = self.x + self.direction * 3
        else:
            self.y += 3



    def render(self):
        self.hitbox = pygame.Rect(self.x,self.y,self.xsize,self.ysize)
        pygame.draw.rect(screen,(54,223,42),self.hitbox,0)

    def getX(self):
        return self.x
    def getY(self):
        return self.y

class Bullet:
    def __init__(self, x, y): # initializer for the bullet, allowing specification of its starting location and its speed
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x,self.y,5,10)

    def move(self):
        self.y -= 10

    def render(self): # this works :)
        self.hitbox = pygame.Rect(self.x,self.y,5,10)
        pygame.draw.rect(screen,(255,0,0),self.hitbox,0)

def moveBullets(bullets):
    for bullet in bullets:
        bullet.move()

    if len(bullets) > 0:
        if bullets[0].y < -10:
            bullets.remove(bullets[0])

def getUserInput(playership, bullets):
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playership.direction = -1
            if event.key == pygame.K_RIGHT:
                playership.direction = 1
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playership.direction = 0
            if event.key == pygame.K_RIGHT:
                playership.direction = 0
            
            if event.key == pygame.K_SPACE:
                start_x = playership.x
                start_y = playership.y
                bullets += [Bullet(playership.x, playership.y)]
                        
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

def moveAliens(aliens):
    if(len(aliens) != 0):
        if(aliens[len(aliens) - 1].x >= Right_Border and aliens[len(aliens) - 1].direction == 1):
            for alien in aliens:
                alien.direction = 2
        elif(aliens[0].x <= Left_Border and aliens[0].direction == -1):
            for alien in aliens:
                alien.direction = 2
        elif(aliens[len(aliens) - 1].x >= Right_Border and aliens[len(aliens) - 1].direction == 2):
            if(aliens[0].y > aliens[0].yold + 40):
                for alien in aliens:
                    alien.direction = -1
                    alien.yold = alien.y
        elif(aliens[0].x <= Left_Border and aliens[0].direction == 2):
            if(aliens[0].y > aliens[0].yold + 40):
                for alien in aliens:
                    alien.direction = 1
                    alien.yold = alien.y
    for alien in aliens:
        alien.move()

def checkHit(bullets, aliens): # sees if hitboxes overlap of aliens and bullets, if it does deletes that bullet and alien
    if(len(aliens) != 0):
        i = 0
        while(i < len(aliens)):
            j = 0
            while(j < len(bullets)):
                if(aliens[i].hitbox.colliderect(bullets[j].hitbox)):
                    aliens.remove(aliens[i])
                    bullets.remove(bullets[j])
                    i -= 1
                    j -= 1
                    break
                j += 1
            i += 1

#def simpleCheck(bullets, aliens): #doesnt work unforturnately
#    for alien in aliens:
#        for bullet in bullets:
#            if(alien.hitbox.colliderect(bullet.hitbox)):
#                aliens.remove(aliens)
#                bullets.remove(bullets)

def gameLogic(playership, bullets, aliens):
    getUserInput(playership, bullets)
    playership.move() #moves player in direction, self.direction updated in playerInput
    moveBullets(bullets)
    moveAliens(aliens)
    checkHit(bullets, aliens)
    #simpleCheck(bullets, aliens)
    
def render(playership, bullets, aliens):
    screen.blit(background,(0,0))
    playership.render()
    for bullet in bullets:
        bullet.render()
    for alien in aliens:
        alien.render()
    pygame.display.flip() #updates the visuals on the screen
    #pygame.display.update()

mygame = Display()
x = 640
y = 890
playership = Player(x,y)
bullets = []
aliens = []
for i in range(6):
    aliens += [Alien(100 + i * 45, 40, 35, 20)]
global running
running = True
while running:
    render(playership, bullets, aliens)
    gameLogic(playership, bullets, aliens)
    pygame.time.delay(10)
pygame.quit()
