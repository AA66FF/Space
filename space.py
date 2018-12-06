from random import *
from time import *
from graphics import *
from math import *
from tkinter import *

# Global variables

# Height of the window.
screenHeight = 600
# Width of the window.
screenWidth = 600
# Whether the window is open or not
open = True
# Frames per second.
fps = 60
runFps = 0
# Movement is multiplied by this value so that lag does not affect the speed of
# the game.
timeDilation = 1
# Drag... in space
drag = 0.01

win = GraphWin("Space", screenWidth, screenHeight)
win.setBackground(color_rgb(0,0,0))
win.autoflush = False

keysPressed = []

def down(e):
    global keysPressed
    if (len(keysPressed) == 0):
        keysPressed.append(e.char)
    else:
        notIn = True
        for i in range(len(keysPressed)-1, -1, -1):
            if e.char == keysPressed[i]:
                notIn = False
        if notIn == True:
            keysPressed.append(e.char)


def up(e):
    global keysPressed
    for i in range(len(keysPressed)-1, -1, -1):
        if e.char == keysPressed[i]:
            del keysPressed[i]

win.master.bind_all('<KeyPress>', down)
win.master.bind_all('<KeyRelease>', up)

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

def inside(pos,rectPos1,rectPos2):
    if (pos[0] > rectPos1[0] and pos[0] < rectPos2[0] and pos[1] > rectPos1[1]\
    and pos[1] < rectPos2[1]):
        return True
    else:
        return False

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
        self.pos = add(self.pos,div(self.vel,timeDilation))
        self.vel = add(self.vel,div(self.acc,timeDilation))
        self.acc = mult(self.acc,0)
        self.vel = mult(self.vel,1-drag/timeDilation)

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

class Asteroid(SpaceObject):
    def __init__(self, pos, vel=[0,0], mass=100):
        super().__init__(pos, vel, mass)
        self.img = Point(0,0)
        self.radius = sqrt(self.mass)*2
        self.hp = 10
        self.draw()

    def update(self):
        super().update()

    def force(self):
        super().force()

    def draw(self):
        self.img.undraw()
        self.img = Circle(vecToPt(sub(self.pos,c.cpos())),self.radius)
        self.img.setFill("#666666")
        self.img.setOutline("#999999")
        self.img.draw(win)

    def onScreen(self):
        posOnCam = sub(self.pos,c.cpos())
        if (posOnCam[0] > -40 and posOnCam[0] < screenWidth+40 and posOnCam[1]\
        > -40 and posOnCam[1] < screenHeight+40):
            return True
        else:
            return False

lasers = []

class Laser(SpaceObject):
    def __init__(self, pos, vel=[0,0], angle=0, mass=1):
        super().__init__(pos, vel, mass)
        self.laser = Point(0,0)
        self.team = 0
        self.angle = angle
        self.lifetime = 200

    def update(self):
        self.pos = add(self.pos,div(self.vel,timeDilation))
        self.vel = add(self.vel,div(self.acc,timeDilation))
        self.acc = mult(self.acc,0)
        self.lifetime -= 1/timeDilation

    def force(self):
        super().force()

    def draw(self):
        self.laser.undraw()
        laserPoints = []
        laserPoints.append([0,-4])
        laserPoints.append([0,4])
        for i in range(len(laserPoints)):
            laserPoints[i] = rotate(laserPoints[i],self.angle)
            laserPoints[i] = add(self.pos,laserPoints[i])
            laserPoints[i] = sub(laserPoints[i],c.cpos())
            laserPoints[i] = vecToPt(laserPoints[i])
        self.laser = Polygon(laserPoints)
        self.laser.setFill(color_rgb(0,0,0))
        if self.team == 0:
            self.laser.setOutline(color_rgb(0,255,0))
        self.laser.draw(win)

    def collide(self, asteroid):
        if inside(add(self.pos,self.vel),\
        add(asteroid.pos,[-asteroid.radius,-asteroid.radius]),\
        add(asteroid.pos,[asteroid.radius,asteroid.radius])):
            self.lifetime = -1

class Ship(SpaceObject):
    def __init__(self, pos, vel=[0,0], angle=0, mass=5):
        super().__init__(pos, vel, mass)
        self.mHp = 10
        self.hp = self.mHp
        self.angle = angle
        self.angVel = 0
        self.topSpeed = 1

    def update(self):
        super().update()
        self.angle += self.angVel/timeDilation
        self.angVel *= 1-0.1/timeDilation
        if mag(self.vel) > self.topSpeed:
            self.vel = normalize(self.vel)
            self.vel = mult(self.vel,self.topSpeed)

    def force(self, force):
        super().force(force)

class Player(Ship):
    def __init__(self, pos, vel=[0,0], angle=0, mass=5, team=0):
        super().__init__(pos, vel, angle, mass)
        self.shipImg = Point(0,0)
        self.draw()
        self.topSpeed = 4/timeDilation
        self.fireCooldown = 0
        self.fireRate = 10

    def update(self):
        super().update()
        self.fireCooldown -= 1/timeDilation

    def force(self, force):
        super().force(force)

    def draw(self):
        self.shipImg.undraw()
        self.shipPoints = []
        self.shipPoints.append([0,2])
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
        keys = keysPressed
        for i in range(len(keys)):
            if keys[i] == "w":
                self.force(rotate([0,-0.5],self.angle))
            if keys[i] == "a":
                self.angVel -= 0.01/timeDilation
            if keys[i] == "s":
                self.force(rotate([0,0.5],self.angle))
            if keys[i] == "d":
                self.angVel += 0.01/timeDilation
            if keys[i] == " " and self.fireCooldown <= 0:
                laserVel = add(self.vel,mult(rotate([0,-1],self.angle),8))
                lasers.append(Laser(self.pos,laserVel,self.angle))
                self.fireCooldown = self.fireRate

    def collide(self, asteroid):
        if inside(add(self.pos,self.vel),\
        add(asteroid.pos,[-asteroid.radius,-asteroid.radius]),\
        add(asteroid.pos,[asteroid.radius,asteroid.radius])):
            self.vel = mult(self.vel,-1)
            self.pos = add(self.pos,self.vel)
            self.vel = [0,0]

player = Player(c.pos,[0,0],radians(0),10)

asteroids = []

for i in range(2000):
    pos = [randrange(-10000,10000),randrange(-10000,10000)];
    asteroids.append(Asteroid(pos))

t = time.time()
t2 = time.time()
frame = 0
runframe = 0
asteroidsOnScreen = []

while open:
    player.update()
    c.update()
    player.control()
    for i in range(len(asteroidsOnScreen)):
        player.collide(asteroidsOnScreen[i])
    c.pos = add(div(sub(player.pos,c.pos),20*timeDilation),c.pos)
    for i in range(len(lasers)-1, -1, -1):
        for j in range(len(asteroidsOnScreen)):
            lasers[i].collide(asteroidsOnScreen[j])
        lasers[i].update()
        lasers[i].draw()
        if lasers[i].lifetime <= 0:
            lasers[i].laser.undraw()
            del lasers[i]
    if (time.time() > t+1/fps):
        asteroidsOnScreen = []
        player.draw()
        for i in range(len(asteroids)):
            if asteroids[i].onScreen():
                asteroids[i].draw()
                asteroidsOnScreen.append(asteroids[i])
            else:
                asteroids[i].img.undraw()
        frame += 1
        t = time.time()
    if (time.time() > t2+0.1):
        runFps = runframe*10
        timeDilation = runFps/fps
        frame = 0
        runframe = 0
        t2 = time.time()
    runframe += 1
    win.update()
