import pygame
import sys
import math
import time

SCREEN_HEIGHT = 981
SCREEN_WIDTH = 1290
RIGHT_BORDER = SCREEN_WIDTH - 85
LEFT_BORDER = 85

ALIEN_SPEED = 10
BULLET_SPEED = 10
PLAYER_SPEED = 5 

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
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        self.x = xpos
        self.y = ypos
       
        self.direction = 0
        self.hitbox = pygame.Rect(self.x,self.y,30,30)
        #current player is a square, add graphics later on
    
    def move(self):
        if (self.x + self.direction * PLAYER_SPEED > LEFT_BORDER) and (self.x + self.direction * PLAYER_SPEED < RIGHT_BORDER):
            self.x = self.x + self.direction * PLAYER_SPEED

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
        if(abs(self.direction) != 2):
            self.x = self.x + self.direction * ALIEN_SPEED
        else:
            self.y += ALIEN_SPEED



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
        self.y -= BULLET_SPEED

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
                bullets += [Bullet(playership.x + 12, playership.y)]
                        
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

def moveAliens(aliens):
    if(len(aliens) != 0):
        if(aliens[len(aliens) - 1].x >= RIGHT_BORDER and aliens[len(aliens) - 1].direction == 1):
            for alien in aliens:
                alien.direction = 2
        elif(aliens[0].x <= LEFT_BORDER and aliens[0].direction == -1):
            for alien in aliens:
                alien.direction = -2
        elif(aliens[0].direction == 2):
            if(aliens[0].y > aliens[0].yold + 40):
                for alien in aliens:
                    alien.direction = -1
                    alien.yold = alien.y
        elif(aliens[0].direction == -2):
            if(aliens[0].y > aliens[0].yold + 40):
                for alien in aliens:
                    alien.direction = 1
                    alien.yold = alien.y
    for alien in aliens:
        alien.move()
        if(alien.y > SCREEN_HEIGHT):
            running = False

def checkHit(bullets, aliens):
    for alien in aliens:
        for bullet in bullets:
            if(alien.hitbox.colliderect(bullet.hitbox)):
                aliens.remove(alien)
                bullets.remove(bullet)

def levelUP(): #Goes to next level if player kills all aliens on current level
    global level, ALIEN_SPEED
    next_level = True
    for row_aliens in aliens:
        if len(row_aliens) != 0:
            next_level = False
    
    if(next_level):
        level += 1
        if(level % 3 == 0):
            ALIEN_SPEED += 2
        for i in range(level % 3 + 1):
            for j in range(15):
                aliens[i] += [Alien(100 + j * 60, 40 + 40 * i, 35, 20)]
    return level

def checkEnd(aliens):
    global running
    for row_aliens in aliens:
        for alien in row_aliens:
            if(alien.y > SCREEN_HEIGHT):
                running = False

def gameLogic(playership, bullets, aliens):
    getUserInput(playership, bullets)
    playership.move() #moves player in direction, self.direction updated in playerInput
    moveBullets(bullets)
    moveAliens(aliens[0])
    moveAliens(aliens[1])
    moveAliens(aliens[2])
    checkHit(bullets, aliens[0])
    checkHit(bullets, aliens[1])
    checkHit(bullets, aliens[2])
    levelUP()
    checkEnd(aliens)
    
    
    
def render(playership, bullets, aliens):
    screen.blit(background,(0,0))
    playership.render()
    for bullet in bullets:
        bullet.render()
    for alien_row in aliens:
        for alien in alien_row:
            alien.render()
     #updates the visuals on the screen
    #pygame.display.update()


mygame = Display()
x = 640
y = 890
playership = Player(x,y)
bullets = []
aliens = [[],[],[]]
level = 0 
for i in range(15):
    aliens[0] += [Alien(100 + i * 60, 40, 35, 20)]
running = True
while running:
    time_start = pygame.time.get_ticks()

    render(playership, bullets, aliens)
    gameLogic(playership, bullets, aliens)
    
    time_end = pygame.time.get_ticks()
    if(time_end - time_start < 17):
        pygame.time.delay(17 - (time_end - time_start))
    pygame.display.flip()

exit_game = False
mygame.gameOver()
pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False #breaks out of loop and quits the game
            sys.exit()

 



























#spce
