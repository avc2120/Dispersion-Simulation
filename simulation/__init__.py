import robot, world
import thread
import time
import Image
from Tkinter import Tk
from math import *


ROBOT_INDEX = 0

class simulation:
    ROBOTS = []
    ROOT = None
    CONTINUE = True
    WORLD = None

    def __init__(self):
        root = Tk()
        self.WORLD = world.COORDS(root)
        self.ROOT = root
        thread.start_new_thread(self.run, ())
        self.WORLD.mainCanvas.after(100, self.update_gui)
    
    def run(self):
        last_update = time.time()
        while self.CONTINUE:
            update_time = time.time()
            dTime = update_time - last_update
            last_update = update_time
            for bot in self.ROBOTS:
                bot.update(dTime)
            time.sleep(max(0, 0.01 + time.time() - update_time)) ##update 100 times a second

    def update_gui(self):
        for r in self.ROBOTS:
            self.WORLD.moveRobot(r)
        self.WORLD.mainCanvas.after(100, self.update_gui)

    def requestRobot(self, start_loc):
        r = robot.robot(start_loc, self.WORLD)
        r.GUI_LAST_LOC = start_loc
        r.ID = self.WORLD.mainCanvas.create_oval(start_loc[0] - 12, start_loc[1] + 12, start_loc[0] + 12, start_loc[1] - 12, fill = 'blue')
        LR = start_loc[2] + pi/2
        RR = start_loc[2] - pi/2
        r.IDL = self.WORLD.mainCanvas.create_line(start_loc[0] + 8*cos(LR), start_loc[1] + 8*sin(LR), start_loc[0], start_loc[1])
        r.IDR = self.WORLD.mainCanvas.create_line(start_loc[0] + 8*cos(RR), start_loc[1] + 8*sin(RR), start_loc[0], start_loc[1])
        self.ROBOTS.append(r)
        return r


 
