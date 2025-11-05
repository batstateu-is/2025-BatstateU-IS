from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from dissociating import *
from pybricks.tools import wait, StopWatch
printInfo()

HUB.imu.reset_heading(0)

# == FLAGS
DEFAULT = "Green"
PARALLEL = True

# == Consts
MAXSPEED = 640
WALLING_KP = 2.85
MAXLOOK = -63
PARKINGLAP = ".0"
WALLINGREVERSEANGLE = -49
WALLING_ANGLE_RIGHT = 45
WALLING_ANGLE_LEFT  = -70
WALLING_TURN_TOLERANCE = 2

WALLING_ERROR_TOLERANCE = 9.5

# in ms
TURNDURATION = 600
SCANDURATION = 100
RED = ['Red']
GREEN = ['Green']

# Clcokwise

#########################################
# --        Walling for ending       -- #
#########################################
def greenEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.drive(100, 600, 700, heading=startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.turn(550, startingAngle)
    sannisLivisa.drive(200, 700, 600, heading=startingAngle)

def redEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.drive(80, 500, 600, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.drive(50, 500, 600, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(550, startingAngle)
    sannisLivisa.drive(80, 600, 500, heading=startingAngle)

#########################################
# --      Exiting Parking Area       -- #
#########################################
def greenStart(sannisLivisa: FE):
    sannisLivisa.drive(40, 500, 800, heading=0)
    sannisLivisa.turn(580, -90)
    sannisLivisa.drive(50, 500, 600, heading=-90)
    sannisLivisa.drive(1250, 500, 600, heading=-96)
    
def redStart(sannisLivisa: FE):
    sannisLivisa.drive(470, 500, 700, heading=0)
    sannisLivisa.turn(480, -90)
    sannisLivisa.drive(500, 500, 700, heading=-90)
    redEnding(sannisLivisa, -90)

#########################################
# --             Parking             -- #
#########################################

def greenParking(sannisLivisa: FE):
    greenFirst(sannisLivisa, parking=True, brake=False)

    if PARALLEL:
        sannisLivisa.drive(630, 500, 600, heading=0)
        sannisLivisa.turn(500, -90)
        sannisLivisa.driveUntilStalled(120, 700, 800, heading=-90)
        sannisLivisa.eBrake(100)
        sharedParking(sannisLivisa)
    else:
        sannisLivisa.eBrake(200)
        sannisLivisa.drive(-200, 400, 600)
        sannisLivisa.turn(300, -50)
        sannisLivisa.eBrake(200)

def redParking(sannisLivisa: FE):
    if PARALLEL:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.drive(420, 500, 600, heading=0)
        sannisLivisa.turn(500, -84)
        sannisLivisa.driveUntilStalled(320, 500, 600, heading=-84)
        sannisLivisa.eBrake(100)
        sharedParking(sannisLivisa)
    else:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.drive(-187, 200, 600, heading=0)
        sannisLivisa.turn(500, -90)
        # sannisLivisa.drive(80, 500, 600, heading=-90)
        sannisLivisa.driveUntilStalled(400, 600, 300, heading=-90)

#########################################
# -- First Obstacle (If there is ONE) --#
#########################################
def greenFirst(sannisLivisa: FE, parking=False, brake=True):
    if not parking:
        sannisLivisa.drive(270, 500, 600, heading=0)
        sannisLivisa.turn(520, -52)
        sannisLivisa.drive(215, 500, 600, heading=-52)
        sannisLivisa.turn(430, 0)
        sannisLivisa.drive(250, 600, 400, heading=0)

        sannisLivisa.center()
    else:
        sannisLivisa.turn(480, -28)
        sannisLivisa.drive(110, 500, 600, heading=-28)
        sannisLivisa.turn(250, 0)
        sannisLivisa.drive(600, 480, 600, heading=0)

    if brake:
        sannisLivisa.eBrake(200)

def redFirst(sannisLivisa: FE, parking=False, brake=True):
    sannisLivisa.drive(250, 500, 950, heading=0)#, decelerate=True)
    sannisLivisa.turn(580, 42)
    sannisLivisa.drive(200, 400, 700, heading=42, decelerate=True)
    sannisLivisa.turnDriveAndCheckIfSnag(510, 0, 600, 510, 290)

    if brake:
        sannisLivisa.eBrake(200)

#########################################
# -- Next Obstacle (If there is ONE) -- #
#########################################
def greenLast(sannisLivisa: FE, recording=False, parking=False):
    if recording:
        sannisLivisa.lookDir(90, asyncBool=False)
    if not parking:
        sannisLivisa.turn(480, -54)
        sannisLivisa.drive(550, 500, 800, heading=-54, decelerate=True)
        sannisLivisa.turn(480, -7)
        sannisLivisa.drive(250, 500, 700, heading=0)
    else:
        sannisLivisa.drive(90, 500, 600, heading=0)
        sannisLivisa.turn(480, -47)
        sannisLivisa.drive(780, 600, 700, heading=-47, decelerate=True)
        sannisLivisa.turn(480, 0)

    greenEnding(sannisLivisa)

def redLast(sannisLivisa: FE, recording=False, parking=False):
    if recording:
        sannisLivisa.lookDir(90, asyncBool=False)
        
    if not parking:
        # Not parking
        sannisLivisa.turn(460, 52)
        sannisLivisa.drive(600, 500, 800, heading=52, decelerate=True)
        sannisLivisa.turn(460, 0)
        sannisLivisa.drive(140, 500, 600, heading=0)
    else:
        sannisLivisa.turn(460, 45)
        sannisLivisa.drive(500, 500, 600, heading=45)
        sannisLivisa.turn(460, 0)
        sannisLivisa.drive(550, 500, 600, heading=0)
    redEnding(sannisLivisa)

#########################################
# --      Pre Recorded Movements     -- #
#########################################
def greenOnly(sannisLivisa: FE, parking):
    greenFirst(sannisLivisa, parking, brake=False)


    if not parking:
        sannisLivisa.drive(1050, 500, 900, heading=0)
        greenEnding(sannisLivisa)
    else:
        sannisLivisa.drive(1050, 500, 900, heading=0)
        sannisLivisa.drive(900, 900, 1000, heading=0)
        # sannisLivisa.drive(400, 500, 600, heading=0)

def redOnly(sannisLivisa: FE):
    redFirst(sannisLivisa, brake=False)
    sannisLivisa.drive(1050, 550, 800, heading=0)

    redEnding(sannisLivisa)


def greenRed(sannisLivisa: FE, recording=True, parking=False):
    greenFirst(sannisLivisa, parking, brake=False)
    redLast(sannisLivisa, recording, parking)

def redGreen(sannisLivisa: FE, recording=True, parking=False):
    redFirst(sannisLivisa, brake=False)
    greenLast(sannisLivisa, recording, parking)

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
        greenLast(sannisLivisa, recording=True)

    elif pillarColor == "Red" and prevTurn != "RIGHT":
        redLast(sannisLivisa, recording=True)

    else:
        beep()
        sannisLivisa.lookDir(90, asyncBool=False)
        sannisLivisa.drive(1150, 500, 900, heading=0, decelerate=True)

        if currentLapRecord[0] == "Green":
            greenEnding(sannisLivisa)
        else:
            redEnding(sannisLivisa)

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
        greenRed(sannisLivisa, False, parking)

    elif currentObstacles ==  RED + GREEN:
        redGreen(sannisLivisa, False, parking)
    
    sannisLivisa.driveUntilStalled(150, 600, 300, heading=0)
    # sannisLivisa.drive(50, 500, 600, heading=0)
    # sannisLivisa.eBrake(100)

def runRecordParking(sannisLivisa: FE):
    wallingTurn(sannisLivisa)
    beep(700, 100)

    currentObstacles = sannisLivisa.remember(".0")
    log(f"Lap Final Obstacles:", currentObstacles)

    if currentObstacles[0] == "Green":
        greenParking(sannisLivisa)
    else:
        redParking(sannisLivisa)

def Clockwise(sannisLivisa: FE):
    sannisLivisa.lookDir(-30)
    details=[]
    pillarColor, data = sannisLivisa.determineTrafficSignBlob()
    if pillarColor == 'None' or data[2] < 600:
        pillarColor, data, details = scanList(sannisLivisa, 30, -85, delayTime=5, minThreshold=270)
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

    currentLap = 0

    detections = sannisLivisa.scanUntilStallled(100, 600, 400, 90, heading=-90)
    HUB.imu.reset_heading(0)

    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, detections, currentLap)
        detections = sannisLivisa.scanUntilStallled(80, 600, 400, 90, heading=0)
        
    for i in range(8):
        currentLap += 0.25
        runRecord(sannisLivisa, currentLap)

    runRecordParking(sannisLivisa)

def checkParking(sannisLivisa: FE, color):
    sannisLivisa.record(".0", color)
    runRecordParking(sannisLivisa)


if __name__ == "__main__":
    sannisLivisa = FE(Port.A, Port.B, Port.C, Port.F, Port.D, Port.E, camEnabled=True)
    # Clockwise(san1nisLivisa)
    wallingTurn(sannisLivisa)
    # checkParking(sannisLivisa, RED)
