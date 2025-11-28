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
MAXSPEED = 650
WALLING_KP = 4.55
MAXLOOK = -63
PARKINGLAP = ".0"
WALLINGREVERSEANGLE = -49
WALLING_ANGLE_RIGHT = 58
WALLING_ANGLE_LEFT  = -70
WALLING_TURN_TOLERANCE = 6.5

WALLING_ERROR_TOLERANCE = 11.5

# REFANGLE = 0

# in ms
TURNDURATION = 600
SCANDURATION = 650
RED = ['Red']
GREEN = ['Green']

# Clcokwise

#########################################
# --        Walling for ending       -- #
#########################################
def greenEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.drive(100, 500, 700, heading=startingAngle+WALLING_ANGLE_RIGHT, decelerate=True)
    sannisLivisa.turn(580, startingAngle)
    sannisLivisa.drive(100, 500, 700, heading=startingAngle, decelerate=True)
    # sannisLivisa.eBrake(10)

def redEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.drive(110, 500, 600, heading=startingAngle)
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.drive(90, 500, 600, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(550, startingAngle)
    sannisLivisa.drive(120, 600, 300, heading=startingAngle)
    # sannisLivisa.eBrake(10)

#########################################
# --      Exiting Parking Area       -- #
#########################################
def greenStart(sannisLivisa: FE):
    HUB.imu.reset_heading(0)
    sannisLivisa.drive(20, 500, 800, heading=0)
    sannisLivisa.turn(480, -94)
    sannisLivisa.drive(50, 500, 600, heading=-92)
    sannisLivisa.drive(1450, 500, 900, heading=-92, decelerate=True)
    # sannisLivisa.drive(350, 700, 350, heading=-90)
    
def redStart(sannisLivisa: FE):
    HUB.imu.reset_heading(0)
    sannisLivisa.drive(480, 500, 700, heading=0)
    sannisLivisa.turn(580, -90)
    sannisLivisa.drive(600, 500, 700, heading=-90)
    redEnding(sannisLivisa, -90)

#########################################
# --             Parking             -- #
#########################################

def greenParking(sannisLivisa: FE, currentHeading=0):
    greenFirst(sannisLivisa, parking=True, brake=False)

    if PARALLEL:
        sannisLivisa.drive(750, 500, 600, heading=0)
        sannisLivisa.turn(400, -70)
        sannisLivisa.turn(600, -90, True)
        sannisLivisa.driveUntilStalled(320, 700, 100, heading=-90)
        sannisLivisa.eBrake(100)
        log(f"Distance to Parking: {sannisLivisa.getDistance(LEFT)}")
        sharedParking(sannisLivisa)
    else:
        sannisLivisa.eBrake(200)
        sannisLivisa.drive(-200, 400, 600)
        sannisLivisa.turn(300, -50)
        sannisLivisa.eBrake(200)

def redParking(sannisLivisa: FE, currentHeading=0):
    if PARALLEL:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.drive(500, 500, 600, heading=0)
        sannisLivisa.turn(500, -90)
        sannisLivisa.driveUntilStalled(320, 600, 300, heading=-90)
        log(f"Distance to Parking: {sannisLivisa.getDistance(LEFT)}")
        sannisLivisa.eBrake(100)
        sharedParking(sannisLivisa)
    else:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.drive(-187, 200, 600, heading=0)
        sannisLivisa.turn(500, -90)
        # sannisLivisa.drive(80, 500, 600, heading=-90)
        sannisLivisa.driveUntilStalled(600, 600, 300, heading=-90)

#########################################
# -- First Obstacle (If there is ONE) --#
#########################################
def greenFirst(sannisLivisa: FE, parking=False, brake=True, currentHeading=0):
    if not parking:
        sannisLivisa.drive(270, 500, 600, heading=currentHeading+0)
        sannisLivisa.turn(580, currentHeading-50)
        sannisLivisa.drive(275, 600, 400, heading=currentHeading-50)
        sannisLivisa.turn(550, currentHeading+0)
        sannisLivisa.drive(250, 600, 400, heading=currentHeading+0)
    else:
        sannisLivisa.turn(480, currentHeading-33)
        sannisLivisa.drive(130, 500, 600, heading=currentHeading-33)
        sannisLivisa.turn(550, currentHeading+0)
        sannisLivisa.drive(600, 480, 600, heading=currentHeading+0)

    if brake:
        sannisLivisa.eBrake(200)

def redFirst(sannisLivisa: FE, parking=False, brake=True, currentHeading=0):
    sannisLivisa.drive(180, 400, 500, heading=currentHeading+0, decelerate=True)
    sannisLivisa.turn(510, currentHeading+45)
    sannisLivisa.drive(240, 500, 700, heading=currentHeading+45, decelerate=True)
    sannisLivisa.turnDriveAndCheckIfSnag(510, currentHeading+0, 600, 510, 330)

    if brake:
        sannisLivisa.eBrake(200)

#########################################
# -- Next Obstacle (If there is ONE) -- #
#########################################
def greenLast(sannisLivisa: FE, recording=False, parking=False, ending=True, currentHeading=0):
    if recording:
        sannisLivisa.lookDir(90, asyncBool=False)
    if not parking:
        sannisLivisa.turn(580, currentHeading-57)
        sannisLivisa.drive(640, 500, 800, heading=currentHeading-57, decelerate=True)
        # sannisLivisa.driveUntilProximity(600, 120, heading=currentHeading-56, lookHeading=currentHeading-90, brake=False, maxDistance=590)
        sannisLivisa.turn(580, currentHeading-2)
        sannisLivisa.drive(300, 500, 700, heading=currentHeading+0)
    else:
        sannisLivisa.drive(90, 500, 600, heading=currentHeading+0)
        sannisLivisa.turn(580, currentHeading-50)
        sannisLivisa.drive(710, 600, 700, heading=currentHeading-50, decelerate=True)
        sannisLivisa.turn(510, currentHeading+0)
        sannisLivisa.drive(200, 600, 700, heading=currentHeading+0, decelerate=True)

    if ending:
       greenEnding(sannisLivisa, startingAngle=currentHeading+0)

def redLast(sannisLivisa: FE, recording=False, parking=False, ending=True, currentHeading=0):
    if recording:
        sannisLivisa.lookDir(90, asyncBool=False)
        
    if not parking:
        # Not parking
        sannisLivisa.turn(580, currentHeading+ 58)
        sannisLivisa.drive(550, 500, 800, heading=currentHeading+58, decelerate=True)
        # sannisLivisa.driveUntilProximity(680, 110, heading=currentHeading+57, lookHeading=currentHeading+90, brake=False, maxDistance=570)
        
        sannisLivisa.turn(520, currentHeading+0)
        sannisLivisa.drive(170, 500, 600, heading=currentHeading+0)
    else:
        sannisLivisa.turn(520, currentHeading+45)
        sannisLivisa.drive(500, 500, 600, heading=currentHeading+45)
        sannisLivisa.turn(460,currentHeading+ 0)
        sannisLivisa.drive(260, 500, 600, heading=currentHeading+0)
    # redEnding(sannisLivisa)

    if ending:
        redEnding(sannisLivisa, startingAngle=currentHeading)

#########################################
# --      Pre Recorded Movements     -- #
#########################################
def greenOnly(sannisLivisa: FE, parking, ending=True, currentHeading=0):
    greenFirst(sannisLivisa, parking, brake=False, currentHeading=currentHeading)


    if not parking:
        sannisLivisa.drive(1100, 700, 900, heading=currentHeading+0)
        beep()
        if ending:
            greenEnding(sannisLivisa, startingAngle=currentHeading)
    else:
        sannisLivisa.drive(1050, 500, 900, heading=currentHeading+0)
        sannisLivisa.drive(900, 900, 1000, heading=currentHeading+0)
        # sannisLivisa.drive(400, 500, 600, heading=0)

    

def redOnly(sannisLivisa: FE, ending=True, currentHeading=0):
    redFirst(sannisLivisa, brake=False, currentHeading=currentHeading)
    sannisLivisa.drive(1050, 550, 800, heading=0)

    if ending:
        redEnding(sannisLivisa, currentHeading)


def greenRed(sannisLivisa: FE, recording=True, parking=False, ending=True, currentHeading=0):
    greenFirst(sannisLivisa, parking, brake=False, currentHeading=currentHeading)
    redLast(sannisLivisa, recording, parking, ending, currentHeading=currentHeading)

def redGreen(sannisLivisa: FE, recording=True, parking=False, ending=True, currentHeading=0):
    redFirst(sannisLivisa, brake=False, currentHeading=currentHeading)
    greenLast(sannisLivisa, recording, parking, ending, currentHeading=currentHeading)

def wallingTurnAndRecord(sannisLivisa: FE, initialDetection: tuple, currentHeading=0):
    pillarColor = "None"
    targetHeading = currentHeading+90
    greenDetections, redDetections = initialDetection
    start = HUB.imu.heading() - targetHeading

    while HUB.imu.heading() < targetHeading - WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction < WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800

        lerror = (targetHeading - HUB.imu.heading())*1.1
        speed = tLinearMap(error, start, 0, MAXSPEED // 1.1, MAXSPEED)

        sannisLivisa.lookDir(lerror, asyncBool=False, speed=1000)
        sannisLivisa.move(-speed, correction)

        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 3700, 0.25, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    beep(600)
    sannisLivisa.driveUntilStalled(-60, MAXSPEED//1.5, MAXSPEED//2, heading=90)
    # sannisLivisa.driveUntilProximity(-500, 50, heading=90, lookHeading=targetHeading, selection=BACK)
    # beep()
    # -- Correct if not flush with wall -- #
    # sannisLivisa.eBrake(30)
    # temp = sannisLivisa.scanUntilStallled(-100, 500, 600, 0, heading=targetHeading)

    # greenDetections += temp[0]
    # redDetections += temp[1]
    beep(900)
    

    scanTimer = StopWatch()
    scanTimer.reset()
    scanTimer.resume()
    while scanTimer.time() < SCANDURATION:
        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 3700, 0.05, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    log("Red:", redDetections, "| Green:", greenDetections)
    sannisLivisa.eBrake(50)
    sannisLivisa.driveMotor.reset_angle(0)
    HUB.imu.reset_heading(0)
    
    if greenDetections > redDetections:
        return "Green"
    elif redDetections > greenDetections:
        return "Red"
    else:
        return "None"

def wallingTurn(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.lookDir(0, asyncBool=False)
    targetHeading = currentHeading+90
    start = HUB.imu.heading() - targetHeading
    
    while HUB.imu.heading() < targetHeading - WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        speed = linearMap(error, start, 0, MAXSPEED, MAXSPEED // 1.1)
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction < WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        sannisLivisa.move(-speed, correction)

    # sannisLivisa.driveUntilStalled(-50, MAXSPEED//2, MAXSPEED//3, heading=90)
    # sannisLivisa.driveUntilProximity(-MAXSPEED//2.5, 40, heading=91, lookHeading=90, selection=BACK)
    # sannisLivisa.driveUntilProximity(-400, 60, heading=targetHeading, lookHeading=targetHeading, selection=BACK)
    sannisLivisa.driveUntilStalled(-190, MAXSPEED//1.5, MAXSPEED//2, heading=targetHeading+0.5)
    beep()
    log("Error in walling:", abs(HUB.imu.heading() - 90))
    sannisLivisa.eBrake(10)

    sannisLivisa.eBrake(10)
    sannisLivisa.driveMotor.reset_angle(0)
    HUB.imu.reset_heading(0)

#########################################
# --            Lap Logic            -- #
#########################################
def recordQuarterLap(sannisLivisa: FE, initalDetection: tuple, currentLap=0.25):
    # sannisLivisa.center()
    pillarColor = wallingTurnAndRecord(sannisLivisa, initalDetection, )
    
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
        pillarColor = scanOnce(sannisLivisa,  70, -15, minThreshold=400)
    else:
        pillarColor = scanOnce(sannisLivisa, -5, -70, minThreshold=400)

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
    
    sannisLivisa.driveUntilStalled(140, sannisLivisa.speed(), 500, heading=0, )
    HUB.imu.reset_heading(0)
    # sannisLivisa.driveUntilProximity(MAXSPEED//4, 30, heading=90, selection=FRONT)
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
    redCount = 0
    greenCount = 0
    scanDur2 = 700
    timer = StopWatch()
    timer.reset()
    timer.resume()
    pilarColor, data = "None", (0, 0, 0)
    while timer.time() < scanDur2:

        pillarColor, data = sannisLivisa.determineTrafficSignBlob()
        if data[2] > 700:
            if pillarColor  =="Green":
                greenCount += 1
            elif pillarColor == "Red":
                redCount += 1

    if redCount > 0 or greenCount > 0:
        if redCount > greenCount:
            pillarColor = "Red"
        else:
            pillarColor = "Green"
            
    print("INI:",pillarColor,data, greenCount, redCount)
    if pillarColor == 'None' or (greenCount < 4 and redCount < 4):

        # pillarColor, data, details = scanList(sannisLivisa, 50, -85, delayTime=5, minThreshold=270)
        parkingLap = []
        pillarColor = scanOnce(sannisLivisa,  70, 5, delayTime=15, minThreshold=270)
        parkingLap.append(pillarColor)
        pillarColor = scanOnce(sannisLivisa, 5, -90, delayTime=15, minThreshold=270)
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

    detections = sannisLivisa.scanUntilStallled(100, sannisLivisa.speed(), 500, 90, heading=-90)
    HUB.imu.reset_heading(0)

    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, detections, currentLap)
        detections = sannisLivisa.scanUntilStallled(150, sannisLivisa.speed(), 500, 90, heading=0)
        sannisLivisa.eBrake(10)
        HUB.imu.reset_heading(0)
        
    for i in range(8):
        currentLap += 0.25
        runRecord(sannisLivisa, currentLap)

    runRecordParking(sannisLivisa)

def checkParking(sannisLivisa: FE, color):
    sannisLivisa.record(".0", color)
    runRecordParking(sannisLivisa)


if __name__ == "__main__":
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.F, Port.D, Port.C, camEnabled=True)
    # Clockwise(sannisLivisa)
    # wallingTurnAndRecord(sannisLivisa, (0, 0))
    # wait(4000)
    # HUB.imu.reset_heading(0)
    # wallingTurn(sannisLivisa)
    checkParking(sannisLivisa, GREEN)
