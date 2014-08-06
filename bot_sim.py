import sys
import simulation
import time, os, datetime
from patrol_config import *
import patrol_config
from threading import Lock
import threading, thread
from math import sqrt, atan, tan, pi, degrees, sin, cos
import patrol

file1 = None
SIM = None
WORLD_X = 24.24      #606 inches
WORLD_Y = 2.76
SPEED = 18
WHEEL_BASE = 12
start_x = 100
start_y = 340

class bot(threading.Thread):
    PROX = None
    KILLED = False
    NAME = "Scribby"
    TOWER = 0
    THREAD_LOCK = None
    STATUS = None
    LOCATION = None
    LAPS = 0
    TOTALLAPS = 0
    ACTIVETIME = 0
    IDLETIME = 0
    STARTTIME = None
    ENDTIME = None
    RETURNTIME = 0
    BATTERY = 0
    ROBOT_DATA_FILE = None
    SCRIBBLER_FORWARD = True
    BLOB_HASH = 0
    
    def __init__(self, add = None, tower=0):
        global SIM, file1
        self.THREAD_LOCK = Lock()
        if file1 == None:
            self.ROBOT_DATA_FILE = patrol_config.LOG_PATH  + datetime.datetime.now().isoformat('_')
            self.open_file()
        if SIM == None:
            SIM = simulation.simulation()
        self.STATUS = "Idle"
        self.LOCATION = -1
        self.LAPS = 0
        self.TOWER = tower
        threading.Thread.__init__(self)

    def move(self, vl, vr):
        if self.PROX == None:
            self.PROX = SIM.requestRobot((start_x, start_y, -pi ))
        vl -= 100
        vr -= 100
        v = (vl + vr)/200.0*SPEED       # value[-1,1]*speed
        t = (vl - vr)/100.0*SPEED/WHEEL_BASE  #
        if self.SCRIBBLER_FORWARD:
            v =- v
#        print v, t
        self.PROX.move(v, t)

    def kill(self):
        self.KILLED = True

    def isDead(self):
        return self.KILLED

    def unKill(self):
        self.KILLED = False

    def stop(self):
        self.move(100,100)
        self.PROX.Dt = 0
        self.PROX.Dx = 0

    def forward(self, speed = 100, ptime = 0):
        if ptime != 0:
            self.move(100 + speed, 100 + speed)
            time.sleep(ptime)
            self.stop()
        self.move(100 + speed, 100 + speed)

    def getBatteryLevel(self):
	return self.PROX.getBattery()

    def backward(self, speed = 100, ptime = 0):
        if ptime != 0:
            self.move(100 - speed, 100 - speed)
            time.sleep(ptime)
            self.stop()
        self.move(100 - speed, 100 - speed)

    def turnLeft(self, speed = 100, ptime = 0):
        if ptime != 0:                                                 
                self.move(100 + speed, 100)
                time.sleep(ptime)
                self.stop()
        self.move(100 + speed, 100)

    def turnRight(self):
        end_time = time.time() + 0.75
        while(time.time() < end_time):                                       
            self.move(50, 200)
        move_time = time.time() + 3
        while(time.time() < move_time):
            self.move(100,100)

    def spinLeft(self, speed = 100, ptime = 0):
        if ptime == 0:
            self.move(100 + speed, 100 - speed)
        else:
            self.spinLeft(speed)
            time.sleep(ptime)
            self.stop()

    def spinRight(self, speed = 100, ptime = 0):
        if ptime == 0:
            self.move(100 - speed, 100 + speed)
        else:
            self.spinRight(speed)
            time.sleep(ptime)
            self.stop()

    def setScribblerForward(self):
        self.SCRIBBLER_FORWARD = True
    
    def setFlukeForward(self):
        self.SCRIBBLER_FORWARD = False

    def detectBeacon(self):
        RGBleft, RGBright = self.getBothColors()
        if RGBleft == (0, 255, 0) or RGBright == (0,255,0):
            print 'intersection detected'
            return 0
        elif RGBleft == (255,100,0) or RGBright == (255,100,0):
            return 2
        elif RGBleft == (125, 125, 125) or RGBright == (125,125,125):
            return 1
        elif RGBleft == (0,0,255) or RGBright == (0,0,255):
            return 3
        else:
            return 4

    def jump(self):
        jump_speed = 200
        end_time = time.time() + 3
        while time.time() < end_time:
           self.move(jump_speed, jump_speed)

    def followEdge(self, out_speed, in_speed):
        lines = self.getBothLines()
        if lines != (None, None):
            (lline, rline) = (lines[0], lines[1])
            if not(lline) and not(rline): 
                self.move(out_speed, in_speed)
            elif lline and not(rline):           
                count = 0
                self.move(out_speed, out_speed)
                inside = True
            elif lline and rline:                
                count = 0
                self.move(in_speed, out_speed)
            elif not(lline) and rline:         
                count = 0
                self.move(out_speed, in_speed)
                inside = False
            else:
                print("?????")


    def getBothLines(self):
        time.sleep(.01)
        return self.PROX.getLines()

    def getBothColors(self):
        time.sleep(0.01)
        return self.PROX.getSign()

    def dropBeacon(self, explored):
        self.PROX.dropBeacon(explored)

    def markExplored(self):
        self.PROX.markExplored()

    def set_location (self, new):
        self.LOCATION = new

    def get_location (self):
        return self.LOCATION

    def set_activetime (self, new):
        self.ACTIVETIME = new

    def get_activetime (self):
        return self.ACTIVETIME
       
    def set_totallaps (self, new):
        self.TOTALLAPS = new
        
    def get_totallaps(self):
        return self.TOTALLAPS

    def set_idletime (self, new):
        self.IDLETIME = new

    def get_idletime (self):
        return self.IDLETIME
       
    def set_starttime(self, new):
        self.STARTTIME = new
        
    def get_starttime(self):
        return self.STARTTIME
    
    def set_endtime(self, new):
        self.ENDTIME = new
        
    def get_endtime(self):
        return self.ENDTIME
    
    def get_returntime(self):
        return self.RETURNTIME

    def set_returntime(self, in_time):
        self.RETURNTIME = in_time

    def get_all (self):
        return self.STATUS, self.LOCATION, self.LAPS, self.getBatteryLevel(), self.ACTIVETIME, self.IDLETIME

    def open_file (self):
        global file1
        if file1 == None:
            file1 = file(self.ROBOT_DATA_FILE + ".csv", "wb")
            file1.write("Names, Status, Location, Laps, Total Laps, Battery, Active Time, Idle Time, Return Time\n")

    def write_to_file (self):
        global file1
        file1.write("%s, %s, %d, %d, %d, %.2f, %s, %s, %s\n" % (self.NAME, self.STATUS, self.LOCATION, self.LAPS, self.TOTALLAPS, self.getBatteryLevel(), self.ACTIVETIME, self.IDLETIME, self.RETURNTIME))


############  Need to implemnt on own ######################

    def programScribbler(self, filename):
        pass
    def programFluke(self, filename):
        pass
    def close(self):
        pass
    def reconnect(self):
        self.PROX.resetBatt()


def radian_w(n):
    if n >= 2*pi:
        return radian_w(n - 2*pi)
    if n < 0:
        return radian_w(n + 2*pi)
    return n

def x_loc(dx, dy, theta):
    return 128 + 128/FOV(theta - atan(float(dy)/dx))

def atan2(o, a): #o = dy, a = dx
    if a > 0:
        return atan(float(o)/a)
    elif a < 0:
        return pi + atan(float(o)/a)
    elif o < 0:
        return 3*pi/2
    else:
        return pi/2
