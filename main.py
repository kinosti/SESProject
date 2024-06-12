import bimatrix_communication as bm
import ping_to_data as p2d
import transfer_data as td

from settings import *

import typing

import threading

import time

import keyboard

from helpers import *


""" 
main.py

The main module handling full process of BiMatrix communication and ping localization.
"""

global pingData, exitRequested
goalBehind = False
pingData = (0,0)
exitRequested = False

def t1():
    global pingData
    global goalBehind
    global exitRequested

    # ---- Set connection to BiMatrix and initialize base settings
    bm.initializeController()

    # ---- Initialize Gaussian Normal Distribution lookup-table with the initial data limits
    GaussianLookup = p2d.calcGaussianCoeffLookupTable()

    sleepTime = 0.0001
    
    trialTimes = []
    trialStartTime = 0
    trialTimeAVG = 0
    trialCount = 0

    trialComparisonAmount = 3
    trialFirstBatchScore = 0
    trialLastBatchScore = 0
    trialFirstBatchTimes = []
    trialLastBatchTimes = []

    # ---- Loop until exit:
    prevTriggerTime = 0
    prevTime = time.perf_counter()
    while True: 
        if exitRequested:
            res = bm.setPulseGenerator(False)
            bm.close()
            #raise Exception('q/esc pressed, exiting...')
            #return
            print(trialTimes)
            print("Total AVG time: " + str(round(trialTimeAVG,1)))
            print("AVG time from first vs last " +  str(trialComparisonAmount) + "trials: " + str(round(trialFirstBatchScore,1)) + "s vs " + str(round(trialLastBatchScore,1)) + "s")
            raise SystemExit()
        
        now = time.perf_counter()
        #print(now,prevTime,now-prevTime,sleepTime,now-prevTime > sleepTime)
        if now-prevTime > sleepTime:
            prevTime = now
            # ---- Fetch ping location (ping is updated separately with independent refresh rate, so the ping might or might not be updated from previous loop)
            
            if pingData != (0,0):
                if trialStartTime == 0:
                    # Started to look for another target
                    trialStartTime = time.perf_counter()
                    
                #sleep(0.2)
                # ---- Calculate pulse sequence data from ping location (that has been transformed based on user orientation)
                data = p2d.getPulseSequenceData(pingData, GaussianLookup, goalBehind)

                # ---- Generate the pulse sequence
                prevTriggerTime = bm.executePulseSequence(data, prevTriggerTime)
            else:
                if trialStartTime != 0:
                    # Target was reached, calculate the time it took
                    trialCount += 1
                    trialTime = time.perf_counter()-trialStartTime
                    trialTimes.append(trialTime)
                    for trial in trialTimes:
                        trialTimeAVG += trial
                    trialTimeAVG /= trialCount

                    if trialCount <= trialComparisonAmount:
                        trialFirstBatchTimes.append(trialTime)
                    if trialCount == trialComparisonAmount:
                        for trial in trialFirstBatchTimes:
                            # if exact number of entries matches the comparison amount, save the first batch avg score
                            trialFirstBatchScore += trial
                        trialFirstBatchScore /= trialComparisonAmount

                    
                    trialLastBatchTimes.append(trialTime)
                    if trialCount > trialComparisonAmount:
                        # if more than compared amount of entries, remove oldest entry
                        trialLastBatchTimes.pop(0)

                    if trialCount >= trialComparisonAmount:
                        # if equal or more entries than comparison amount, update the last batch avg score
                        for trial in trialLastBatchTimes:
                            trialLastBatchScore += trial
                        trialLastBatchScore /= trialComparisonAmount

                    printf(trialTimes,"It took " + str(round(trialTime,1)) + "s [" + str(round(trialTimeAVG,1)) + "s] to reach the target")
                    print("Total AVG time: " + str(round(trialTimeAVG,1)))
                    print("AVG time from first vs last " + str(trialComparisonAmount) + "trials: " + str(round(trialFirstBatchScore,1)) + "s vs " + str(round(trialLastBatchScore,1)) + "s")
                    trialStartTime = 0

def t2():
    global goalBehind
    global pingData
    global exitRequested

    sleepTime = 0.005

    while True:
        if exitRequested:
            #return
            raise SystemExit()

        x, y = td.fetchRelCoordinates(fromFile=True) 
        if P_USELOCPULSE:
            goalBehind=True if y<0 else False
        pingData = (x*10,y*10)

        time.sleep(sleepTime)

if __name__ == '__main__':
    #

    thread1 = threading.Thread(target=t1)
    thread2 = threading.Thread(target=t2)

    threads = [thread1, thread2]

    for thread in threads:
        thread.start()

    while True:
        keyOrg = keyboard.read_key()
        key = keyOrg.lower()
        if key == "q" or key == "esc":
            print()
            print("-------------------------")
            print("User QUIT activated - waiting for all threads to end")
            print("-------------------------")
            print()

            exitRequested = True
            for thread in threads:
                thread.join()

            print()
            print("-------------------------")
            print("All threads are closed - exiting")
            print("-------------------------")
            raise SystemExit()
