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
MAXLOOK = -63
PARKINGLAP = ".0"
WALLINGREVERSEANGLE = 42


WALLING_KP = 2.55
WALLING_ANGLE_RIGHT = 55
WALLING_ANGLE_LEFT  = -60
WALLING_TURN_TOLERANCE = 4
WALLING_ERROR_TOLERANCE = 9.5

TURNDURATION = 1200
SCANDURATION = 100
RED = ['Red']
GREEN = ['Green']

#########################################
# --        Walling for ending       -- #
#########################################
def greenEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.drive(100, 600, 700, heading=startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.turn(550, startingAngle)
    sannisLivisa.drive(150, 600, 600, heading=startingAngle)

def redEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.drive(80, 600, 700, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(550, startingAngle)
    sannisLivisa.drive(150, 600, 500, heading=startingAngle)
    
#########################################
# --      Exiting Parking Area       -- #
#########################################
def greenStart(sannisLivisa: FE):
    sannisLivisa.drive(450, 500, 600, heading=-4)
    sannisLivisa.turn(500, 90)
    sannisLivisa.drive(20, 500, 600, heading=90)
    sannisLivisa.turn(580, 90+WALLING_ANGLE_RIGHT+5)
    sannisLivisa.drive(100, 500, 700, heading=90+WALLING_ANGLE_RIGHT+5)
    sannisLivisa.turn(550, 90)
    sannisLivisa.drive(200, 500, 600, heading=90)
    
def redStart(sannisLivisa: FE):
    sannisLivisa.drive(30, 500, 600, heading=0)
    sannisLivisa.turn(400, 90)
    sannisLivisa.drive(750, 500, 750, heading=90, decelerate=True)

#########################################
# --             Parking             -- #
#########################################
def greenParking(sannisLivisa: FE):
    if PARALLEL:
        greenFirst(sannisLivisa)
        sannisLivisa.drive(-150, 400, 500, heading=0)
        sannisLivisa.turn(400, 90)
        # sannisLivisa.drive(40, 500, 600, heading=90)

        # sannisLivisa.turn(400, 112)
        # sannisLivisa.drive(80, 400, 500, heading=112)
        # sannisLivisa.turn(400, 90)
        sannisLivisa.driveUntilStalled(500, 400, 500, heading=90)
        sharedParking(sannisLivisa)
    else:
        greenFirst(sannisLivisa, False)
        sannisLivisa.drive(440, 500, 600, heading=0)
        sannisLivisa.turn(430, 90)
        sannisLivisa.driveUntilStalled(170, 500, 600, heading=90)

def redParking(sannisLivisa: FE):
    if PARALLEL:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.turn(400, 60)
        sannisLivisa.turn(500, 100, True)
        sannisLivisa.driveUntilStalled(250, 500, 600, heading=-90)
        sannisLivisa.eBrake(200)
        sharedParking(sannisLivisa)
    else:    
        redFirst(sannisLivisa, True, False)
        sannisLivisa.drive(720, 500, 600, heading=-1)
        # sannisLivisa.drive(120, 500, 600, heading=-1)
        sannisLivisa.turn(500, 40)
        sannisLivisa.eBrake(200)



#########################################
# -- First Obstacle (If there is ONE) --#
#########################################
def greenFirst(sannisLivisa: FE, parking=False, brake=True):
    # if not parking:
    sannisLivisa.drive(200, 500, 600, heading=0)
    sannisLivisa.turn(580, -45)
    sannisLivisa.drive(130, 400, 600, heading=-45)
    sannisLivisa.turnDriveAndCheckIfSnag(540, 0, 600, 520, 390)

    if brake:
        sannisLivisa.eBrake(200)

def redFirst(sannisLivisa: FE, parking=False, brake=True):
    # log("Red First:",parking)
    if not parking:
        sannisLivisa.drive(200, 500, 600, heading=0)
        sannisLivisa.turn(520, 44)
        sannisLivisa.drive(350, 500, 600, heading=44)
        sannisLivisa.turn(500, 0)
        sannisLivisa.drive(150, 600, 400, heading=0)
    else:
        sannisLivisa.drive(280, 500, 700, heading=0)
        sannisLivisa.turn(480, 35)
        sannisLivisa.drive(120, 500, 600, heading=35)
        sannisLivisa.turn(480, 0)
        sannisLivisa.drive(280, 600, 400, heading=0)
        

    if brake:
        sannisLivisa.eBrake(200)

#########################################
# -- Next Obstacle (If there is ONE) -- #
#########################################
def greenLast(sannisLivisa: FE, recording=False, parking=False):
    if recording:
        sannisLivisa.lookDir(-90, asyncBool=False)
    if not parking:
        sannisLivisa.turn(500, -56)
        sannisLivisa.drive(475, 500, 800, heading=-56, decelerate=True)
        sannisLivisa.turn(480, -2)
        sannisLivisa.drive(260, 500, 700, heading=0)
    else:
        sannisLivisa.turn(480, -47)
        sannisLivisa.drive(410, 600, 700, heading=-47, decelerate=True)
        sannisLivisa.turn(480, 0)
        sannisLivisa.drive(400, 500, 600, heading=0)

    greenEnding(sannisLivisa)

def redLast(sannisLivisa: FE, recording=False, parking=False):
    if recording:
        sannisLivisa.lookDir(-90, asyncBool=False)
        
    if not parking:
        sannisLivisa.turn(480, 47)
        sannisLivisa.drive(750, 500, 800, heading=47, decelerate=True)
        sannisLivisa.turn(480, 0)
        sannisLivisa.drive(100, 500, 800, heading=0)
        redEnding(sannisLivisa)
    else:
        sannisLivisa.turn(450, 44)
        sannisLivisa.drive(390, 600, 400, heading=44)
        sannisLivisa.turn(470, 0)
        sannisLivisa.drive(950, 500, 600, heading=0)
    

#########################################
# --      Pre Recorded Movements     -- #
#########################################
def greenOnly(sannisLivisa: FE, parking):
    greenFirst(sannisLivisa, parking, brake=False)
    sannisLivisa.drive(1050, 500, 950, heading=0, decelerate=True)
    greenEnding(sannisLivisa)

def redOnly(sannisLivisa: FE, parkingBool):
    redFirst(sannisLivisa, parking=parkingBool, brake=False)
    sannisLivisa.drive(1100, 600, 800, heading=0, decelerate=True)
    if not parkingBool:
        redEnding(sannisLivisa)
    else:
        sannisLivisa.drive(800, 500, 950, heading=0, decelerate=True)



def greenRed(sannisLivisa: FE, recording=True, parking=False):
    greenFirst(sannisLivisa, parking, brake=False)
    redLast(sannisLivisa, recording, parking)

def redGreen(sannisLivisa: FE, recording=True, parking=False):
    redFirst(sannisLivisa, parking, brake=False)
    greenLast(sannisLivisa, recording, parking)

def wallingTurnAndRecord(sannisLivisa: FE, initialDetection: tuple):
    pillarColor = "None"
    targetHeading = -90
    # Turn and record
    greenDetections, redDetections = initialDetection
    start = HUB.imu.heading() - targetHeading

    while HUB.imu.heading() > targetHeading + WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction > WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        lerror = (targetHeading - HUB.imu.heading())*1.1

        sannisLivisa.lookDir(lerror, asyncBool=False, speed=1000)
        speed = linearMap(error, start, 0, MAXSPEED, MAXSPEED // 1.6)
        sannisLivisa.move(-speed, correction)

        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    sannisLivisa.driveUntilStalled(-40, MAXSPEED//1.1, MAXSPEED//1.5, heading=-90)
    sannisLivisa.eBrake(30)
    sannisLivisa.lookDir(0)
    # -- Correct if not flush with wall -- #
    checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 50, 600, -90, TURNDURATION, -40)
    # sannisLivisa.driveUntilStalled(-10, MAXSPEED//1.1, MAXSPEED//1.5, heading=-90)
    beep()

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
    targetHeading = -90
    start = HUB.imu.heading() - targetHeading
    while HUB.imu.heading() > targetHeading + WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        speed = linearMap(error, start, 0, MAXSPEED, MAXSPEED // 1.5)
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction > WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        sannisLivisa.move(-speed, correction)

    sannisLivisa.driveUntilStalled(-80, MAXSPEED//1.5, MAXSPEED//2, heading=-90)
    beep()
    log("Error in walling:", abs(HUB.imu.heading() - 90))
    sannisLivisa.eBrake(10)
    checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 50, 600, -90, TURNDURATION, -40)
    # sannisLivisa.driveUntilStalled(-10, MAXSPEED//1.5, MAXSPEED//2, heading=-90)
    sannisLivisa.eBrake(10)

    # sannisLivisa.driveMotor.reset_angle(0)
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

    log("\n" + str(currentLap))
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
        pillarColor = scanOnce(sannisLivisa,  2, 70, minThreshold=450)
    else:
        pillarColor = scanOnce(sannisLivisa, -10, -80, minThreshold=450)

    log("2.", pillarColor)

    try:
        if currentLapRecord[0] != pillarColor:
            currentLapRecord.append((pillarColor))
    except:
        currentLapRecord.append((pillarColor))

    sannisLivisa.center()

    if pillarColor == "Green" and prevTurn != "LEFT":
        greenLast(sannisLivisa, True)

    elif pillarColor == "Red" and prevTurn != "RIGHT":
        redLast(sannisLivisa, True)

    else:
        beep()
        log(currentLapRecord)
        sannisLivisa.lookDir(-90, asyncBool=False)
        sannisLivisa.drive(1050, 500, 900, heading=0, decelerate=True)

        if currentLapRecord[0] == "Green":
            greenEnding(sannisLivisa)
        else:
            redEnding(sannisLivisa)


    currentLapRecord = [e for e in currentLapRecord if e != 'None']
    log(currentLapRecord)

    sannisLivisa.record(str(currentLap)[1::], currentLapRecord)

    # sannisLivisa.driveUntilStalled(50, 600, 300, heading=0)
    # sannisLivisa.drive(100, 500, 400, heading=0)
    # sannisLivisa.eBrake(200)



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
        redOnly(sannisLivisa, parking)

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
        
def Counter(sannisLivisa: FE):
    sannisLivisa.lookDir(-28)
    details=[]
    pillarColor, data = sannisLivisa.determineTrafficSignBlob()
    if pillarColor == 'None' or data[2] < 700:
        pillarColor, data, details = scanList(sannisLivisa, -90, 45, delayTime=10, minThreshold=270)
        pillarColor, data, angle = details[-1]
    else:
        details = [[pillarColor, data, -30]]

    log("First Detection:", pillarColor, data, details)

    sannisLivisa.record(".0", [i[0] for i in details])
    sannisLivisa.center()

    sannisLivisa.lookDir(-90, asyncBool=False)

    if pillarColor == "Green":  
        greenStart(sannisLivisa)

    elif pillarColor == "Red":
        redStart(sannisLivisa)        

    else:                
        beep()                        
        if DEFAULT == "Red":
            redStart(sannisLivisa)
        else:
            greenStart(sannisLivisa)

    currentLap = 0

    detections = sannisLivisa.scanUntilStallled(100, 600, 400, -90, heading=90)
    HUB.imu.reset_heading(0)

    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, detections, currentLap)
        detections = sannisLivisa.scanUntilStallled(80, 600, 400, -90, heading=0)
        
    for i in range(8):
        currentLap += 0.25
        runRecord(sannisLivisa, currentLap)

    runRecordParking(sannisLivisa)

def checkParking(sannisLivisa: FE, color):
    sannisLivisa.record(".0",color)
    runRecordParking(sannisLivisa)

def testing(sannisLivisa):
    # while True:
    recordQuarterLap(sannisLivisa)
    runRecord(sannisLivisa, 0.25)


if __name__ == "__main__":
    sannisLivisa = FE(Port.B, Port.A, Port.E, Port.C, Port.D, Port.F)
    # sannisLivisa.record(".0",RED)
    checkParking(sannisLivisa, GREEN)
