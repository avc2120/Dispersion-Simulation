from Tkinter import *
import tkMessageBox, sys, os, threading, math, time, datetime
from PIL import Image
from math import *
from patrol import *
pic = Image.open('simulation/world.png')
im = pic.load()

R_OLD, G_OLD, B_OLD = (0, 0, 0)
R_NEW, G_NEW, B_NEW = (0, 174, 239)
class COORDS:
    def __init__(self, root):
        root.title("Simulation Setup")
        root.resizable(width=0, height=0)
        
        self.myParent = root
        self.height = 600
        self.width = 800

        self.mainCanvas = Canvas(self.myParent, height=self.height, width=self.width)
        self.mainCanvas.pack_propagate(0)
        self.mainCanvas.pack(side=TOP)

        line1 = self.mainCanvas.create_rectangle(80,80,720,85, fill='black') # top
        line2 = self.mainCanvas.create_rectangle(715,80,720,520, fill='black') # right
        line3 = self.mainCanvas.create_rectangle(80, 515, 720, 520, fill = 'black' ) #bottom
        line4 = self.mainCanvas.create_rectangle(80, 80, 85 , 270, fill = 'black') #top left
        line5 = self.mainCanvas.create_rectangle(80,340, 85, 520, fill = 'black') #bottom left
        line6 = self.mainCanvas.create_rectangle(80, 275, 150 ,270, fill = 'black' )#done
        line7 = self.mainCanvas.create_rectangle(210, 275, 450 ,270, fill = 'black' )#done
        line8 = self.mainCanvas.create_rectangle(445, 80, 450 ,145, fill = 'black' )#done1
        line8 = self.mainCanvas.create_rectangle(445, 205, 450 ,270, fill = 'black' )#done1
        line9 = self.mainCanvas.create_rectangle(80, 345, 235 ,340, fill = 'black' ) #done2
        line9 = self.mainCanvas.create_rectangle(295, 345, 450 ,340, fill = 'black' ) #done2
        line10 = self.mainCanvas.create_rectangle(445, 340, 450 ,520, fill = 'black' )
        line11 = self.mainCanvas.create_rectangle(515, 340, 520 ,400, fill = 'black' )#right room bottom
        line11 = self.mainCanvas.create_rectangle(515, 460, 520 ,520, fill = 'black' )#done
        line12 = self.mainCanvas.create_rectangle(515, 80, 520 ,270, fill = 'black' )#right room top
        line13 = self.mainCanvas.create_rectangle(515, 270, 580 ,275, fill = 'black' )
        line13 = self.mainCanvas.create_rectangle(640, 270, 720 ,275, fill = 'black' )
        line14 = self.mainCanvas.create_rectangle(520, 340, 720 ,345, fill = 'black' )
        line15 = self.mainCanvas.create_rectangle(270, 80, 275 ,270, fill = 'black' )#split between two rooms

	def close(self):
		root.destroy()
        root.quit()
        #sys.exit()
        
    def lineStatus(self, xL, yL, xR, yR):
        leftRGB = (im[xL, yL][0], im[xL, yL][1], im[xL, yL][2])
        rightRGB = (im[xR, yR][0], im[xR, yR][1], im[xR, yR][2])
        if (leftRGB == (255, 255, 255)):
            left = True
        elif (leftRGB == (0, 0, 0)):
            left = False
        else:
            return (None, None)

        if  (rightRGB == (255, 255, 255)):
            right = True
        elif (rightRGB == (0, 0, 0)):
            right = False
        else:
            return (None, None)
        return (left, right)

    def getColor(self, xL, yL, xR, yR):
        RGBright = (im[xR, yR][0], im[xR, yR][1], im[xR, yR][2])
        RGBleft = (im[xL, yL][0], im[xR, yR][1], im[xR, yR][2])
        return RGBleft, RGBright

    def addNewRobot(self, loc):
        r = self.mainCanvas.create_oval(loc[0] - 8, loc[1] + 8, loc[0] + 8, loc[1] - 8, fill = 'blue')
        return r

    def moveRobot(self, r):
        old_loc = r.GUI_LAST_LOC
        new_loc = r.getLoc()
        r.GUI_LAST_LOC = new_loc
        self.mainCanvas.delete(r.IDL)
        self.mainCanvas.delete(r.IDR)
        LR = new_loc[2] + pi/6
        RR = new_loc[2] - pi/6
        self.mainCanvas.move(r.ID, new_loc[0] - old_loc[0], new_loc[1] - old_loc[1])
        r.IDL = self.mainCanvas.create_line(
            new_loc[0] + 32*cos(LR), 
            new_loc[1] - 32*sin(LR), 
            new_loc[0], new_loc[1], 
            new_loc[0] + 32*cos(RR), 
            new_loc[1] - 32*sin(RR))

    def dropBeacon(self, xL, yL, explored):
        #print xL, yL
        80, 345, 235 ,340
        if explored == False:
            print 'marking unexplored'
            if (xL >= 100 and xL <= 240 and yL >= 330 and yL <= 350):
                width, height = pic.size
                for x in range(350):
                    for y in range(300,height):
                        r, g, b, a = im[x, y]
                        if (r, g, b) == (0, 255, 0):
                            im[x, y] = (125, 125, 125, a)
            elif(xL >= 400 and xL <= 700 and yL >= 450 and yL <= 600):
                width, height = pic.size
                for x in range(350, 799):
                    for y in range(300,height):
                        r, g, b, a = im[x, y]
                        if (r, g, b) == (0, 255, 0):
                            im[x, y] = (125, 125, 125, a)
            elif(xL >= 600 and xL <= 799 and yL >= 200 and yL <= 300):
                width, height = pic.size
                for x in range(600, 799):
                    for y in range(200,350):
                        r, g, b, a = im[x, y]
                        if (r, g, b) == (0, 255, 0):
                            im[x, y] = (125, 125, 125, a)
            elif(xL >= 400 and xL <= 550 and yL >= 100 and yL <= 450):
                width, height = pic.size
                for x in range(400, 550):
                    for y in range(100,450):
                        r, g, b, a = im[x, y]
                        if (r, g, b) == (0, 255, 0):
                            im[x, y] = (125, 125, 125, a)
            elif(xL >= 200 and xL <= 500 and yL >= 200 and yL <= 450):
                width, height = pic.size
                for x in range(200, 500):
                    for y in range(200,450):
                        r, g, b, a = im[x, y]
                        if (r, g, b) == (0, 255, 0):
                            im[x, y] = (125, 125, 125, a)
            elif(xL >= 420 and xL <= 480 and yL >= 320 and yL <= 360):
                width, height = pic.size
                for x in range(420, 480):
                    for y in range(320,360):
                        r, g, b, a = im[x, y]
                        if (r, g, b) == (0, 255, 0):
                            im[x, y] = (125, 125, 125, a)
        else:
            print 'marking explored'
            if (xL >= 235 and xL <= 350 and yL >= 280 and yL <= 350):
                print 'changing 1'
                width, height = pic.size
                for x in range(225,400):
                    for y in range(340,345):
                        r,g,b,a = im[x,y]
                        im[x,y] = (0,0,0,a)
            elif (xL >= 500 and xL <= 530 and yL >= 343 and yL <= 520):
                print 'changing 2'
                width, height = pic.size
                for x in range(518,520):
                    for y in range(350,465):
                        r,g,b,a = im[x,y]
                        im[x,y] = (0,0,0,a)
            elif (xL >= 560 and xL <= 700 and yL >= 260 and yL <= 280):
                print 'changing 3'
                width, height = pic.size
                for x in range(530,645):
                    for y in range(270,275):
                        r,g,b,a = im[x,y]
                        im[x,y] = (0,0,0,a)
            elif (xL >= 445 and xL <= 460 and yL >= 80 and yL <= 280):
                print 'changing 4'
                width, height = pic.size
                for x in range(445,450):
                    for y in range(135,270):
                        r,g,b,a = im[x,y]
                        im[x,y] = (0,0,0,a)
            elif (xL >= 100 and xL <= 300 and yL >= 260 and yL <= 280):
                print 'changing 5'
                width, height = pic.size
                for x in range(100,215):
                    for y in range(270,275):
                        r,g,b,a = im[x,y]
                        im[x,y] = (0,0,0,a)
        pic.save('worldhi.png')
        
