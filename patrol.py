# -*- coding: utf-8 -*-
import time, threading, thread, datetime
from patrol_config import *
from math import pi
import bot_sim  
NEEDS_REINFORCEMENTS =[]
ROBOTS = []
IDLE_ROBOTS = []
ROFFLINE=[]
EST = False

def initializeRobots():
    #connect with all possible robots and put them into the queue
    global ROBOTS, ROFFLINE, IDLE_ROBOTS
    for i in range(len(ROBOT_LIST_ALL[0])):
        try:
            a=bot.bot(ROBOT_LIST_ALL[0][i][1])
            a.NAME=ROBOT_LIST_ALL[0][i][0]
            a.STATUS="InQueue"
            IDLE_ROBOTS.append(a)
            print a.NAME
            a.stop()
            if(a!=None):
                ROBOTS.append(a)
        except IOError, e:
            print e
            print "Could not connect to %s" %(ROBOT_LIST_ALL[0][i][0])
            ROFFLINE.append(ROBOT_LIST_ALL[0][i])

    for x in ROBOTS:
        x.set_starttime(time.time())
    print 'done initialize'

def initializePositions():
    global ROBOTS
    for i in range(len(ROBOTS)): 
        bot = IDLE_ROBOTS.pop(0)
        print bot.NAME, 'getting on left'
        dispersion(bot, 'left')
        bot.stop()
        print 'stop'

def initOfflineRobot():
    #try to connect to all in roffline
    global ROBOTS, ROFFLINE
    print "trying to reach offline robots"
    for i in range(len(ROFFLINE)):
        try:
            a=bot.bot(ROFFLINE[i][1])
            a.NAME=ROFFLINE[i][0]
            a.STATUS="InQueue"
            if(a!=None):
                ROBOTS.append(a)
                ROFFLINE.pop(i)
                a.set_starttime(time.time())
        except IOError:
            print "Could not connect to %s" %(ROFFLINE[i][0])

def resetRobotConnection(bot):
    #disconnect, wait for recharge, reconnect
    global ROBOTS, ROFFLINE
    counter = 0;
    print "reset", bot.NAME
    bot.stop()
    conn=bot.reconnect()
    while(conn == 2 and counter < 180):
        print bot.NAME, "not connected"
        time.sleep(1)
        conn=bot.reconnect()
        counter=counter+1
    if(counter>=60):
        print bot.NAME, "Could not reconnect"
        for i in range(len(ROBOT_LIST_ALL[0])):
            if(bot.NAME==ROBOT_LIST_ALL[0][i][0]):
                ROBOTS.pop(ROBOTS.index(bot))
                ROFFLINE.append(ROBOT_LIST_ALL[0][i])
                break
    else:
        print bot.NAME, "connected!"
        bot.STATUS="InQueue"
    IDLE_ROBOTS.append(bot)
    bot.PROX.Px = 606
    bot.PROX.Py = 138
    bot.PROX.Pt = -pi/2

def dispersion(bot, direction):
    bot.setScribblerForward()
    print 'scribbler set forward'
    while True:
        global home
        #print home
        beacon = bot.detectBeacon()
        if (home == True and beacon != 3):
                    #print bot.NAME, 'following edge'
                    lines = bot.getBothLines()
                    (lline, rline) = (lines[0], lines[1])
                    if not(lline) and not(rline): 
                        bot.move(250, 200)
                    elif lline and not(rline):           
                        count = 0
                        bot.move(250, 250)
                        inside = True
                    elif lline and rline:                
                        count = 0
                        bot.move(200, 250)
                    elif not(lline) and rline:         
                        count = 0
                        bot.move(250, 200)
                        inside = False
                    else:
                        print("?????")
        elif (beacon == 3):
            #print 'home detected'
            home = True
            bot.stop()
        elif (home == False and beacon == 0):
            bot.dropBeacon(False)
            end_time = time.time() + 0.5
            while time.time() < end_time:
                bot.stop()
            print 'initializing new robot'
            thread.start_new_thread(main, ())   
        elif (beacon == 2):
            #print 'marking explored'
            bot.dropBeacon(True)
        elif (beacon == 4):
            bot.followEdge(250,200)
        
def main():
    global ROBOTS, ROFFLINE, NEEDS_REINFORCEMENTS, IDLE_ROBOTS
    initializePositions()
    EST = True  #Enable random exits           
    #Call reinforcements for exiting robots

if __name__ == "__main__":
    print 'count set'
    global home
    home = False
    initializeRobots()
    print 'robots initialized'
    thread.start_new_thread(main, ())
    input()