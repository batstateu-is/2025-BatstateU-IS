from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from dissociating import *
from pybricks.tools import wait, StopWatch
printInfo()

HUB.imu.reset_heading(0)

from ObstacleClockwise import greenStart, redStart, greenEnding, redEnding, greenFirst, redFirst, greenLast, redLast, greenRed, redGreen, greenOnly, redOnly, \
    DEFAULT, PARALLEL, MAXSPEED, WALLING_KP, MAXLOOK, PARKINGLAP, WALLINGREVERSEANGLE, \
    WALLING_ANGLE_RIGHT, WALLING_ANGLE_LEFT, WALLING_TURN_TOLERANCE, WALLING_ERROR_TOLERANCE, \
    TURNDURATION, SCANDURATION, RED, GREEN, wallingTurn, wallingTurnAndRecord


def noWallGreenBothEnding(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.turn(500, currentHeading+45)
    sannisLivisa.driveUntilProximity(500, 140)
    sannisLivisa.eBrake(200)
    sannisLivisa.turn(500, currentHeading+90)
    sannisLivisa.drive(200, 400, 600, heading=currentHeading+90, decelerate=True)
    return currentHeading+90

def noWallRedBothEnding(sannisLivisa: FE, currentHeading=0):
    pass

def noWallGreenRedEnding(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.turn(500, currentHeading+90)
    sannisLivisa.drive(400, 400, 600, decelerate=True, heading=currentHeading+90)
    return currentHeading+90

def noWallRedGreenEnding(sannisLivisa: FE):
    pass

def noWallGreenOnly(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.drive(1100, 500, 1000, heading=currentHeading, decelerate=True)

def noWallRedOnly(sannisLivisa: FE):
    pass

# def 

def wallingTurnAndRecord(sannisLivisa: FE, initialDetection: tuple):
    pillarColor = "None"
    targetHeading = 90
    greenDetections, redDetections = initialDetection
    start = HUB.imu.heading() - targetHeading

    while HUB.imu.heading() < targetHeading - WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction < WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800

        lerror = (targetHeading - HUB.imu.heading())*1.1
        speed = linearMap(error, start, 0, MAXSPEED, MAXSPEED // 1.4)

        sannisLivisa.lookDir(lerror, asyncBool=False, speed=1000)
        sannisLivisa.move(-speed, correction)

        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    sannisLivisa.driveUntilStalled(-50, MAXSPEED//1.1, MAXSPEED//1.5, heading=90)
    beep()

    sannisLivisa.lookDir(0)

    # -- Correct if not flush with wall -- #
    sannisLivisa.eBrake(10)
    checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 80, 600, 90, TURNDURATION, 40)

    scanTimer = StopWatch()
    scanTimer.reset()
    scanTimer.resume()
    while scanTimer.time() < SCANDURATION:
        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    log("Red:", redDetections, "| Green:", greenDetections)
    sannisLivisa.eBrake(20)
    sannisLivisa.driveMotor.reset_angle(0)
    HUB.imu.reset_heading(0)
    
    if greenDetections > redDetections:
        return "Green"
    elif redDetections > greenDetections:
        return "Red"
    else:
        return "None"

def wallingTurn(sannisLivisa: FE):
    sannisLivisa.lookDir(0, asyncBool=False)
    targetHeading = 90
    start = HUB.imu.heading() - targetHeading
    while HUB.imu.heading() < targetHeading - WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        speed = linearMap(error, start, 0, MAXSPEED, MAXSPEED // 1.4)
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction < WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        sannisLivisa.move(-speed, correction)

    sannisLivisa.driveUntilStalled(-80, MAXSPEED//1.5, MAXSPEED//2, heading=90)
    beep()
    log("Error in walling:", abs(HUB.imu.heading() - 90))
    sannisLivisa.eBrake(10)
    checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 80, 600, 90, TURNDURATION, 40)

    # sannisLivisa.drive(-50, 500, 600)
    sannisLivisa.driveMotor.reset_angle(0)
    sannisLivisa.eBrake(50)
    HUB.imu.reset_heading(0)

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
        pillarColor = scanOnce(sannisLivisa, -15, -70, minThreshold=400)

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
        else:
            redEnding(sannisLivisa)

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
    
    sannisLivisa.driveUntilStalled(150, 600, 300, heading=0)
    # sannisLivisa.drive(50, 500, 600, heading=0)
    # sannisLivisa.eBrake(100)
    return [currentObstacles[-1]]

def runOptimizedQuarterLap(sannisLivisa: FE, currentLap):
    wallingTurn(sannisLivisa)
    formattedCurrent = str(currentLap)[1::]
    if formattedCurrent == ".75":
        # run normal ending
        last = runRecord(sannisLivisa, currentLap, True)
        return

    currentObstacles = sannisLivisa.remember(formattedCurrent)
    print(sannisLivisa.memory)
    parking = formattedCurrent == PARKINGLAP
    log(f"Lap {currentLap} Obstacles:", currentObstacles)
    

    beep(800)
    wait(1000)
    lastObstacle = runRecord(sannisLivisa, currentLap)
    beep(800)

    newHeading = 0
    for i in range(2):
        formattedNext = str(round(currentLap+0.25, 2))[1::]
        nextObstacles = sannisLivisa.remember(formattedNext)
        print(lastObstacle + [nextObstacles[0]])
        if list(set(lastObstacle + [nextObstacles[0]])) == GREEN:
            newHeading = noWallGreenBothEnding(sannisLivisa)
            noWallGreenOnly(sannisLivisa, newHeading)
        
        elif lastObstacle + [nextObstacles[0]] == GREEN + RED:
            newHeading = noWallGreenRedEnding(sannisLivisa, currentHeading=newHeading)

        currentLap +=0.25
            

    

    
def runRecordParking(sannisLivisa: FE):
    wallingTurn(sannisLivisa)
    beep(700, 100)

    currentObstacles = sannisLivisa.remember(".0")
    log(f"Lap Final Obstacles:", currentObstacles)

    if currentObstacles[0] == "Green":
        greenParking(sannisLivisa)
    else:
        redParking(sannisLivisa)

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

    log("First Detection:", pillarColor, data, details)

    sannisLivisa.center()

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

    currentLap = 0

    detections = sannisLivisa.scanUntilStallled(100, 600, 400, 90, heading=-90)
    HUB.imu.reset_heading(0)

    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, detections, currentLap)
        detections = sannisLivisa.scanUntilStallled(80, 600, 400, 90, heading=0)
        
    #TODOt7
    currentLap += 0.25
    
    for i in range(3):
        wallingTurn(sannisLivisa)
        last = runRecord(sannisLivisa, currentLap, ending=True)
        currentLap += 0.25

        runOptimizedQuarterLap(sannisLivisa, currentLap)
        currentLap += 0.75

    # Optimized run
    currentLap += 0.25
    runRecord(sannisLivisa, currentLap)
    # runRecordParking(sannisLivisa)

def checkParking(sannisLivisa: FE, color):
    sannisLivisa.record(".0", color)
    runRecordParking(sannisLivisa)


if __name__ == "__main__":
    sannisLivisa = FE(Port.A, Port.B, Port.C, Port.F, Port.D, Port.E, camEnabled=True)
    ClockwiseNoWall(sannisLivisa)
    # wallingTurn(sannisLivisa)
    # checkParking(sannisLivisa, RED)
