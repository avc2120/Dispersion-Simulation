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
ONLINE_ROBOTS = []

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
        ONLINE_ROBOTS.append(bot)
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
    again = True
    global home
    print home
    while again:
        beacon = bot.detectBeacon()
        if (beacon == 0):
            bot.dropBeacon(False)
            bot.stop()
            print 'initializing new robot'
            end_time = time.time() + 1
            if time.time() > end_time:
                thread.start_new_thread(main, ())
            again = False
        elif (beacon == 2):
            print 'marking explored'
            bot.dropBeacon(True)
        elif (beacon == 3 and home == False):
            home = True
            bot.stop()
            ONLINE_ROBOTS.pop(0)
            break
        else:
            bot.followEdge(direction, 250,200)
        
def goHome(direction):
    for x in ROBOTS:
        if x.detectBeacon() == 3:
            ONLINE_ROBOTS.pop(0)
        else:
            x.followEdge(direction, 250, 200)
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
    #goHome('left')