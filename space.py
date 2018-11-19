from random import *
from time import *
from graphics import *
from math import *

# Global variables

# Height of the window.
screenHeight = 900
# Width of the window.
screenWidth = 1500

win = GraphWin("Space", screenWidth, screenHeight)
win.setBackground(color_rgb(10,10,10))
win.autoflush = False

def add(v1,v2):
    return [v1[0]+v2[0],v1[1]-v2[1]]

def sub(v1,v2):
    return [v1[0]-v2[0],v1[1]-v2[1]]

def mult(v1,mult):
    return [v1[0]*mult,v1[1]*mult]

def div(v1,div):
    return [v1[0]/div,v1[1]/div]

def dist(v1,v2):
    return sqrt((v1[0]-v2[0])**2+(v1[1]-v2[1])**2)

def normalize(vector):
    deg = 0
    if vector[0] >= 0 and vector[1] < 0:
        deg = atan(vector[0]/-vector[1])
    if vector[0] > 0 and vector[1] >= 0:
        deg = atan(-vector[1]/-vector[0])+radians(90)
    if vector[0] <= 0 and vector[1] > 0:
        deg = atan(vector[0]/-vector[1])+radians(180)
    if vector[0] < 0 and vector[1] <= 0:
        deg = atan(-vector[1]/-vector[0])+radians(270)
    return [sin(deg),-cos(deg)]

def angle(vector):
    deg = 0
    if vector[0] >= 0 and vector[1] < 0:
        deg = atan(vector[0]/-vector[1])
    if vector[0] > 0 and vector[1] >= 0:
        deg = atan(-vector[1]/-vector[0])+radians(90)
    if vector[0] <= 0 and vectorf[1] > 0:
        deg = atan(vector[0]/-vector[1])+radians(180)
    if vector[0] < 0 and vector[1] <= 0:
        deg = atan(-vector[1]/-vector[0])+radians(270)
    return deg

class SpaceObject:
    def __init__(self, pos, vel, mass=1):
        self.pos = pos
        self.vel = vel
        self.acc = [0,0]
        self.mass = mass

    def update(self):
        self.pos.add(self.vel)
        self.vel.add(self.acc)
        self.acc.mult(0)

    def force(self,force):
        f = force
        f.div(self.mass)
        self.acc.add(f)

class Ship(SpaceObject):
    def __init__(self, pos, vel, mass=5):
        super().__init__(pos, vel, mass)

    def update(self):
        super().update()

    def force(self, force):
        super().force(force)

while True:
    pass
