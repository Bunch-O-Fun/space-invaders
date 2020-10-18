class Bullet:

    __position__ = [0,0] # bullet keeps track of its location via a 2D array (x,y)
    __speed__ = 0 # bullet's speed is a integer value

    def __init__(self, x, y, speed): # initializer for the bullet, allowing specification of its starting location and its speed
        self.__position__[0]= x
        self.__position__[1] = y
        self.__speed__ = speed

    def setSpeed(self, speed): # sets the speed of the bullet, if needed
        self.__speed__ = speed
    def getSpeed(self): # returns the speed of the bullet
        return self.__speed__

    def setPosition(self, x, y): # sets the x and y coordinates of the bullet
        self.__position__[0] = x
        self.__position__[1] = y
    def getPosition(self): # returns the 2D array of the bullet's coordinates
        return self.__position__

    def setX(self, x): # sets only the x coordinate of the bullet
        self.__position__[x] = x
    def getX(self): # returns only the x coordinate of the bullet as an integer
        return self.__position__[0]

    def setY(self, y): # sets only the y coordinate of the bullet
        self.__position__[1] = y
    def getY(self): # returns only the y coordinate of the bullet as an integer
        return self.__position__[1]