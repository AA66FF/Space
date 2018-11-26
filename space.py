from random import *
from time import *
from graphics import *
from math import *

# Global variables

# Height of the window.
screenHeight = 600
# Width of the window.
screenWidth = 600
# Drag... in space
drag = 0.0006
# Whether the window is open or not
open = True

win = GraphWin("Space", screenWidth, screenHeight)
win.setBackground(color_rgb(0,0,0))
win.autoflush = False

def add(v1,v2):
    return [v1[0]+v2[0],v1[1]+v2[1]]

def sub(v1,v2):
    return [v1[0]-v2[0],v1[1]-v2[1]]

def mult(v1,mult):
    return [v1[0]*mult,v1[1]*mult]

def div(v1,div):
    return [v1[0]/div,v1[1]/div]

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def mag(vector):
    return sqrt(vector[0]**2+vector[1]**2)

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

def rotate(vector, angle):
    return [vector[0]*cos(angle)-vector[1]*sin(angle),vector[0]*sin(angle)\
    +vector[1]*cos(angle)]

def vecToPt(vector):
    return Point(vector[0],vector[1])

class SpaceObject:
    def __init__(self, pos, vel=[0,0], mass=1):
        self.pos = pos
        self.vel = vel
        self.acc = [0,0]
        self.mass = mass

    def update(self):
        self.pos = add(self.pos,self.vel)
        self.vel = add(self.vel,self.acc)
        self.acc = mult(self.acc,0)
        self.vel = mult(self.vel,1-drag)

    def force(self,force):
        f = force
        f = div(f,self.mass)
        self.acc = add(self.acc,f)

class Camera(SpaceObject):
    def __init__(self, pos, vel=[0,0], mass=10):
        super().__init__(pos, vel, mass)

    def update(self):
        super().update()

    def force(self, force):
        super().force(force)

    def cpos(self):
        return add(self.pos,[-300,-300])

c = Camera([0,0])

class Ship(SpaceObject):
    def __init__(self, pos, vel=[0,0], angle=0, mass=5):
        super().__init__(pos, vel, mass)
        self.mHp = 10;
        self.hp = self.mHp;
        self.angle = angle;
        self.topSpeed = 0.01;

    def update(self):
        super().update()
        if mag(self.vel) > self.topSpeed:
            self.vel = normalize(self.vel)
            self.vel = mult(self.vel,self.topSpeed)

    def force(self, force):
        super().force(force)

class Player(Ship):
    def __init__(self, pos, vel=[0,0], angle=0, mass=5):
        super().__init__(pos, vel, angle, mass)
        self.shipImg = Point(0,0)
        self.draw()
        self.topSpeed = 0.01;

    def update(self):
        super().update()

    def force(self, force):
        super().force(force)

    def draw(self):
        self.shipImg.undraw()
        self.shipPoints = []
        self.shipPoints.append([0,0])
        self.shipPoints.append([-6,8])
        self.shipPoints.append([0,-8])
        self.shipPoints.append([6,8])
        for i in range(len(self.shipPoints)):
            self.shipPoints[i] = rotate(self.shipPoints[i],self.angle)
            self.shipPoints[i] = add(self.pos,self.shipPoints[i])
            self.shipPoints[i] = sub(self.shipPoints[i],c.cpos())
            self.shipPoints[i] = vecToPt(self.shipPoints[i])
        self.shipImg = Polygon(self.shipPoints)
        self.shipImg.setFill(color_rgb(0,255,0))
        self.shipImg.setOutline(color_rgb(0,255,0))
        self.shipImg.draw(win)

    def control(self):
        print(_root.keysym)

bob = Player(c.pos,[0,0],radians(0),10)

while open:
    bob.control()
    bob.update()
    c.update()
    bob.force()
    bob.draw()
    print(bob.pos)
    print(c.cpos())
    c.force(div(sub(bob.pos,c.pos),1000000))
    win.flush()
