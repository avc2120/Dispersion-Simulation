import random, Image
from math import *

BACKSET = 6
SIDESET = 1
DxNoise = .5
DtNoise = .5
FOV = pi/3
X_RES = 256
size_x = 1212
size_y = 276
BATTERY_START = 10000

class robot:
    WORLD = None
    Dx = 0  #forward speed
    Dt = 0  #turning speed -->left
    Px = 0  #location size_x
    Py = 0  #location size_y
    Pt = 0  #current orintation

    def __init__(self, posTuple, inWorld):
        global size_x, size_y
        self.Batt = BATTERY_START + random.gauss(0, 250)
        self.Px = posTuple[0]
        self.Py = posTuple[1]
        self.Pt = posTuple[2]
        self.WORLD = inWorld
        try:
            size_x = inWorld.width
            size_y = inWorld.height
        except Exception, e:
            pass

    def resetBatt(self):
        self.Batt = BATTERY_START + random.gauss(0, 250)

    def getSensorLoc(self):
        (x, y, theta) = self.getLoc()
#        print x, y, theta
        px = x + BACKSET*cos(theta + pi)
        py = y - BACKSET*sin(theta + pi)

        px1 = min(size_x, max(0, int(px + SIDESET*cos(theta + pi/2))))
        py1 = min(size_y, max(0, int(py + SIDESET*sin(theta + pi/2))))

        px2 = min(size_x, max(0, int(px - SIDESET*cos(theta + pi/2))))
        py2 = min(size_y, max(0, int(py - SIDESET*sin(theta + pi/2))))

        px1 = min(max(0, px1), size_x-1)
        py1 = min(max(0, py1), size_y-1)

        px2 = min(max(0, px2), size_x-1)
        py2 = min(max(0, py2), size_y-1)
        return px2, py2, px1, py1

    def getLines(self):
        px2, py2, px1, py1 = self.getSensorLoc()
        return self.WORLD.lineStatus(px2, py2, px1, py1)

    def getSign(self):
        px2, py2, px1, py1 = self.getSensorLoc()
        return self.WORLD.getColor(px2, py2, px1, py1)

    def dropBeacon(self, explored):
        xL = self.getSensorLoc()[0]
        yL = self.getSensorLoc()[1]
        self.WORLD.dropBeacon(xL, yL, explored)
    
    def markExplored(self):
        xL = self.getSensorLoc()[0]
        yL = self.getSensorLoc()[1]
        self.WORLD.markExplored(xL, yL)

    def getBattery(self):
        if self.Batt < 0:
            return 6.2 - (self.Batt*self.Batt)/100
        return 7.0

    def move(self, Dx, Dt):
        self.Dx = Dx
        self.Dt = Dt
    
    def getLoc(self):
        return (self.Px, self.Py, self.Pt)

    def update(self, timeElasped):
        if self.Dx == 0 and self.Dt == 0:
            self.Batt -= 0.1*timeElasped
            return
        v = self.Dx + random.gauss(0, DxNoise)
        dt = self.Dt + random.gauss(0, DtNoise)
        pt = self.Pt
        t = timeElasped
        self.Batt = self.Batt - abs(v*t)
        if dt == 0:
            self.Px = self.Px + v*cos(pt)*t
            self.Py = self.Py - v*sin(pt)*t
        else:
            self.Px = self.Px + v*(sin(pt + dt*t) - sin(pt))/dt
            self.Py = self.Py - v*(-cos(pt + dt*t) + cos(pt))/dt
            self.Pt = normalize(self.Pt + t*dt)

    def getBlob(self, pColor):
        loc = self.getLoc()
        pX = loc[0]
        pY = loc[1]
        maxRay = loc[2] + FOV/2 # Start at the left side of the image
        x_adv = 0
        y_adv = 0
        count = 0
        for i in range(X_RES):
            ray = maxRay - (FOV/X_RES)*i
            min_dist = 1000
            minColor = 'none'
            if minColor == pColor:
                x_adv += i
                count += 192
        if count == 0:
            return (0, 0, 0)
        return (count, x_adv*192/count, 0)

def checkInterceptDist(line, point):
    (x1, y1, x2, y2) = line
    (pX, pY, pT) = point
    m = float(y1 - y2)/float(x1 - x2)
    pT = normalize(pT)
    tanR = tan(pT)
    if m == tanR:
        return 0.0001
    y = ((pX - x1)*(tanR*m) + y1*tanR - pY*m)/(tanR - m) #Y value of the point of intersection
    x = (y - y1)/m + x1                                  #X value of the point of intersection
    if (pT > 0 and pT < pi and y < pY):
        # Intercetction is below origin, and should be above
        return -1
    if (pT > pi and pT < 2*pi and y > pY):
        # Intercection is above origin and should be below
        return -1
    if (min(y1, y) == max(y2, y) or min(y2, y) == max(y1, y)):
        return sqrt((x - pX)**2 + (y - pY)**2)
    return -1

def normalize(n):
    if n < 2*pi and n >= 0:
        return n
    elif n >= 2*pi:
        return normalize(n - 2*pi)
    else:
        return normalize(n + 2*pi)





