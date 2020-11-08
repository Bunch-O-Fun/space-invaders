from game import Player
from game import Alien
from game import Bullet
from game import moveBullets
from game import moveAliens
from game import checkHit
from game import levelUP
from game import checkEnd
from game import moveBullets

import pygame

print("*****TESTING PLAYER FEATURES*****")
testPlayer = Player(400,400)
print("Passed Creation Test: " + str(testPlayer.x == 400 and testPlayer.y == 400 and testPlayer.direction == 0))
testPlayer.direction = 1
testPlayer.move()
print("Passed Movement Test: " + str(testPlayer.x == 405))
testPlayer.x = 1290 - 85
testPlayer.move()
print("Passed Edge Test: " + str(testPlayer.x == 1290 - 85))

print("\n*****TESTING ALIEN FEATURES*****")
testAlien = Alien(400,400)
print("Passed Creation Test: " + str(testAlien.x == 400 and testAlien.y == 400 and testAlien.direction == 1))
testAlien.direction = 2
testAlien.move()
print("Passed Movement Test: " + str(testAlien.y == 410))

print("\n*****TESTING BULLET FEATURES*****")
testBullet = Bullet(400,400)
print("Passed Creation Test: " + str(testBullet.x == 400 and testBullet.y == 400))
testBullet.move()
print("Passed Movement Test: " + str(testBullet.y == 390))

print("\n*****TESTING DEALLOCATING FEATURES*****")
arrayBullet = [Bullet(100,-20)]
moveBullets(arrayBullet)
print("Passed Bullet Leave Screen Test: " + str(len(arrayBullet) == 0))

score = 0
pygame.init()
arrayBullet = [Bullet(100,100)]
arrayAlien = [Alien(100,100)]
checkHit(arrayBullet, arrayAlien)
print("Passed Bullet Hit Alien Test: " + str(len(arrayBullet) == 0 and len(arrayAlien) == 0))

print("\n*****TESTING MASS MOVEMENT FEATURES*****")
for i in range(6):
    arrayAlien += [Alien(100,100)]
moveAliens(arrayAlien)
passed = True
for alien in arrayAlien:
    if(alien.x != 110):
        passed = False;
print("Passed Mass Move Alien Test: " + str(passed))
for i in range(6):
    arrayBullet += [Bullet(100,100)]
moveBullets(arrayBullet)
passed = True
for bullet in arrayBullet:
    if(bullet.y != 90):
        passed = False;
print("Passed Mass Move Bullet Test: " + str(passed))

print("\n*****TESTING GAMEPLAY FEATURES*****")
aliens1 = [[],[],[]]
aliens2 = [[],[Alien(0, 0)],[]]
running = True
checkEnd(aliens1)
print(running)
