from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from dissociating import *
from pybricks.tools import wait, StopWatch
# import os
# print()
printInfo()

HUB.imu.reset_heading(0)

DEFAULT = "Red"
MAXSPEED = 550
WALLING_KP = 0.88
MAXLOOK = -63
PARKINGLAP = ".0"
WALLINGREVERSEANGLE = -49
WALLING_ANGLE_RIGHT = 22
WALLING_ANGLE_LEFT  = -48
WALLING_TURN_TOLERANCE = 6

WALLING_ERROR_TOLERANCE = 4.5
TURNDURATION = 800
RED = ['Red']
GREEN = ['Green']

#########################################
# --        Walling for ending       -- #
#########################################
def greenEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.drive(80, 500, 800, heading=startingAngle)
    sannisLivisa.turn(500, startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.drive(310, 600, 800, heading=startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.turn(500, startingAngle)

def redEnding(sannisLivisa: FE, startingAngle=0):

    sannisLivisa.turn(400, startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.drive(160, 500, 600, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(450, startingAngle)
    sannisLivisa.drive(250, 500, 600, heading=startingAngle)

#########################################
# --      Exiting Parking Area       -- #
#########################################
def greenStart(sannisLivisa: FE):
    sannisLivisa.drive(40, 500, 800, heading=0)
    sannisLivisa.turn(400, -90)
    sannisLivisa.drive(50, 500, 600, heading=-90)
    sannisLivisa.drive(1250, 500, 600, heading=-96)
    
def redStart(sannisLivisa: FE):
    sannisLivisa.drive(480, 500, 700, heading=0)
    sannisLivisa.turn(400, -90)
    sannisLivisa.drive(620, 500, 700, heading=-91)
    redEnding(sannisLivisa, -90)

#########################################
# --             Parking             -- #
#########################################

def sharedParking(sannisLivisa: FE):
    sannisLivisa.lookDir(-40)
    sannisLivisa.turn(300, 40, True)

    beep()
    # sannisLivisa.turn(200, 5, reverse=True)
    sannisLivisa.driveUntilProximity(-210, 500, selection="front", heading=45, lookHeading=-10)
    sannisLivisa.driveUntilProximity(-210, 50, selection="back", heading=0, lookHeading=0)
    while abs(0 - HUB.imu.heading()) > 5:
        sannisLivisa.driveUntilProximity(110, 40, selection="front", heading=-20, lookHeading=0)
        sannisLivisa.driveUntilProximity(-110, 48, selection="back", heading=-20, lookHeading=0)

   

    sannisLivisa.eBrake(200)

def greenParking(sannisLivisa: FE):
    greenFirst(sannisLivisa, parking=True, brake=False)
    # sannisLivisa.drive(20, 500, 600, heading=0)
    # sannisLivisa.turn(500, 90)
    # sannisLivisa.drive(280, 500, 600, heading=90)
    # sannisLivisa.driveUntilStalled(-140, 700, 800, heading=90)
    # sannisLivisa.eBrake(100)
    # sharedParking(sannisLivisa)
    # sannisLivisa.drive(50, 500, 600, heading=0)
    # sannisLivisa.eBrake(200)
    sannisLivisa.drive(80, 500, 600, heading=0)
    sannisLivisa.turn(450, 90)
    sannisLivisa.driveUntilStalled(-100, 500, 600, heading=90)


def redParking(sannisLivisa: FE):
    redFirst(sannisLivisa, True, False)
    # sannisLivisa.drive(290, 500, 600, heading=-2)
    sannisLivisa.drive(180, 500, 600, heading=0)
    sannisLivisa.turn(500, -90)
    sannisLivisa.drive(80, 500, 600, heading=-90)
    sannisLivisa.driveUntilStalled(-400, 400, 500, heading=-91)

#########################################
# -- First Obstacle (If there is ONE) --#
#########################################
def greenFirst(sannisLivisa: FE, parking=False, brake=True):
    if not parking:
        sannisLivisa.drive(270, 500, 600, heading=0)
        sannisLivisa.turn(400, -45)
        sannisLivisa.drive(210, 500, 600, heading=-45)
        sannisLivisa.turn(430, 0)
        sannisLivisa.drive(50, 500, 600, heading=0)

        sannisLivisa.center()
    else:
        sannisLivisa.turn(400, -20)
        sannisLivisa.drive(110, 500, 600, heading=-20)
        sannisLivisa.turn(300, 0)
        sannisLivisa.drive(380, 500, 600, heading=0)


    if brake:
        sannisLivisa.eBrake(200)

def redFirst(sannisLivisa: FE, parking=False, brake=True):
    sannisLivisa.drive(250, 500, 600, heading=0)
    sannisLivisa.turn(430, 34)
    sannisLivisa.drive(260, 500, 600, heading=34)
    # sannisLivisa.eBrake(10000)
    sannisLivisa.turn(470, 0)
    sannisLivisa.drive(80, 500, 600, heading=0)
    # sannisLivisa.driveUntilProximity(500, 400, heading=0, selection="back")
    # sannisLivisa.center()

    if brake:
        sannisLivisa.eBrake(200)

#########################################
# -- Next Obstacle (If there is ONE) -- #
#########################################
def greenLast(sannisLivisa: FE, recording=False, parking=False):
    if not recording:
        sannisLivisa.lookDir(90, asyncBool=False)
    if not parking:
        sannisLivisa.turn(400, -53)
        sannisLivisa.drive(520, 500, 600, heading=-53)
        sannisLivisa.turn(480, 0)
        sannisLivisa.drive(400, 500, 600, heading=0)
    else:
        sannisLivisa.turn(400, -44)
        sannisLivisa.drive(800, 500, 700, heading=-44)
        sannisLivisa.turn(400, 20)

    greenEnding(sannisLivisa)

def redLast(sannisLivisa: FE, recording=False, parking=False):
    if not recording:
        sannisLivisa.lookDir(90, asyncBool=False)
        
    if not parking:
        # Not parking
        sannisLivisa.turn(430, 43)
        sannisLivisa.drive(710, 500, 600, heading=43)
        sannisLivisa.turn(470, 0)
        sannisLivisa.drive(250, 500, 600, heading=0)
    else:
        sannisLivisa.turn(400, 34)
        sannisLivisa.drive(650, 500, 600, heading=34)
        sannisLivisa.turn(370, 0)
        sannisLivisa.drive(300, 500, 600, heading=0)
    redEnding(sannisLivisa)

#########################################
# --      Pre Recorded Movements     -- #
#########################################
def greenOnly(sannisLivisa: FE, parking):
    greenFirst(sannisLivisa, parking, brake=False)

    sannisLivisa.drive(900, 500, 700, heading=-2)

    if not parking:
        greenEnding(sannisLivisa)
    else:
        sannisLivisa.drive(700, 500, 600, heading=4)
        # sannisLivisa.drive(400, 500, 600, heading=0)\

def redOnly(sannisLivisa: FE):
    redFirst(sannisLivisa, brake=False)
    sannisLivisa.drive(1250, 400, 700, heading=0)

    redEnding(sannisLivisa)


def greenRed(sannisLivisa: FE, recording=True, parking=False):
    greenFirst(sannisLivisa, parking, brake=False)
    redLast(sannisLivisa, recording, parking)

def redGreen(sannisLivisa: FE, recording=True, parking=False):
    redFirst(sannisLivisa, brake=False)
    greenLast(sannisLivisa, recording, parking)

def wallingTurnAndRecord(sannisLivisa: FE):
    pillarColor = "None"
    targetHeading = 90
    # Turn and record

    greenDetections = 0
    redDetections = 0
    while HUB.imu.heading() < targetHeading - WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction < WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800

        lerror = (targetHeading - HUB.imu.heading())*1.1
        sannisLivisa.lookDir(lerror, asyncBool=False, speed=1000)
        sannisLivisa.move(-MAXSPEED, correction)

        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > 150:
            pixelWeight = linearMap(tempData[2], 150, 1500, 0.2, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    sannisLivisa.driveUntilStalled(-100, 500, 600, heading=90)
    
    beep()
    sannisLivisa.lookDir(0)
    log("Error in walling:", abs(HUB.imu.heading() - 90))
    error = HUB.imu.heading() - 90
    if error > WALLING_ERROR_TOLERANCE:
        turntimer = StopWatch()
        turntimer.reset()
        turntimer.pause()
        beep(700)
        direc = 40 if error > 0 else -40
        turntimer.resume()
        while turntimer.time() < TURNDURATION:
            sannisLivisa.move(-600, direc)
        turntimer.reset()
        turntimer.pause()
        # sannisLivisa.eBrake(200)


    tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
    if tempData != (0, 0, 0) and tempColor != "None":
        if tempColor == "Green":
            greenDetections += 2
        else:
            redDetections += 2

    sannisLivisa.driveMotor.reset_angle(0)
    sannisLivisa.eBrake(500)
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
    while HUB.imu.heading() < targetHeading - WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction < WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800

        sannisLivisa.move(-MAXSPEED, correction)

    sannisLivisa.driveUntilStalled(-80, 500, 600, heading=90)
    beep()
    log("Error in walling:", abs(HUB.imu.heading() - 90))

    error = HUB.imu.heading() - 90
    if error > WALLING_ERROR_TOLERANCE:
        turntimer = StopWatch()
        turntimer.reset()
        turntimer.pause()
        beep(700)
        direc = 40 if error > 0 else -40
        turntimer.resume()
        while turntimer.time() < TURNDURATION:
            sannisLivisa.move(-600, direc)
        turntimer.reset()
        turntimer.pause()
        sannisLivisa.eBrake(200)

    sannisLivisa.drive(-50, 500, 600)
    sannisLivisa.driveMotor.reset_angle(0)
    sannisLivisa.eBrake(300)
    HUB.imu.reset_heading(0)

#########################################
# --            Lap Logic            -- #
#########################################

def recordQuarterLap(sannisLivisa: FE, currentLap=0.25):
    # sannisLivisa.center()
    pillarColor = wallingTurnAndRecord(sannisLivisa)
    
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
        pillarColor = scanOnce(sannisLivisa,  50, -30, minThreshold=400)
    else:
        pillarColor = scanOnce(sannisLivisa, 30, -50, minThreshold=400)

    log("2.", pillarColor)

    try:
        if currentLapRecord[0] != pillarColor:
            currentLapRecord.append((pillarColor))
    except:
        currentLapRecord.append((pillarColor))

    sannisLivisa.center()

    if pillarColor == "Green" and prevTurn != "LEFT":
        greenLast(sannisLivisa)

    elif pillarColor == "Red" and prevTurn != "RIGHT":
        redLast(sannisLivisa)

    else:
        beep()
        log(currentLapRecord)
        sannisLivisa.lookDir(90, asyncBool=False)
        sannisLivisa.drive(1050, 500, 600, heading=0)

        if currentLapRecord[0] == "Green":
            greenEnding(sannisLivisa)
        else:
            redEnding(sannisLivisa)

    sannisLivisa.driveUntilStalled(100, 500, 600, heading=0)

    currentLapRecord = [e for e in currentLapRecord if e != 'None']
    log(currentLapRecord)

    sannisLivisa.record(str(currentLap)[1::], currentLapRecord)



def runRecord(sannisLivisa: FE, currentLap):
    wallingTurn(sannisLivisa)
    beep()
    formattedCurrent = str(currentLap)[1::]
    currentObstacles = sannisLivisa.remember(formattedCurrent)

    parking = formattedCurrent == PARKINGLAP
    log(f"Lap {currentLap} Obstacles:", currentObstacles)

    if list(set(currentObstacles)) == GREEN:
        greenOnly(sannisLivisa, parking)

    elif list(set(currentObstacles)) == RED:
        redOnly(sannisLivisa)

    elif currentObstacles == GREEN + RED:
        greenRed(sannisLivisa, True, parking)

    elif currentObstacles ==  RED + GREEN:
        redGreen(sannisLivisa, True, parking)
    
    sannisLivisa.driveUntilStalled(100, 500, 600, heading=0)

def runRecordParking(sannisLivisa: FE):
    wallingTurn(sannisLivisa)
    beep(700, 100)

    currentObstacles = sannisLivisa.remember(".0")
    log(f"Lap Final Obstacles:", currentObstacles)

    if currentObstacles[0] == "Green":
        greenParking(sannisLivisa)
    else:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.turn(500, -90)
        sannisLivisa.driveUntilStalled(400, 500, 600, heading=-90)

def Clockwise(sannisLivisa: FE):
    sannisLivisa.lookDir(-30)
    details=[]
    pillarColor, data = sannisLivisa.determineTrafficSignBlob()
    if pillarColor == 'None' or data[2] < 600:
        pillarColor, data, details = scanList(sannisLivisa, 30, -85, delayTime=5, minThreshold=570)
    else:
        details = [[pillarColor, data, -30]]

    log("First Detection:", pillarColor, data, details)

    sannisLivisa.record(".0", [i[0] for i in details])
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

    sannisLivisa.driveUntilStalled(150, 500, 600, heading=-90)
    HUB.imu.reset_heading(0)

    currentLap = 0
    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, currentLap)
        
    for i in range(8):
        currentLap += 0.25
        runRecord(sannisLivisa, currentLap)

    runRecordParking(sannisLivisa)

def checkParking(sannisLivisa: FE):
    sannisLivisa.record(".0", ["Red"])
    runRecordParking(sannisLivisa)


if __name__ == "__main__":
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.C, Port.D, Port.F)
    # Clockwise(san1nisLivisa)
    checkParking(sannisLivisa)
