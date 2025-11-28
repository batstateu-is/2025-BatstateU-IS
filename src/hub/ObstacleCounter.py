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
MAXSPEED = 700
MAXLOOK = -63
PARKINGLAP = ".0"
WALLINGREVERSEANGLE = 42


WALLING_KP = 4.55
WALLING_ANGLE_RIGHT = 57
WALLING_ANGLE_LEFT  = -60
WALLING_TURN_TOLERANCE = 6
WALLING_ERROR_TOLERANCE = 9.5

TURNDURATION = 1200
SCANDURATION = 900
RED = ['Red']
GREEN = ['Green']

#########################################
# --        Walling for ending       -- #
#########################################
def greenEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.turn(550, startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.drive(100, 550, 600, heading=startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.turn(580, startingAngle)
    sannisLivisa.drive(300, 600, 480, heading=startingAngle)

def redEnding(sannisLivisa: FE, startingAngle=0):
    sannisLivisa.turn(580, startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.drive(50, 500, 400, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(580, startingAngle)
    sannisLivisa.drive(380, 600, 480, heading=startingAngle)
    
#########################################
# --      Exiting Parking Area       -- #
#########################################
def greenStart(sannisLivisa: FE):
    sannisLivisa.drive(500, 500, 600, heading=-6)
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
        # sannisLivisa.drive(80, 400, 500, heading=0)
        sannisLivisa.turn(400, 90)
        # sannisLivisa.drive(40, 500, 600, heading=90)

        # sannisLivisa.turn(400, 112)
        # sannisLivisa.drive(80, 400, 500, heading=112)
        # sannisLivisa.turn(400, 90)
        sannisLivisa.driveUntilStalled(500, 400, 500, heading=90)
        log(f"Distance to Parking: {sannisLivisa.getDistance(LEFT)}")
        sharedParking(sannisLivisa)
    else:
        greenFirst(sannisLivisa, False)
        sannisLivisa.drive(440, 500, 600, heading=0)
        sannisLivisa.turn(430, 90)
        sannisLivisa.driveUntilStalled(170, 500, 600, heading=90)

def redParking(sannisLivisa: FE):
    if PARALLEL:
        redFirst(sannisLivisa, True, False)
        sannisLivisa.drive(120, 600, 400, heading=0, stopBool=True)
        sannisLivisa.turn(400, 60)
        # sannisLivisa.turn(500, 70, True)
        sannisLivisa.turn(500, 74, True)
        sannisLivisa.driveUntilStalled(210, 500, 600, heading=90)
        sannisLivisa.eBrake(50)
        log(f"Distance to Parking: {sannisLivisa.getDistance(LEFT)}")
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
def greenFirst(sannisLivisa: FE, parking=False, brake=True, currentHeading=0):
    # if not parking:
    sannisLivisa.drive(200, 500, 600, heading=currentHeading+0)
    sannisLivisa.turn(580, currentHeading-48)
    sannisLivisa.drive(175, 500, 600, heading=currentHeading-48, decelerate=True)
    sannisLivisa.turnDriveAndCheckIfSnag(540, currentHeading+0, 600, 580, 290)

    if brake:
        sannisLivisa.eBrake(200)

def redFirst(sannisLivisa: FE, parking=False, brake=True, currentHeading=0):
    # log("Red First:",parking)
    if not parking:
        sannisLivisa.drive(200, 500, 600, currentHeading+0)
        sannisLivisa.turn(580, currentHeading+44)
        sannisLivisa.drive(320, 500, 600, heading=currentHeading+44)
        sannisLivisa.turn(520, currentHeading+0)
        sannisLivisa.drive(200, 600, 500, heading=currentHeading+0)
    else:
        sannisLivisa.drive(250, 500, 700, heading=currentHeading+0)
        sannisLivisa.turn(480, currentHeading+35)
        sannisLivisa.drive(90, 500, 600, heading=currentHeading+35)
        sannisLivisa.turn(480, currentHeading+0)
        sannisLivisa.drive(280, 600, 500, heading=currentHeading+0)
        

    if brake:
        sannisLivisa.eBrake(200)

#########################################
# -- Next Obstacle (If there is ONE) -- #
#########################################
def greenLast(sannisLivisa: FE, recording=False, parking=False, ending=True, currentHeading=0):
    if recording:
        sannisLivisa.lookDir(-90, asyncBool=False)
    if not parking:
        sannisLivisa.turn(500, currentHeading-55)
        sannisLivisa.drive(585, 500, 800, heading=currentHeading-55, decelerate=True)
        sannisLivisa.turn(580, currentHeading-2)
        sannisLivisa.drive(310, 500, 700, heading=currentHeading+0)
    else:
        sannisLivisa.turn(480, currentHeading-53)
        sannisLivisa.drive(420, 600, 700, heading=currentHeading-53, decelerate=True)
        sannisLivisa.turn(480, currentHeading+0)
        sannisLivisa.drive(500, 500, 600, heading=currentHeading+0)

    if ending:
        greenEnding(sannisLivisa, currentHeading)

def redLast(sannisLivisa: FE, recording=False, parking=False, ending=True, currentHeading=0):
    if recording:
        sannisLivisa.lookDir(-90, asyncBool=False)
        
    if not parking:
        sannisLivisa.turn(510, currentHeading+47)
        sannisLivisa.drive(750, 500, 800, heading=currentHeading+47, decelerate=True)
        sannisLivisa.turn(520, currentHeading+0)
        sannisLivisa.drive(100, 500, 800, heading=currentHeading+0)
        if ending:
            redEnding(sannisLivisa, currentHeading)
    else:
        sannisLivisa.turn(450, currentHeading+44)
        sannisLivisa.drive(430, 600, 500, heading=currentHeading+44)
        sannisLivisa.turn(470, currentHeading+0)
        sannisLivisa.drive(800, 500, 600, heading=currentHeading+0)
    

#########################################
# --      Pre Recorded Movements     -- #
#########################################
def greenOnly(sannisLivisa: FE, parking, currentHeading=0, ending=True):
    greenFirst(sannisLivisa, parking, brake=False, currentHeading=currentHeading)
    sannisLivisa.drive(1250, 500, 950, currentHeading+0, decelerate=True)

    if ending:
        greenEnding(sannisLivisa, currentHeading)

def redOnly(sannisLivisa: FE, parkingBool, currentHeading=0, ending=True):
    redFirst(sannisLivisa, parking=parkingBool, brake=False, currentHeading=currentHeading)
    sannisLivisa.drive(1150, 600, 800, currentHeading+0, decelerate=True)
    if not parkingBool and ending:
        redEnding(sannisLivisa, currentHeading)
    else:
        sannisLivisa.drive(1100, 500, 950, heading=currentHeading, decelerate=True)



def greenRed(sannisLivisa: FE, recording=True, parking=False, currentHeading=0, ending=True):
    greenFirst(sannisLivisa, parking, brake=False)
    redLast(sannisLivisa, recording, parking, currentHeading=currentHeading, ending=ending)

def redGreen(sannisLivisa: FE, recording=True, parking=False, currentHeading=0, ending=True):
    redFirst(sannisLivisa, parking, brake=False)
    greenLast(sannisLivisa, recording, parking, ending=ending, currentHeading=currentHeading)

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
        speed = linearMap(error, start, 0, MAXSPEED//1.5, MAXSPEED // 2)
        sannisLivisa.move(-speed, correction)

        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.6, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

    # sannisLivisa.lookDir(90, asyncBool=False)
    # sannisLivisa.driveUntilProximity(-400, 80, heading=-90, lookHeading=targetHeading, selection=BACK)
    sannisLivisa.driveUntilStalled(-200, MAXSPEED//2, MAXSPEED//3, heading=-90)
    # temp = sannisLivisa.scanUntilStallled(-30, 400, 500, 0, heading=targetHeading)
    temp = [0, 0]
    greenDetections += temp[0]
    redDetections += temp[1]
    beep()

    scanTimer = StopWatch()
    scanTimer.reset()
    scanTimer.resume()
    while scanTimer.time() < SCANDURATION:
        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD-100:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD-100, 4000, 0.25, 1.0)
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

def wallingTurn(sannisLivisa: FE, currentHeading=0):
    sannisLivisa.lookDir(0, asyncBool=False)
    targetHeading = -90
    start = HUB.imu.heading() - targetHeading
    while HUB.imu.heading() > targetHeading + WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        speed = linearMap(error, start, 0, MAXSPEED//1.5, MAXSPEED // 2)
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction > WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        sannisLivisa.move(-speed, correction)

    beep()
    log("Error in walling:", abs(HUB.imu.heading() - 90))
    sannisLivisa.eBrake(10)
    # checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 80, 600, 90, TURNDURATION, 40)
    sannisLivisa.driveUntilStalled(-300, MAXSPEED//2, MAXSPEED//3, heading=targetHeading)
    sannisLivisa.eBrake(10)

    # sannisLivisa.drive(-50, 500, 600)
    # sannisLivisa.driveMotor.reset_angle(0)
    # sannisLivisa.eBrake(50)
    HUB.imu.reset_heading(0)

#########################################
# --            Lap Logic            -- #
#########################################

def recordQuarterLap(sannisLivisa: FE, initalDetection: tuple, currentLap=0.25):
    # sannisLivisa.center()
    pillarColor = wallingTurnAndRecord(sannisLivisa, initalDetection)

    formattedCurrent = str(currentLap)[1::]

    currentLapRecord = []
    prevTurn = ""

    if formattedCurrent == ".0":
        parking = True
    else:
        parking = False


    log("\n" + str(currentLap))
    log("1.", pillarColor)
    
    if pillarColor == "Green":
        greenFirst(sannisLivisa, brake=True, parking=parking)
        prevTurn = "LEFT"
    elif pillarColor == "Red":
        redFirst(sannisLivisa, brake=True, parking=parking)
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
        pillarColor = scanOnce(sannisLivisa, -2, -80, minThreshold=450)

    log("2.", pillarColor)

    try:
        if currentLapRecord[0] != pillarColor:
            currentLapRecord.append((pillarColor))
    except:
        currentLapRecord.append((pillarColor))

    sannisLivisa.center()

    if pillarColor == "Green" and prevTurn != "LEFT":
        greenLast(sannisLivisa, True, parking= parking)

    elif pillarColor == "Red" and prevTurn != "RIGHT":
        redLast(sannisLivisa, True, parking= parking)

    else:
        beep()
        log(currentLapRecord)
        sannisLivisa.lookDir(-90, asyncBool=False)
        sannisLivisa.drive(1200, 500, 900, heading=0, decelerate=True)

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
    
    sannisLivisa.driveUntilStalled(150, 500, 600, heading=0)
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
    sannisLivisa.lookDir(-29)
    details=[]
    redCount = 0
    greenCount = 0
    scanDur2 = 800
    timer = StopWatch()
    timer.reset()
    timer.resume()
    pilarColor, data = "None", (0, 0, 0)
    while timer.time() < scanDur2:

        pillarColor, data = sannisLivisa.determineTrafficSignBlob()
        if data[2] > 600:
            if pillarColor  =="Green":
                greenCount += 1
            elif pillarColor == "Red":
                redCount += 1
    print("G:",greenCount,"R:",redCount)
    if redCount > 0 or greenCount > 0:
        if redCount > greenCount:
            pillarColor = "Red"
        else:
            pillarColor = "Green"

    print("INI:",pillarColor,data)
    if pillarColor == 'None' or (greenCount < 4 and redCount < 4):
        # pillarColor, data, details = scanList(sannisLivisa, -90, 45, delayTime=10, minThreshold=270)
        # pillarColor, data, angle = details[-1]
        parkingLap = []
        pillarColor = scanOnce(sannisLivisa,  -85, 0, delayTime=15, minThreshold=270)
        parkingLap.append(pillarColor)
        pillarColor = scanOnce(sannisLivisa, 0, 90, delayTime=15, minThreshold=270)
        parkingLap.append(pillarColor)

        sannisLivisa.record(".0", parkingLap)


    else:
        details = [[pillarColor, data, -30]]
        sannisLivisa.record(".0", [pillarColor])

    log("First Detection:", pillarColor, data, details)
    log("First Lap:", pillarColor, data, details)

    # sannisLivisa.record(".0", [i[0] for i in details])
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

    detections = sannisLivisa.scanUntilStallled(100, sannisLivisa.speed(), 500, -90, heading=90)
    HUB.imu.reset_heading(0)

    for i in range(3):
        currentLap += 0.25
        recordQuarterLap(sannisLivisa, detections, currentLap)
        detections = sannisLivisa.scanUntilStallled(130, sannisLivisa.speed(), 500, -90, heading=0)
        sannisLivisa.eBrake(10)
        HUB.imu.reset_heading(0)
        
    for i in range(8):
        currentLap += 0.25
        beep(700)
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
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.F, Port.D, Port.C, camEnabled=True)
    # sannisLivisa.record(".0",RED)
    # Counter(sannisLivisa)
    checkParking(sannisLivisa, GREEN)
