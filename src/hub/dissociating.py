# Contains Utils and Classes

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.tools import wait, StopWatch
from pupremote_hub import PUPRemoteHub
from usys import stdin
from uselect import poll

HUB = PrimeHub()

HUB.system.set_stop_button([Button.BLUETOOTH])
HUB.speaker.volume(100)
HUB.display.off()
HUB.light.off()
HUB.speaker.volume(100)

# For RC ONLY
keys = poll()
keys.register(stdin)

# Consts
STEERING = -1
SENSE = 1
DEBUG = True
SCREENWIDTH = 320
SCREENHEIGHT = 169

MAXCORRECTION_DRIVE = 13
MINCORRECTION_DRIVE = -20

MAX_TURN_ANGLE = 45
MIN_TURN_ANGLE = -49
ANGLE_KP_THRESHOLD = 50
MINTHRESHOLD = 300

## To be Copied Over
def clearOutput():
    for i in range(5):
        print()

def beep(freq=500, dur=10):
    HUB.speaker.beep(freq, dur)

def linearMap(lmInput, lmInputMin, lmInputMax, lmOutputMin, lmOutputMax):
    if lmInputMin > lmInputMax:
        lmInputMin, lmInputMax = lmInputMax, lmInputMin
        lmOutputMin, lmOutputMax = lmOutputMax, lmOutputMin
    return ((((lmOutputMax - lmOutputMin) * (lmInput - lmInputMin)) / (lmInputMax - lmInputMin)) + lmOutputMin)

def tLinearMap(lmInput, lmInputMin, lmInputMax, lmOutputMin, lmOutputMax):
    lmMid = (lmInputMin + lmInputMax) / 2
    lmDistance = abs(lmInput - lmMid)
    lmMaxDistance = (lmInputMax - lmInputMin) / 2
    lmNormalized = lmDistance / lmMaxDistance
    lmOutputRange = lmOutputMax - lmOutputMin
    return lmOutputMax - (lmNormalized * lmOutputRange)

def pid(KP, KI, KD, inError, inSum, inPrevError, maxSum=150, minSum=-150):
    p = inError * KP
    newSum = inError + inSum
    if newSum > 0:
        inSum = newSum if newSum < maxSum else maxSum

    else:
        inSum = newSum if newSum > -minSum else -minSum

    i = inSum * KI
    d = (inError - inPrevError) * KD

    output = p + i + d

    return inSum, inError, output

def colorSensorIntHSV(colorSensor, colorSensorReturnValue = -1):
    # 0 = hue
    # 1 = sat
    # 2 = val
    if (colorSensorReturnValue == -1):
        return [int(str(colorSensor.hsv()).split(",")[0].split("=")[1]), int(str(colorSensor.hsv()).split(",")[1].split("=")[1]), int(str(colorSensor.hsv()).split(",")[2].split("=")[1].split(")")[0])];
    elif (colorSensorReturnValue == 0):
        return int(str(colorSensor.hsv()).split(",")[0].split("=")[1]);
    elif (colorSensorReturnValue == 1):
        return int(str(colorSensor.hsv()).split(",")[1].split("=")[1]);
    elif (colorSensorReturnValue == 2):
        return int(str(colorSensor.hsv()).split(",")[2].split("=")[1].split(")")[0]);

def log(*args, level="LOG"):
    print(f"[{level}]", *args)

def printInfo():
    clearOutput()
    log("Current Bat:", HUB.battery.voltage())

# Pre-programmed Movements

def scanList(sannisLivisa, startAngle, endAngle, delayTime=10, minThreshold=MINTHRESHOLD):
    # Final return values
    pillarColor, trafficSignData = "None", (0, 0, 0)

    # List of all valid detections: [("Red", (x, y, pix), angle), ...]
    detected = []

    lastSeenColor = None
    lastSeenData = (0, 0, 0)
    lastSeenAngle = None

    _ = startAngle
    angleStep = 1 if startAngle < endAngle else -1

    def tryAppend():
        nonlocal pillarColor, trafficSignData, lastSeenColor, lastSeenData, lastSeenAngle
        if lastSeenColor is not None:
            detected.append((lastSeenColor, lastSeenData, lastSeenAngle))
            pillarColor = lastSeenColor
            trafficSignData = lastSeenData
            lastSeenColor = None
            lastSeenData = (0, 0, 0)
            lastSeenAngle = None

    while (startAngle < endAngle and sannisLivisa.senseMotor.angle() < endAngle) or \
          (startAngle > endAngle and sannisLivisa.senseMotor.angle() > endAngle):

        sannisLivisa.lookDir(_, asyncBool=False)
        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()

        if tempColor != "None" and tempData[-1] > minThreshold:
            lastSeenColor = tempColor
            lastSeenData = tempData
            lastSeenAngle = _
            beep(dur=delayTime)
        else:
            tryAppend()
            wait(delayTime)
        _ += angleStep

    tryAppend()  # Finalize last detection if loop ended with one in view

    def merge(detections, angleThreshold):
        merged = []
        used = [False] * len(detections)

        for i in range(len(detections)):
            if used[i]:
                continue
                
            color_i, data_i, angle_i = detections[i]
            best = detections[i]

            for j in range(i + 1, len(detections)):
                if used[j]:
                    continue
                color_j, data_j, angle_j = detections[j]
                if color_i == color_j and abs(angle_i - angle_j) <= angleThreshold:
                    # Choose the one with more pixels (data[2])
                    if data_j[2] > best[1][2]:
                        best = detections[j]
                    used[j] = True

            used[i] = True
            merged.append(best)

        return merged

    log(detected)
    merged = merge(detected, 55)
    if len(merged) > 0:
        pillarColor, trafficSignData = merged[-1][0:2]
        return pillarColor, trafficSignData, merged[0:2]
    else:
        return "None", (0, 0, 0), [("None", (0, 0, 0), 0)]

def scanOnce(sannisLivisa: FE, startAngle: FE, endAngle: int, delayTime: int=10, minThreshold: int=MINTHRESHOLD):
    pillarColor = "None"
    pillarData = (0, 0, 0)

    greenDetections = 0
    redDetections = 0

    _ = startAngle
    angleStep = 1 if startAngle < endAngle else -1

    while (startAngle < endAngle and sannisLivisa.senseMotor.angle() < endAngle) or \
          (startAngle > endAngle and sannisLivisa.senseMotor.angle() > endAngle):

        sannisLivisa.lookDir(_, asyncBool=False)
        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()

        if tempColor != "None" and tempData[2] > minThreshold:
            pixelWeight = linearMap(tempData[2], minThreshold, 4000, 0.2, 1.0)  # You can adjust range/scale
            # print(pixelWeight, tempData[2])
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight
            beep(500, delayTime)
        else:
            wait(delayTime)


        _ += angleStep

    log("Red:", redDetections, "| Green:", greenDetections)

    if greenDetections > redDetections:
        return "Green"
    elif redDetections > greenDetections:
        return "Red"
    else:
        return "None"

class FE():
    def __init__(self, steeringMotor: Port, driveMotor: Port, senseMotor: Port, distSensorB: Port, distSensor: Port, camSensor: Port, camEnabled: bool = True):
        """
        Params:
        Steering Motor, Drive Motor, SenseMotor, Back Distance Sensor, Distance Sensor, Camera Sensor
        ( All are Ports)
        """
        self.steeringMotor = Motor(steeringMotor, Direction.COUNTERCLOCKWISE, reset_angle=False, profile=5)
        self.driveMotor = Motor(driveMotor, Direction.COUNTERCLOCKWISE, reset_angle=False, profile=365)
        self.senseMotor = Motor(senseMotor, Direction.COUNTERCLOCKWISE, reset_angle=False, profile=5)
        self.defaultDriveValues = [2000, 20000, 1000]
        self.driveMotor.control.limits(2000, 20000, 1000)
        self.steeringMotor.control.limits(2000, 20000, 1000)
        self.senseMotor.control.limits(2000, 20000, 1000)
        
        # -- Reset Angle of Movement motors -- #

        # self.steeringMotor.reset_angle(0)
        # self.senseMotor.reset_angle(0)  
        self.driveMotor.reset_angle(0)

        # self.colorSensor = ColorSensor(colorSensor)
        self.distSensor = UltrasonicSensor(distSensor)
        self.distSensorBack = UltrasonicSensor(distSensorB)

        # -- PID Constants - Forward Direction -- #
        self.KPdriveFCT = 4.6
        self.KIdriveFCT = 0.00004    

        self.KPdriveBCT = 4.8
        self.KIdriveBCT = 0.00004

        self.KPdriveFC  = 4.6
        self.KIdriveFC  = 0.000056

        self.KPdriveBC  = 4.2
        self.KIdriveBC  = 0.00004

        self.KDdrive    = 0.91
        self.prevError  = 0
        self.errorSum   = 0

        self.KPturnLeftLess     = 0.9
        self.KPturnLeftMore     = 1.11

        self.KPturnRightLess    = 0.89
        self.KPturnRightMore    = 0.9

        self.KDturn     = 0.81
        self.KITurn     = 0

        self.forwardMinTorque = 310
        self.backwardMinTorque = 320
        self.stalledTime = 1500

        self.forwardTurnLeftTolerance = 17
        self.forwardTurnRightTolerance = 9
        self.backwardTurnLeftTolerance = 15
        self.backwardTurnRightTolerance = 18 


        self.driveSpeedMin = 500
        self.driveSpeedMax = 1000
        self.lookSpeed     = 1000

        HUB.imu.reset_heading(0)

        self.memory = {}
        self.resetParams()

        if camEnabled:
            self.camSensor = PUPRemoteHub(camSensor)
            self.camSensor.add_command("blob", "hhhhhhhh")
            wait(500)                      # Wait for camera to setUp
        
        
    def _selectPIDConstants(self, heading, forward=True):
        """
        Select appropriate PID constants based on initial heading direction
        Negative heading = counterclockwise, use CT constants
        Positive heading = clockwise, use C constants
        """
        if forward:
            if heading < 0:  # Counterclockwise direction
                return self.KPdriveFCT, self.KIdriveFCT
            else:  # Clockwise direction
                return self.KPdriveFC, self.KIdriveFC
        else:  # Backward
            if heading < 0:  # Counterclockwise direction
                return self.KPdriveBCT, self.KIdriveBCT
            else:  # Clockwise direction
                return self.KPdriveBC, self.KIdriveBC

    # --- Getters --- #
    def mileage(self):
        return self.driveMotor.angle()

    def getDistance(self, selection):
        if selection == "front":
            return self.distSensor.distance()
        else:
            return self.distSensorBack.distance()

    def lookDir(self, deg, asyncBool: bool = True, speed = None, delayTimeation: int = 200):
        if speed == None:
            speed = self.lookSpeed

        self.senseMotor.run_target(speed, deg, wait=asyncBool)
        if asyncBool:
            wait(delayTimeation)

    def remember(self, key):
        return self.memory[key]

    # --- Setters --- #
    def resetParams(self):
        self.errorSum = 0
        self.prevError = 0

    def record(self, key, value):
        self.memory[key] = value
    
    # --- Movement --- #
    def center(self, specifier=0, wait=False):
        if specifier == 0:    
            self.steeringMotor.run_target(1000, 0)
            self.senseMotor.run_target(1000, 0)   

        elif specifier == STEERING:
            self.steeringMotor.run_target(1000, 0, wait=False)

        else:
            self.senseMotor.run_target(1000, 0, wait=wait)

    def eBrake(self, duration: int = 0):
        self.driveMotor.control.limits(speed=10, torque=1)
        self.driveMotor.hold()

        brakeTimer = StopWatch()
        brakeTimer.reset()
        brakeTimer.resume()

        while brakeTimer.time() < duration:
            pass            

        self.driveMotor.control.limits(speed=self.defaultDriveValues[0], torque=self.defaultDriveValues[2])

    def stop(self):
        self.driveMotor.stop()

    def move(self, speed, angle):
        self.steeringMotor.run_target(1000, angle)
        self.driveMotor.run(speed)

    def drive(self, dist, initialSpeed, finalSpeed, heading="", stopBool=False, stopDuration=100):
        global MAXCORRECTION_DRIVE, MINCORRECTION_DRIVE
        heading = HUB.imu.heading() if heading == "" else heading
        start = self.driveMotor.angle()
        target = start + dist

        # Select PID constants once based on initial heading
        baseKP, KI = self._selectPIDConstants(heading, forward=(dist > 0))
        # print(start, target, heading, HUB.imu.heading(), baseKP, KI)
        if (dist > 0):
            while self.driveMotor.angle() < target:
                error = heading - HUB.imu.heading()
                speed = linearMap(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

            # print(i)
        else:
            while self.driveMotor.angle() > target:
                error = HUB.imu.heading() - heading

                speed = linearMap(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, -1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, -1000, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                # if correction >= 0:
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                # else:
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.steeringMotor.run_target(1000, correction)
                self.driveMotor.run(speed)

        if stopBool:
            self.eBrake(stopDuration)
        # else:
        #     self.stop()
            
        self.resetParams()

    def driveUntilStalled(self, accelDist, initialSpeed, finalSpeed, heading=""):
        heading = HUB.imu.heading() if heading == "" else heading
        start = self.driveMotor.angle()
        target = start + accelDist
        self.resetParams()

        self.drive(accelDist, initialSpeed, finalSpeed, heading=heading)

        # Select PID constants once based on initial heading
        baseKP, KI = self._selectPIDConstants(heading, forward=(accelDist > 0))

        stallClock = StopWatch()
        stallClock.reset()
        stallClock.resume()
        

        if (accelDist > 0):
            self.driveMotor.control.limits(torque=self.forwardMinTorque)
            self.forwardStallSpeed = finalSpeed // 2

            while (self.driveMotor.speed() > self.forwardStallSpeed and stallClock.time() < self.stalledTime):
                error = heading - HUB.imu.heading()
                speed = linearMap(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                
                # if correction >= 0:
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                # else:
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

            self.driveMotor.stop()
            self.driveMotor.control.limits(torque=self.defaultDriveValues[2])
            self.center(STEERING)
            # self.drive(110, initialSpeed, finalSpeed)
        else:
            self.driveMotor.control.limits(torque=self.backwardMinTorque)
            self.backwardStallSpeed = -(finalSpeed // 2.4)

            while (self.driveMotor.speed() < self.backwardStallSpeed and stallClock.time() < self.stalledTime):
                error = HUB.imu.heading() - heading

                speed = linearMap(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, -1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, -1000, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)

                # if correction >= 0:
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                # else:
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

            self.driveMotor.stop()
            self.driveMotor.control.limits(torque=self.defaultDriveValues[2])
            self.center(STEERING)
            self.drive(-110, initialSpeed, finalSpeed)
        stallClock.pause()
        stallClock.reset()
            
    def driveUntilProximity(self, speed, proximity, heading="", lookHeading=0, selection="front", brake=True):
        heading = HUB.imu.heading() if heading == "" else heading
        self.resetParams()

        baseKP, KI = self._selectPIDConstants(heading, forward=(speed > 0))
        
        if (speed > 0):
            while self.getDistance(selection) > proximity:
                error = heading - HUB.imu.heading()
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                self.lookDir(lookHeading - HUB.imu.heading(), False)
                
                correction = 40 if correction > 40 else correction
                correction = -48 if correction < -48 else correction

                self.move(speed, correction)

        else:
            if selection == "front":
                while self.getDistance(selection) > proximity:
                    # log(self.getDistance(selection))
                    error = HUB.imu.heading() - heading
                    KP = linearMap(self.driveMotor.speed(), 0, -1000, 0, baseKP)
                    KD = linearMap(self.driveMotor.speed(), 0, -1000, self.KDdrive, 0)
                    self.lookDir(lookHeading - HUB.imu.heading(), False)
                    
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = 30 if correction > 30 else correction
                    correction = -35 if correction < -35 else correction
                    # print(error, HUB.imu.heading(), correction)
                    self.move(speed, correction)
            else:
                while self.getDistance(selection) > proximity:
                    # print(self.getDistance(selection))
                    error = HUB.imu.heading() - heading
                    KP = linearMap(self.driveMotor.speed(), 0, -1000, 0, baseKP)
                    KD = linearMap(self.driveMotor.speed(), 0, -1000, self.KDdrive, 0)
                    
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)

                    correction = 48 if correction > 48 else correction
                    correction = -45 if correction < -45 else correction

                    self.lookDir(lookHeading - HUB.imu.heading(), False)
                    self.move(speed, correction)

    
        # self.driveMotor.stop()
        if brake:
            self.eBrake(200)
        print(f"Final Distance From Wall: {self.getDistance(selection)}")

    def turn(self, speed, targetAngle, reverse=False, ):
        # reset error sum and prev error
        self.resetParams()
        current = HUB.imu.heading()
        targetError = targetAngle - current
        direction = 1 if targetError > 0 else -1
        # Set PID constants
        if direction > 0:
            KP = self.KPturnRightLess if abs(targetError) < ANGLE_KP_THRESHOLD else self.KPturnRightMore
        else:
            KP = self.KPturnLeftLess if abs(targetError) < ANGLE_KP_THRESHOLD else self.KPturnLeftMore

        KI = self.KITurn
        KD = self.KDturn

        prevCorrection = 0

        if reverse == False:
            if direction > 0:
                correction = 100
                tolerance = self.forwardTurnRightTolerance * 1.5 if abs(targetError) > ANGLE_KP_THRESHOLD else self.forwardTurnRightTolerance
                toFollow = targetAngle - tolerance
                if DEBUG:
                    log(f"Turn to {targetAngle}deg ending", toFollow)
        
                while HUB.imu.heading() < toFollow:
                    error = targetAngle - HUB.imu.heading()
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = 45 if correction > 45 else correction
                    correction = 3 if correction < 3 else correction
                    self.move(speed, correction)



            else:
                tolerance = self.forwardTurnLeftTolerance * 1.2 if abs(targetError) > 40 else self.forwardTurnLeftTolerance // 2
                toFollow = targetAngle + tolerance
                if DEBUG:
                    log(f"Turn to {targetAngle}deg ending", targetAngle+tolerance)
                while HUB.imu.heading() > toFollow:
                    error = targetAngle - HUB.imu.heading()
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = -48 if correction < -48 else correction
                    correction = -8 if correction > -8 else correction
                    self.move(speed, correction)

        else:
            if direction > 0:
                if DEBUG:
                    log(f"Turn to {targetAngle}deg ending", targetAngle - self.backwardTurnRightTolerance)

                while HUB.imu.heading() < targetAngle - self.backwardTurnRightTolerance:
                    error = HUB.imu.heading() - targetAngle
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = -60 if correction < -60 else correction
                    self.move(-speed, correction)
            else:
                if DEBUG:
                    log(f"Turn to {targetAngle}deg ending", targetAngle + self.backwardTurnLeftTolerance)
                while HUB.imu.heading() > targetAngle + self.backwardTurnLeftTolerance:
                    error = HUB.imu.heading() - targetAngle
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = 45 if correction > 45 else correction
                    self.move(-speed, correction)

        print(HUB.imu.heading())

    def turnDriveAndCheckIfSnag(self, turnSpeed, targetAngle, initalDriveSpeed, driveDist, graceTime):
        snagTimer = StopWatch()
        snagTimer.pause()
        snagTimer.reset()

    def determineDir(self):
        self.lookDir(90, speed=1000)
        wait(200)
        distRight = self.distSensor.distance()
        print(distRight)

        self.lookDir(-90, speed=1000)
        wait(200)
        distLeft = self.distSensor.distance()
        print(distLeft)

        if distLeft > distRight:
            direction = -1
        else:
            direction = 1

        print(direction)
        self.center()
        return direction
        
    def getTrafficSigns(self):
        # if DEBUG:
        #     data = self.camSensor.call("blob")

        #     green = data[0:3]
        #     red = data[3:6]
        
        #     return green, red
        # else:
        try:
            data = self.camSensor.call("blob")

            green = data[0:3]
            red = data[3:6]
        
            return green, red
        except:
            print("Error! Problem Encountered while attempting to retreive data from camera!\n Maybe connection is loose?")
            return ((0, 0, 0), (0, 0, 0))

    def determineTrafficSignBlob(self):
        currentGreen, currentRed = self.getTrafficSigns()
        greenX, greenY, greenPix = currentGreen
        redX, redY, redPix = currentRed
        obstacleData = (0, 0, 0)
        obsColor = "None"

        # determin & log first obstacle
        if greenPix > redPix:
            obstacleData = currentGreen
            obsColor = "Green"
        elif redPix > greenPix:
            obstacleData = currentRed
            obsColor = "Red"
        else:
            if DEBUG:
                pass
                # log("No Traffic Signs Detected!")

        return [obsColor, obstacleData]
    
    def kc(self):
        self.senseMotor.close()
        self.steeringMotor.close()
        self.driveMotor.close()

    def remoteControl(self):
        key = ""
        theta = 0
        vel = 0
        while True:
            if keys.poll(0):
                key = stdin.read(1)
                if (key == "w"): 
                    vel = 800
                if (key == "s"): 
                    vel = -800
                if (key == "a"): 
                    theta = min(theta - 40, -40)
                if (key == "q"):
                    theta = 0
                if (key == "d"): 
                    theta = max(theta  + 40, 40)
                if (key == " "):
                    vel = 0

            self.move(vel, theta)

# # Avoid Misdownload of Code
if __name__ == "__main__":
    from test import *
    # OpenChallenge()
