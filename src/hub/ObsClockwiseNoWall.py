from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from dissociating import *
from pybricks.tools import wait, StopWatch
printInfo()

HUB.imu.reset_heading(0)

from ObstacleClockwise import greenStart, redStart, greenEnding, redEnding, greenFirst, redFirst, greenLast, redLast, greenRed, redGreen, greenOnly, redOnly, \
    greenParking, redParking, \
    DEFAULT, PARALLEL, MAXSPEED, WALLING_KP, MAXLOOK, PARKINGLAP, WALLINGREVERSEANGLE, \
    WALLING_ANGLE_RIGHT, WALLING_ANGLE_LEFT, WALLING_TURN_TOLERANCE, WALLING_ERROR_TOLERANCE, \
    TURNDURATION, SCANDURATION, RED, GREEN, wallingTurn, wallingTurnAndRecord


def noWallGreenBothEnding(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.turn(580, currentHeading+50)
    sannisLivisa.driveUntilProximity(520, 140, heading=currentHeading+50, lookHeading=currentHeading, selection=FRONT, brake=False)
    # sannisLivisa.eBrake(200)
    sannisLivisa.turn(500, currentHeading+90)
    sannisLivisa.drive(400, 400, 600, heading=currentHeading+90, decelerate=True)
    sannisLivisa.lookDir(0, False)
    return currentHeading+90

def noWallRedBothEnding(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.drive(250, 500, 600, heading=currentHeading, decelerate=True, stopBool=True)
    sannisLivisa.driveUntilProximity(-400, 824, heading=currentHeading, lookHeading=currentHeading, reverseCondition=True)
    # sannisLivisa.drive(-150, 300, 400, heading=currentHeading, decelerate=True, stopBool=True)
    sannisLivisa.drive(20, 500, 600, heading= currentHeading, decelerate=True)
    sannisLivisa.turn(520, currentHeading + 90)
    sannisLivisa.drive(150, 500, 600, heading= currentHeading+90, decelerate=True)#, stopBool=True)
    # sannisLivisa.drive(-250, 500, 600, heading=currentHeading+90, decelerate=True)
    return currentHeading+90

def noWallGreenRedEnding(sannisLivisa: FE, currentHeading=0):

    sannisLivisa.drive(200, 500, 600, heading=currentHeading, decelerate=True)
    sannisLivisa.eBrake(100)
    # sannisLivisa.driveUntilProximity(400, 820, heading=currentHeading, selection=FRONT, brake=True, lookHeading=currentHeading)
    # beep()
    sannisLivisa.driveUntilProximity(-350, 750, heading=currentHeading, selection=FRONT, lookHeading=currentHeading, reverseCondition=True, brake=True)
    sannisLivisa.turn(580, currentHeading+93)
    # sannisLivisa.drive(800, 400, 600, decelerate=True, heading=currentHeading+90)
    sannisLivisa.driveUntilStalled(-210, MAXSPEED//1.5, MAXSPEED//3, heading=currentHeading+93)
    HUB.imu.reset_heading(0)
    sannisLivisa.drive(1100, 500, 600, heading=0, decelerate=True)
    # beep()
    return 0

def noWallRedGreenEnding(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.driveUntilProximity(500, 710, heading=currentHeading, selection=FRONT, brake=True, lookHeading=currentHeading)
    sannisLivisa.turn(500, -60+currentHeading)
    sannisLivisa.turn(580, currentHeading+92)
    # sannisLivisa.drive(100, 500, 600, heading=currentHeading+90, decelerate=True, stopBool=True, stopDuration=200)
    sannisLivisa.drive(-400, 500, 600, heading=currentHeading+90, decelerate=True, stopBool=True)
    sannisLivisa.drive(500, 300, 600, heading=currentHeading+90, decelerate=True, stopBool=False)
    return currentHeading+90
    # d

def noWallGreenOnly(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.driveDistAdjust(900, 500, 750, 100, LEFT, heading=currentHeading, decelerate=True, tolerance=28)
    # sannisLivisa.drive(1300, 500, 900, heading=currentHeading, decelerate=True)

def noWallRedOnly(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.driveDistAdjust(1100, 500, 750, 110, RIGHT, heading=currentHeading, decelerate=True, tolerance=28)
    # sannisLivisa.drive(1100, 500, 900, heading=currentHeading, decelerate=True)
    # pass

def greenLast(sannisLivisa: FE, recording=False, parking=False, ending=True, currentHeading=0):
    if recording:
        sannisLivisa.lookDir(90, asyncBool=False)
        if not parking:
            sannisLivisa.turn(580, currentHeading-56)
            sannisLivisa.drive(590, 500, 800, heading=currentHeading-56, decelerate=True)
            # sannisLivisa.driveUntilProximity(500, 120, heading=currentHeading-56, lookHeading=currentHeading-90, brake=False)
            sannisLivisa.turn(580, currentHeading-2)
            sannisLivisa.drive(270, 500, 700, heading=currentHeading+0)
        else:
            sannisLivisa.drive(90, 500, 600, heading=currentHeading+0)
            sannisLivisa.turn(580, currentHeading-50)
            sannisLivisa.drive(610, 600, 700, heading=currentHeading-50, decelerate=True)
            sannisLivisa.turn(510, currentHeading+0)
            sannisLivisa.drive(200, 600, 700, heading=currentHeading+0, decelerate=True)
    else:
        if not parking:
            sannisLivisa.turn(580, currentHeading-56)
            # sannisLivisa.drive(590, 500, 800, heading=currentHeading-56, decelerate=True)
            sannisLivisa.driveUntilProximity(600, 120, heading=currentHeading-56, lookHeading=currentHeading-90, brake=False, maxDistance=590)
            sannisLivisa.turn(580, currentHeading-2)
            sannisLivisa.drive(270, 500, 700, heading=currentHeading+0)
        else:
            sannisLivisa.drive(90, 500, 600, heading=currentHeading+0)
            sannisLivisa.turn(580, currentHeading-50)
            sannisLivisa.drive(610, 600, 700, heading=currentHeading-50, decelerate=True)
            sannisLivisa.turn(510, currentHeading+0)
            sannisLivisa.drive(200, 600, 700, heading=currentHeading+0, decelerate=True)

    if ending:
       greenEnding(sannisLivisa, startingAngle=currentHeading+0)

def redLast(sannisLivisa: FE, recording=False, parking=False, ending=True, currentHeading=0):
    if recording:
        sannisLivisa.lookDir(90, asyncBool=False)
        if not parking:
            # Not parking
            sannisLivisa.turn(580, currentHeading+ 57)
            sannisLivisa.drive(500, 500, 700, heading=currentHeading+57, decelerate=True)
            # sannisLivisa.driveUntilProximity(500, 120, heading=currentHeading+57, lookHeading=currentHeading+90, brake=False)
            sannisLivisa.turn(520, currentHeading+0)
            sannisLivisa.drive(170, 500, 600, heading=currentHeading+0)
        else:
            sannisLivisa.turn(520, currentHeading+45)
            sannisLivisa.drive(400, 500, 600, heading=currentHeading+45)
            sannisLivisa.turn(460,currentHeading+ 0)
            sannisLivisa.drive(350, 500, 600, heading=currentHeading+0)
    else:

        if not parking:
            # Not parking
            sannisLivisa.turn(580, currentHeading+ 57)
            # sannisLivisa.drive(500, 500, 800, heading=currentHeading+57, decelerate=True)
            sannisLivisa.driveUntilProximity(680, 110, heading=currentHeading+57, lookHeading=currentHeading+90, brake=False, maxDistance=570)
            sannisLivisa.turn(520, currentHeading+0)
            sannisLivisa.drive(170, 500, 600, heading=currentHeading+0)
        else:
            sannisLivisa.turn(520, currentHeading+45)
            sannisLivisa.drive(400, 500, 600, heading=currentHeading+45)
            sannisLivisa.turn(460,currentHeading+ 0)
            sannisLivisa.drive(350, 500, 600, heading=currentHeading+0)
    # redEnding(sannisLivisa)

    if ending:
        redEnding(sannisLivisa, startingAngle=currentHeading)

#########################################
# --            Lap Logic            -- #
#########################################
def recordQuarterLap(sannisLivisa: FE, initalDetection: tuple, currentLap=0.25):
    # sannisLivisa.center()
    pillarColor = wallingTurnAndRecord(sannisLivisa, initalDetection)
    
    currentLapRecord = []
    prevTurn = ""

    log("1.", pillarColor)
    
    if pillarColor == "Green":
        greenFirst(sannisLivisa, brake=True)
        prevTurn = "LEFT"
    elif pillarColor == "Red":
        redFirst(sannisLivisa, brake=True)
        prevTurn = "RIGHT"
    else:
        if DEFAULT == "Red":
            redFirst(sannisLivisa, brake=True)
            prevTurn = "RIGHT"
            pillarColor = "Red"
        else:
            greenFirst(sannisLivisa, brake=True)
            prevTurn = "LEFT"
            pillarColor = "Green"

    currentLapRecord.append((pillarColor))

    if pillarColor == "Green":
        pillarColor = scanOnce(sannisLivisa,  70, -15, minThreshold=400)
    else:
        pillarColor = scanOnce(sannisLivisa, 0, -70, minThreshold=400)

    log("2.", pillarColor)

    try:
        if currentLapRecord[0] != pillarColor:
            currentLapRecord.append((pillarColor))
    except:
        currentLapRecord.append((pillarColor))

    sannisLivisa.center()

    if pillarColor == "Green" and prevTurn != "LEFT":
        greenLast(sannisLivisa, recording=True, ending=True)

    elif pillarColor == "Red" and prevTurn != "RIGHT":
        redLast(sannisLivisa, recording=True, ending=True)

    else:
        beep()
        log(currentLapRecord)
        sannisLivisa.lookDir(90, asyncBool=False)
        sannisLivisa.drive(1150, 500, 900, heading=0, decelerate=True)

        if currentLapRecord[0] == "Green":
            greenEnding(sannisLivisa)
            currentLapRecord.append(("Green"))
        else:
            redEnding(sannisLivisa)
            currentLapRecord.append(("Red"))

    # sannisLivisa.driveUntilStalled(100, 600, 300, heading=0)

    currentLapRecord = [e for e in currentLapRecord if e != 'None']
    log(currentLapRecord)

    sannisLivisa.record(str(currentLap)[1::], currentLapRecord)
    # sannisLivisa.drive(50, 500, 600, heading=0)
    # sannisLivisa.eBrake(100)

def runRecord(sannisLivisa: FE, currentLap, ending=False):
    beep()
    formattedCurrent = str(currentLap)[1::]
    currentObstacles = sannisLivisa.remember(formattedCurrent)

    parking = formattedCurrent == PARKINGLAP
    log(f"Lap {currentLap} Obstacles:", currentObstacles)

    if list(set(currentObstacles)) == GREEN:
        greenOnly(sannisLivisa, parking, ending)

    elif list(set(currentObstacles)) == RED:
        redOnly(sannisLivisa, ending)

    elif currentObstacles == GREEN + RED:
        greenRed(sannisLivisa, False, parking, ending)

    elif currentObstacles ==  RED + GREEN:
        redGreen(sannisLivisa, False, parking, ending)

    if ending:    
        sannisLivisa.driveUntilStalled(150, 600, 300, heading=0)

    return [currentObstacles[-1]]

def runOptimizedQuarterLap(sannisLivisa: FE, currentLap):
    newHeading = 0
    finalObstacle = [DEFAULT]
    runRecord(sannisLivisa, 0.25)
    lastObstacle = sannisLivisa.remember(".25")[-1]
    for i in range(2):
        formattedNext = str(currentLap+0.25)[1::]
        nextObstacles = sannisLivisa.remember(formattedNext)
        print(lastObstacle, nextObstacles[0], currentLap)
        # print(lastObstacle + [nextObstacles[0]])
        # print(lastObstacle + nextObstacles[0])
        if [lastObstacle] + [nextObstacles[0]] == GREEN + GREEN:
            beep(800)
            newHeading = noWallGreenBothEnding(sannisLivisa, currentHeading=newHeading)

            if [nextObstacles[-1]] == GREEN:
                noWallGreenOnly(sannisLivisa, newHeading)
                finalObstacle = GREEN

            else:
                redLast(sannisLivisa, ending=False, currentHeading=newHeading)    
                finalObstacle = RED


        elif [lastObstacle] + [nextObstacles[0]] == RED + RED:
            newHeading = noWallRedBothEnding(sannisLivisa, currentHeading=newHeading)

            if [nextObstacles[-1]] == GREEN:
                greenLast(sannisLivisa, ending=False, currentHeading=newHeading)
                finalObstacle = GREEN

            else:
                noWallRedOnly(sannisLivisa, newHeading)
                finalObstacle = RED
            
        
        elif [lastObstacle] + [nextObstacles[0]] == GREEN + RED:
            newHeading = noWallGreenRedEnding(sannisLivisa, currentHeading=newHeading)
            # print(lastObstacle, nextObstacles)
            if [nextObstacles[-1]] == GREEN:
                # noWallGreenOnly(sannisLivisa, newHeading)
                greenLast(sannisLivisa, ending=False, currentHeading=newHeading)
                finalObstacle = GREEN
            else:
                noWallRedOnly(sannisLivisa, newHeading)
                finalObstacle = RED

        elif [lastObstacle] + [nextObstacles[0]] == RED + GREEN:
            newHeading = noWallRedGreenEnding(sannisLivisa, currentHeading=newHeading)
            # print(lastObstacle, nextObstacles)
            if [nextObstacles[-1]] == GREEN:
                # noWallGreenOnly(sannisLivisa, newHeading)
                # greenLast(sannisLivisa, ending=False, currentHeading=newHeading)
                noWallGreenOnly(sannisLivisa, newHeading)
                finalObstacle = GREEN
            else:
                redLast(sannisLivisa, currentHeading=newHeading, ending=False)
                finalObstacle = RED

        currentLap +=0.25
        lastObstacle = nextObstacles[-1]

    if finalObstacle == GREEN:
        greenEnding(sannisLivisa, newHeading)
    else:
        redEnding(sannisLivisa, newHeading)


    sannisLivisa.driveUntilStalled(150, 200, 600, heading=newHeading, decelerate=True)
    return newHeading

    
def runRecordParking(sannisLivisa: FE, currentHeading=0):
    wallingTurn(sannisLivisa, currentHeading)
    beep(700, 100)

    currentObstacles = sannisLivisa.remember(".0")
    log(f"Lap Final Obstacles:", currentObstacles)

    if currentObstacles[0] == "Green":
        greenParking(sannisLivisa, currentHeading)
    else:
        redParking(sannisLivisa, currentHeading)

def ClockwiseNoWall(sannisLivisa: FE):
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
        sannisLivisa.record(".0", [details[0][0]])

    log("First Detection:", pillarColor, data, details)

    sannisLivisa.center()
    print(sannisLivisa.memory)
    sannisLivisa.lookDir(90, asyncBool=False)
    if pillarColor == "Green":  
        greenStart(sannisLivisa)

    elif pillarColor == "Red":
        redStart(sannisLivisa)        

    else:                
        beep()    
        details = [[DEFAULT, (0,0,0), 0]]                    
        sannisLivisa.record(".0", [i[0] for i in details])
        if DEFAULT == "Red":
            redStart(sannisLivisa)
        else:
            greenStart(sannisLivisa)

    currentLap = 0

    detections = sannisLivisa.scanUntilStallled(100, 600, 400, 90, heading=-90)
    HUB.imu.reset_heading(0)

    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, detections, currentLap)
        detections = sannisLivisa.scanUntilStallled(80, 600, 400, 90, heading=0)
        
    #TODOt7
    currentLap += 0.25
    newHeading = 0
    for i in range(2):
        wallingTurn(sannisLivisa, newHeading)
        last = runRecord(sannisLivisa, currentLap, ending=True)
        wallingTurn(sannisLivisa)
        currentLap += 0.25
    
        newHeading = runOptimizedQuarterLap(sannisLivisa, currentLap)
        currentLap += 0.75

    # Optimized run
    # currentLap += 0.25
    # runRecord(sannisLivisa, currentLap)
    runRecordParking(sannisLivisa, newHeading)

def checkParking(sannisLivisa: FE, color):
    sannisLivisa.record(".0", color)
    runRecordParking(sannisLivisa)


if __name__ == "__main__":
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.F, Port.D, Port.C, camEnabled=True)
    ClockwiseNoWall(sannisLivisa)
    # wallingTurn(sannisLivisa)
    # checkParking(sannisLivisa, RED)
