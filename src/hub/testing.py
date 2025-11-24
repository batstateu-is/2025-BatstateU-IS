from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from dissociating import *
import umath
# from OpenChallenge impor4t OpenChallenge
# OpenChallenge()

import ObstacleCounter as CC
import ObstacleClockwise as CW

printInfo()
sannisLivisa = FE(Port.A, Port.B, Port.E, Port.F, Port.D, Port.C, camEnabled=True)


# DIRECTION = 1
from ObstacleChallenge import Obstacle
# from ObstacleCounter import greenStart, redStart, redGreen, greenRed, greenOnly, redOnly, recordQuarterLap, greenFirst, wallingTurnAndRecord, wallingTurn, runRecord

def Counter(sannisLivisa: FE):
    sannisLivisa.lookDir(-28)
    details=[]
    pillarColor, data = sannisLivisa.determineTrafficSignBlob()
    if pillarColor == 'None' or data[2] < 700:
        # pillarColor, data, details = scanList(sannisLivisa, -90, 45, delayTime=10, minThreshold=270)
        # pillarColor, data, angle = details[-1]
        parkingLap = []
        pillarColor = scanOnce(sannisLivisa,  -85, 0, minThreshold=270)
        parkingLap.append(pillarColor)
        pillarColor = scanOnce(sannisLivisa, 0, 60, minThreshold=270)
        parkingLap.append(pillarColor)

        sannisLivisa.record(".0", parkingLap)

    else:
        details = [[pillarColor, data, -30]]

    log("First Detection:", pillarColor, data, details)
    log("First Lap:", pillarColor, data, details)

    # sannisLivisa.record(".0", [i[0] for i in details])
    sannisLivisa.center()

    sannisLivisa.lookDir(-90, asyncBool=False)

    if pillarColor == "Green":  
        CC.greenStart(sannisLivisa)

    elif pillarColor == "Red":
        CC.redStart(sannisLivisa)        

    else:                
        beep()                        
        if DEFAULT == "Red":
            CC.redStart(sannisLivisa)
        else:
            CC.greenStart(sannisLivisa)

    currentLap = 0

    detections = sannisLivisa.scanUntilStallled(100, 600, 400, -90, heading=90)
    HUB.imu.reset_heading(0)
    while True:
        currentLap = 0

        for i in range(4):
            currentLap += 0.25
            CC.recordQuarterLap(sannisLivisa, detections, currentLap)
            detections = sannisLivisa.scanUntilStallled(80, 600, 300, -90, heading=0)

        # currentLap += 0.25
        # recordQuarterLap(sannisLivisa, detections, currentLap)
        # detections = sannisLivisa.scanUntilStallled(80, 600, 300, -90, heading=0)
        # currentLap += 0.25
        # recordQuarterLap(sannisLivisa, detections, currentLap)
        # detections = sannisLivisa.scanUntilStallled(100, 600, 300, -90, heading=0)

        sannisLivisa.memory = {

        }



        
def Clockwise(sannisLivisa: FE):
    sannisLivisa.lookDir(-30)
    details=[]
    pillarColor, data = sannisLivisa.determineTrafficSignBlob()
    if pillarColor == 'None' or data[2] < 600:

        # pillarColor, data, details = scanList(sannisLivisa, 50, -85, delayTime=5, minThreshold=270)
        parkingLap = []
        pillarColor = scanOnce(sannisLivisa,  70, -15, minThreshold=270)
        parkingLap.append(pillarColor)
        pillarColor = scanOnce(sannisLivisa, -15, -85, minThreshold=270)
        parkingLap.append(pillarColor)

        sannisLivisa.record(".0", parkingLap)

    else:
        details = [[pillarColor, data, -30]]
        sannisLivisa.record(".0", [pillarColor])

    log("First Detection:", pillarColor, data, details)
    # pillarColor = "Gww

    sannisLivisa.center()

    sannisLivisa.lookDir(90, asyncBool=False)
    if pillarColor == "Green":  
        CW.greenStart(sannisLivisa)

    elif pillarColor == "Red":
        CW.redStart(sannisLivisa)        

    else:                
        beep()    
        details = [[DEFAULT, (0,0,0), 0]]                    
        sannisLivisa.record(".0", [i[0] for i in details])
        if DEFAULT == "Red":
            CW.redStart(sannisLivisa)
        else:
            CW.greenStart(sannisLivisa)

    currentLap = 0

    detections = sannisLivisa.scanUntilStallled(100, sannisLivisa.speed(), 200, 90, heading=-90)
    HUB.imu.reset_heading(0)

    # for i in range(3):
    #     currentLap += 0.25
    #     recordQuarterLap(sannisLivisa, detections, currentLap)
    #     detections = sannisLivisa.scanUntilStallled(110, sannisLivisa.speed(), 200, 90, heading=0)
    #     sannisLivisa.eBrake(10)
    #     HUB.imu.reset_heading(0)
        
    # for i in range(8):
    #     currentLap += 0.25
    #     runRecord(sannisLivisa, currentLap)
    ###--------
        
    detections = sannisLivisa.scanUntilStallled(100, 600, 400, 90, heading=-90)
    HUB.imu.reset_heading(0)
    while True:
        currentLap = 0

        for i in range(4):
            currentLap += 0.25
            CW.recordQuarterLap(sannisLivisa, detections, currentLap)
            detections = sannisLivisa.scanUntilStallled(110, sannisLivisa.speed(), 200, 90, heading=0)
        # currentLap += 0.25
        # currentLap += 0.25
        # recordQuarterLap(sannisLivisa, detections, currentLap)
        # detections = sannisLivisa.scanUntilStallled(80, 600, 300, -90, heading=0)
        # currentLap += 0.25
        # recordQuarterLap(sannisLivisa, detections, currentLap)
        # detections = sannisLivisa.scanUntilStallled(100, 600, 300, -90, heading=0)

        sannisLivisa.memory = {

        }

    CW.runRecordParking(sannisLivisa)

direction = Obstacle(sannisLivisa)

if direction == "clockwise":

    Clockwise(sannisLivisa)
else:
    Counter(sannisLivisa)