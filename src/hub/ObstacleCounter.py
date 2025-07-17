from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from dissociating import *
from pybricks.tools import wait, StopWatch

printInfo()

HUB.imu.reset_heading(0)

DEFAULT = "Red"
MAXSPEED = 500
MAXLOOK = -63
PARKINGLAP = ".0"
WALLINGREVERSEANGLE = 44
WALLING_KP = 0.6
WALLING_ANGLE_RIGHT = 45
WALLING_ANGLE_LEFT  = -28
WALLING_TURN_TOLERANCE = 12
WALLING_ERROR_TOLERANCE = 4.5
TURNDURATION = 1200
RED = ['Red']
GREEN = ['Green']

#########################################
# --        Walling for ending       -- #
#########################################
def greenEnding(sannisLivisa: FE, startingAngle=0):

    sannisLivisa.turn(400, startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.drive(200, 500, 600, heading=startingAngle+WALLING_ANGLE_RIGHT)
    sannisLivisa.turn(450, startingAngle)
    sannisLivisa.drive(250, 500, 600, heading=startingAngle)

def redEnding(sannisLivisa: FE, startingAngle=0):
    # sannisLivisa.drive(200, 500, 600, heading=startingAngle)
    sannisLivisa.turn(400, startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.drive(450, 500, 600, heading=startingAngle+WALLING_ANGLE_LEFT)
    sannisLivisa.turn(400, startingAngle)
    sannisLivisa.drive(100, 500, 600, heading=startingAngle)
    
#########################################
# --      Exiting Parking Area       -- #
#########################################
def greenStart(sannisLivisa: FE):
    sannisLivisa.drive(510, 500, 600, heading=-3)
    sannisLivisa.turn(400, 90)
    sannisLivisa.drive(40, 500, 600, heading=90)
    sannisLivisa.lookDir(-90, False)
    greenEnding(sannisLivisa, 90)
    
def redStart(sannisLivisa: FE):
    sannisLivisa.drive(30, 500, 800, heading=0)
    sannisLivisa.turn(400, 90)
    sannisLivisa.drive(50, 500, 600, heading=90)
    sannisLivisa.drive(150, 500, 600, heading=93)
    sannisLivisa.drive(550, 500, 600, heading=80)

#########################################
# --             Parking             -- #
#########################################
def greenParking(sannisLivisa: FE):
    greenFirst(sannisLivisa, False)
    sannisLivisa.drive(530, 500, 600, heading=0)
    sannisLivisa.turn(430, 90)
    sannisLivisa.driveUntilStalled(170, 500, 600, heading=90)

def redParking(sannisLivisa: FE):
    redFirst(sannisLivisa, True, False)
    # sannisLivisa.drive(290, 500, 600, heading=-2)
    sannisLivisa.drive(550, 500, 600, heading=0)
    sannisLivisa.turn(500, -90)
    sannisLivisa.drive(80, 500, 600, heading=-90)
    sannisLivisa.driveUntilStalled(-400, 500, 600, heading=-91)



#########################################
# -- First Obstacle (If there is ONE) --#
#########################################
def greenFirst(sannisLivisa: FE, parking=False, brake=True):
    # if not parking:
    sannisLivisa.drive(200, 500, 600, heading=0)
    sannisLivisa.turn(450, -44)
    sannisLivisa.drive(220, 500, 600, heading=-44)
    sannisLivisa.turn(450, 0)
    sannisLivisa.drive(80, 500, 600, heading=0)

    if brake:
        sannisLivisa.eBrake(200)

def redFirst(sannisLivisa: FE, parking=False, brake=True):
    log("Red First:",parking)
    if not parking:
        sannisLivisa.drive(200, 500, 600, heading=0)
        sannisLivisa.turn(430, 38)
        sannisLivisa.drive(260, 500, 600, heading=38)
        sannisLivisa.turn(480, 0)
        sannisLivisa.drive(50, 500, 600, heading=0)
    else:
        sannisLivisa.drive(280, 500, 600, heading=0)
        sannisLivisa.drive(480, 500, 600, heading=5)
        sannisLivisa.drive(200, 500, 600, heading=0)
        

    if brake:
        sannisLivisa.eBrake(200)

#########################################
# -- Next Obstacle (If there is ONE) -- #
#########################################
def greenLast(sannisLivisa: FE, recording=False, parking=False):
    if not recording:
        sannisLivisa.lookDir(-90, asyncBool=False)
    if not parking:
        sannisLivisa.turn(450, -49)
        sannisLivisa.drive(625, 500, 600, heading=-49)
        sannisLivisa.turn(450, 0)
        sannisLivisa.drive(180, 500, 600, heading=0)
    else:
        sannisLivisa.turn(450, -45)
        sannisLivisa.drive(400, 500, 600, heading=-45)
        sannisLivisa.turn(450, 0)
        sannisLivisa.drive(300, 500, 600, heading=0)

    greenEnding(sannisLivisa)

def redLast(sannisLivisa: FE, recording=False, parking=False):
    if not recording:
        sannisLivisa.lookDir(-90, asyncBool=False)
        
    if not parking:
        sannisLivisa.turn(430, 45)
        sannisLivisa.drive(600, 500, 600, heading=45)
        sannisLivisa.turn(450, 0)
        sannisLivisa.drive(180, 500, 600, heading=0)
        redEnding(sannisLivisa)
    else:
        sannisLivisa.turn(450, 24)
        sannisLivisa.drive(630, 500, 600, heading=24)
        log("Done with turn")
        sannisLivisa.turn(370, 0)
        sannisLivisa.drive(800, 500, 600, heading=0)
    

#########################################
# --      Pre Recorded Movements     -- #
#########################################
def greenOnly(sannisLivisa: FE, parking):
    greenFirst(sannisLivisa, parking, brake=False)
    sannisLivisa.drive(1050, 500, 750, heading=0)
    greenEnding(sannisLivisa)

def redOnly(sannisLivisa: FE, parkingBool):
    redFirst(sannisLivisa, parking=parkingBool, brake=False)
    sannisLivisa.drive(900, 500, 850, heading=0)
    if not parkingBool:
        redEnding(sannisLivisa)
    else:
        sannisLivisa.drive(800, 500, 850, heading=-1)



def greenRed(sannisLivisa: FE, recording=True, parking=False):
    greenFirst(sannisLivisa, parking, brake=False)
    redLast(sannisLivisa, recording, parking)

def redGreen(sannisLivisa: FE, recording=True, parking=False):
    redFirst(sannisLivisa, parking, brake=False)
    greenLast(sannisLivisa, recording, parking)

def wallingTurnAndRecord(sannisLivisa: FE):
    pillarColor = "None"
    targetHeading = -90
    # Turn and record
    greenDetections = 0
    redDetections = 0

    while HUB.imu.heading() > targetHeading + WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction > WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        lerror = (targetHeading - HUB.imu.heading())*1.1

        sannisLivisa.lookDir(lerror, asyncBool=False, speed=1000)
        sannisLivisa.move(-MAXSPEED, correction)

        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
        if tempColor != "None" and tempData[2] > MINTHRESHOLD:
            pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 1500, 0.2, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight

        

    sannisLivisa.driveUntilStalled(-200, 500, 600, heading=-90)

    beep()
    sannisLivisa.lookDir(0, asyncBool=False)
    log("Error in walling:", abs(HUB.imu.heading() + 90))

    #Correct if not walled Correctly
    error = HUB.imu.heading() + 90
    if error > WALLING_ERROR_TOLERANCE:
        turntimer = StopWatch()
        turntimer.reset()
        turntimer.pause()
        beep(700)
        direc = -40 if error > 0 else 40
        turntimer.resume()
        while turntimer.time() < TURNDURATION:
            sannisLivisa.move(-600, direc)
        turntimer.reset()
        turntimer.pause()
        sannisLivisa.eBrake(200)

    tempColor, tempData = sannisLivisa.determineTrafficSignBlob()
    if tempData != (0, 0, 0) and tempColor != "None":
        pillarColor = tempColor

    sannisLivisa.drive(-50, 500, 600)
    sannisLivisa.driveMotor.reset_angle(0)
    sannisLivisa.eBrake(300)
    HUB.imu.reset_heading(0)
    return pillarColor

def wallingTurn(sannisLivisa: FE):
    targetHeading = -90
    # Turn and record
    while HUB.imu.heading() > targetHeading + WALLING_TURN_TOLERANCE:
        error =  HUB.imu.heading() - targetHeading
        # print(error)
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(WALLING_KP, 0.001, 0.3, error, sannisLivisa.errorSum, sannisLivisa.prevError)
        correction = WALLINGREVERSEANGLE if correction > WALLINGREVERSEANGLE else correction # -37 if correction < -37 else correction for 800
        sannisLivisa.move(-MAXSPEED, correction)

    sannisLivisa.driveUntilStalled(-200, 500, 600, heading=-90)
    beep()
    sannisLivisa.lookDir(0, asyncBool=False)
    log("Error in walling:", abs(HUB.imu.heading() + 90))
    error = HUB.imu.heading() + 90
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
        pillarColor = scanOnce(sannisLivisa,  -30, 50, minThreshold=450)
    else:
        pillarColor = scanOnce(sannisLivisa, -50, 40, minThreshold=450)

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
        sannisLivisa.drive(1250, 500, 600, heading=0)
        sannisLivisa.lookDir(-90, asyncBool=False)

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
    if parking:
        log("Parking Lap")

    if list(set(currentObstacles)) == GREEN:
        greenOnly(sannisLivisa, parking)

    elif list(set(currentObstacles)) == RED:
        redOnly(sannisLivisa, parking)

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
        redParking(sannisLivisa)
        
def Counter(sannisLivisa: FE):
    sannisLivisa.lookDir(-30)
    details=[]
    pillarColor, data = sannisLivisa.determineTrafficSignBlob()
    if pillarColor == 'None' or data[2] < 600:
        pillarColor, data, details = scanList(sannisLivisa, -90, 10, delayTime=10, minThreshold=570)
        pillarColor, data, angle = details[-1]
    else:
        details = [[pillarColor, data, -30]]

    log("First Detection:", pillarColor, data, details)
    # wait(1000)
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
    runRecordParking(sannisLivisa)

def testing(sannisLivisa):
    while True:
        recordQuarterLap(sannisLivisa)
        runRecord(sannisLivisa, 0.25)


if __name__ == "__main__":
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.C, Port.D, Port.F)
    # checkParking(sannisLivisa)
    # wait(100000)
    # wallingTurnAndRecord(sannisLivisa)
    # sannisLivisa.record(".0", ["Green", "Green"])
    # # runRecord(sannisLivisa, 0.0)
    # checkParking(sannisLivisa)
    Counter(sannisLivisa)
