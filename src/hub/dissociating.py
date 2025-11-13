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

PUSH = 1
INSERT = -1

FRONT = "front"
LEFT = "left"
RIGHT = "right"
BACK = "back"
FORWARD = "forward"
BACKWARD = "backward"

DEBUG = False
SCREENWIDTH = 320
SCREENHEIGHT = 169

MAXCORRECTION_DRIVE = 15
MINCORRECTION_DRIVE = -15

MAX_TURN_ANGLE = 42
MIN_TURN_ANGLE = -42
ANGLE_KP_THRESHOLD = 60
MINTHRESHOLD = 110

COMPE = False

logs = []

## To be Copied Over
def clearOutput():
    for i in range(5):
        print()

def beep(freq=500, dur=10):
    HUB.speaker.beep(freq, dur)

def chopsuey(sannisLivisa: FE):
    sannisLivisa.eBrake(400)
    k

def linearMap(lmInput, lmInputMin, lmInputMax, lmOutputMin, lmOutputMax):
    if lmInput <lmInputMin:
        return lmOutputMin
    elif lmInput > lmInputMax:
        return lmOutputMax

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


# tLinearap((left + right) / 2, 0, 100, 500, 1000, 500)
# start = (left.angle() + right.angle()) / 2
# while True:
#     current = left.angle() + right.angle()) / 2
#     left.run(tLinearap(current, start, 100, 500, 1000, 500))
#     right.run(tLinearap(current, start, 100, 500, 1000, 500))

def pid(KP, KI, KD, inError, inSum, inPrevError, maxSum=150, minSum=-150):
    # if inError < 0.1 and inError > -0.1 :
    #     newSum = 0
    if inError > 0.25 or inError < -0.25:
        newSum = inError + inSum
    else:
        newSum = inSum


    # Clamp the integral sum
    if newSum > maxSum:
        inSum = maxSum
    elif newSum < minSum:
        inSum = minSum
    else:
        inSum = newSum

    # Continue with PID calculation
    p = inError * KP
    i = inSum * KI
    d = (inError - inPrevError) * KD

    output = p + i + d
    # print(f"Err: {inError:.2f}, P: {p:.2f}, KP: {KP},  D: {d:.2f}, I: {i}, Corr: {output:.2f}, Sum: {inSum}")
    return inSum, inError, output


def colorSensorIntHSV(colorSensor, colorSensorReturnValue = -1):
    # 0 = hue
    # 1 = sat
    # 2 = val
    # print(colorSensor.hsv())
    if (colorSensorReturnValue == -1):
        return [int(str(colorSensor.hsv()).split(",")[0].split("=")[1]), int(str(colorSensor.hsv()).split(",")[1].split("=")[1]), int(str(colorSensor.hsv()).split(",")[2].split("=")[1].split(")")[0])];
    elif (colorSensorReturnValue == 0):
        return int(str(colorSensor.hsv()).split(",")[0].split("=")[1]);
    elif (colorSensorReturnValue == 1):
        return int(str(colorSensor.hsv()).split(",")[1].split("=")[1]);
    elif (colorSensorReturnValue == 2):
        return int(str(colorSensor.hsv()).split(",")[2].split("=")[1].split(")")[0]);

def log(*args, level="LOG"):
    # global logs
    # if COMPE:
    # print(args)
    # logs.append(f"[{level}]" + " ".join(str(arg) for arg in args))
    # if DEBUG:
    print(f"[{level}]", *args)

def saveLogs(logs):
    result = []

    for string in logs:
        result.extend([ord(char) for char in string] + [10])

    length = len(result)
    result.insert(0, length)
    return result

def readLogs():
    processed = ""
    num = ord(HUB.system.storage(0, read=1))
    # print(num)

    data = HUB.system.storage(1, read=num)

    for char in data:
        processed += chr(char)

    return processed

def printInfo():
    clearOutput()
    log("Current Bat:", HUB.battery.voltage())

# Pre-programmed Movements
def scanList(sannisLivisa: FE, startAngle, endAngle, delayTime=10, minThreshold=MINTHRESHOLD):
    # Default outputs
    pillarColor, trafficSignData = "None", (0, 0, 0, "None")
    detected = []  # [(color, (x, y, pix), angle)]

    angleStep = 1 if startAngle < endAngle else -1
    _ = startAngle
    sannisLivisa.senseMotor.run_target(1000, startAngle)

    # --- Scan loop ---
    if startAngle < endAngle:
        while sannisLivisa.senseMotor.angle() < endAngle:
            sannisLivisa.lookDir(_, asyncBool=False)
            color, data = sannisLivisa.determineTrafficSignBlob()
            if color != "None" and data[-1] > minThreshold:
                detected.append((color, data, _))
            wait(delayTime)
            _ += angleStep
    else:
        while sannisLivisa.senseMotor.angle() > endAngle:
            sannisLivisa.lookDir(_, asyncBool=False)
            color, data = sannisLivisa.determineTrafficSignBlob()
            if color != "None" and data[-1] > minThreshold:
                detected.append((color, data, _))
            wait(delayTime)
            _ += angleStep

    # --- Nothing seen ---
    if not detected:
        return "None", (0, 0, 0, "None"), [("None", (0, 0, 0, "None"), 0)]

    # --- Group detections by color ---
    grouped = {}
    for color, data, angle in detected:
        grouped.setdefault(color, []).append((data, angle))

    # --- Keep max 2 distinct colors (based on largest blob seen overall) ---
    color_order = sorted(
        grouped.keys(),
        key=lambda c: max([d[0][2] for d in grouped[c]]),  # sort by biggest blob
        reverse=True
    )[:2]

    final_detections = []

    # --- Pick the largest blob per color, classify, and store ---
    for color in color_order:
        blobs = grouped[color]
        biggest_data, biggest_angle = max(blobs, key=lambda d: d[0][2])

        # categorize by position for context
        span = endAngle - startAngle
        if biggest_angle < startAngle + span / 3:
            zone = "Left"
        elif biggest_angle > startAngle + 2 * span / 3:
            zone = "Right"
        else:
            zone = "Middle"

        data_with_zone = (biggest_data[0], biggest_data[1], biggest_data[2], zone)
        final_detections.append((color, data_with_zone, biggest_angle))

    # --- Sort detections left-to-right (or reversed) ---
    reverse = False if startAngle < endAngle else True
    final_detections.sort(key=lambda d: d[2], reverse=reverse)

    # --- Select pillar color (default: leftmost / reverse: rightmost) ---
    # if reverse:
    #     pillarColor, trafficSignData = final_detections[0][0], final_detections[0][1]
    # else:
    pillarColor, trafficSignData = final_detections[-1][0], final_detections[-1][1]


    return pillarColor, trafficSignData, final_detections

def scanOnce(sannisLivisa: FE, startAngle: int, endAngle: int, delayTime: int=10, minThreshold: int=MINTHRESHOLD):
    pillarColor = "None"
    greenDetections = 0
    redDetections = 0

    angleStep = 1 if startAngle < endAngle else -1

    for angle in range(startAngle, endAngle + angleStep, angleStep):
        sannisLivisa.lookDir(angle, asyncBool=False)
        tempColor, tempData = sannisLivisa.determineTrafficSignBlob()

        if tempColor != "None" and tempData[2] > minThreshold:
            pixelWeight = linearMap(tempData[2], minThreshold, 4000, 0.2, 1.0)
            if tempColor == "Green":
                greenDetections += pixelWeight
            elif tempColor == "Red":
                redDetections += pixelWeight
            # beep(500, delayTime)
            wait(delayTime)

        else:
            wait(delayTime)

    log("Red:", redDetections, "| Green:", greenDetections)

    if greenDetections > redDetections:
        return "Green"
    elif redDetections > greenDetections:
        return "Red"
    else:
        return "None"

def sharedParking(sannisLivisa: FE):
    sannisLivisa.driveUntilStalled(50, 500, 600, heading=-90)
    sannisLivisa.eBrake(200)
    HUB.imu.reset_heading(0)
    sannisLivisa.turn(600,55, True)

    sannisLivisa.drive(400, 400, 600, heading=90)
    sannisLivisa.eBrake(200)
    # sannisLivisa.drive(-540, 400, 500, heading=90, decelerate=True)
    sannisLivisa.driveUntilProximity(-400, 1080, heading=90, lookHeading=90, reverseCondition=True)
    sannisLivisa.eBrake(200)
    
    sannisLivisa.turn(300, 155, True)
    # sannisLivisa.driveUntilProximity(-250, 150, heading=145, selection=BACK)
    # sannisLivisa.drive(-50, 250, 300, heading=154)
    sannisLivisa.driveUntilStalled(-300, 400, 500, heading=155)
    beep()
    sannisLivisa.drive(80, 300, 400, stopBool=True)
    sannisLivisa.turn(200, 130, True)
    sannisLivisa.reverseUntilAngleOrWall(200, 90, 60)

    i = 0
    while abs(90 - HUB.imu.heading()) > 4 and i < 2:
        # print(i)
        sannisLivisa.driveUntilProximity(200, 50, heading=90, lookHeading=90)
        sannisLivisa.driveUntilProximity(-200, 55, heading=90, lookHeading=90, selection=BACK)

def checkIfFlushWithWall(sannisLivisa, errorTolerance, forwardAmount, backwardSpeed, targetHeading, turnDuration, steerAngle):
    # log("Error in walling:", abs(HUB.imu.heading() - targetHeading))
    error = HUB.imu.heading() - targetHeading
    if abs(error) > errorTolerance:
        sannisLivisa.drive(forwardAmount, 300, 400)
        sannisLivisa.eBrake(10)

        turntimer = StopWatch()
        turntimer.reset()
        turntimer.pause()
        beep(700)
        direc = -steerAngle if error > 0 else steerAngle
        turntimer.resume()
        while turntimer.time() < turnDuration:
            sannisLivisa.move(-backwardSpeed, direc)
        turntimer.reset()
        turntimer.pause()


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

        print(self.driveMotor.settings())
        
        # -- Reset Angle of Movement motors -- #

        # self.steeringMotor.reset_angle(0)
        # self.senseMotor.reset_angle(0)  
        self.driveMotor.reset_angle(0)

        # self.colorSensor = ColorSensor(colorSensor)

        self.distSensor = UltrasonicSensor(distSensor)

        print("goods")

        # TODO try except which sets global flag
        self.distSensorBack = PUPRemoteHub(distSensorB)
        self.distSensorBack.add_command('line', 'hhh') 
        # print(self.distSensorBack.call("line")[-1])

        # -- PID Constants - Forward Direction -- #
        self.KPdriveFCT = 4.8
        self.KIdriveFCT = 0.000026

        self.KPdriveBCT = 3.5
        self.KIdriveBCT = 0.00003

        self.KPdriveFC  = 4.5
        self.KIdriveFC  = 0.00001

        self.KPdriveBC  = 4.6
        self.KIdriveBC  = 0.000002
        self.KDdrive    = 0.04
        self.prevError  = 0
        self.errorSum   = 0

        self.KPturnLeftLess     = 1.05
        self.KPturnLeftMore     = 1.78

        self.KPturnRightLess    = 1.02
        self.KPturnRightMore    = 1.7

        self.KDturn     = 0.48
        self.KITurn     = 0

        self.forwardMinTorque = 392
        self.backwardMinTorque = 315
        self.stalledTime = 1200
        self.globalStallTimer = StopWatch()
        self.globalStallTimer.reset()
        self.isTimerRunning = False

        self.forwardTurnLeftTolerance = 13
        self.forwardTurnRightTolerance = 15
        self.backwardTurnLeftTolerance = 12
        self.backwardTurnRightTolerance = 9

        self.driveSpeedMin = 500
        self.driveSpeedMax = 1000
        self.lookSpeed     = 1000

        HUB.imu.reset_heading(0)
        self.memory = {}
        self.resetParams()
        # beep()

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
        try:
            if selection == FRONT:
                # beep()
                return self.distSensor.distance()
            elif selection == LEFT:
                return self.distSensorBack.call("line")[0]
            elif selection == RIGHT:
                return self.distSensorBack.call("line")[1]
            else:
                return self.distSensorBack.call("line")[2]
        except:
            return 0

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

    def record(self, key, value, method=PUSH):
        if key in self.memory.keys():

            if method == PUSH:
                if type(value) != int:
                    self.memory[key].append(value)
                else:
                    self.memory[key] = value

            else:
                self.memory[key].insert(0, value)
            return

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
        self.steeringMotor.run_target(1000, angle, wait=False)
        # self.steeringMotor.track_target(angle)
        self.driveMotor.run(speed)

    def isStalled(self, currentSpeed, direction=FORWARD):
        """
        Check once if the drive motor is stalled, using a timer to confirm.
        Does not drive or loop — just detects.
        """

        

        # --- 1. Start or resume stall timer if not running --- #
        if not self.isTimerRunning:
            self.globalStallTimer.reset()
            self.globalStallTimer.resume()
            self.isTimerRunning = True

        # --- 2. Check speed thresholds based on direction --- #
        if direction == FORWARD:
            stallSpeed = currentSpeed // 1.8
            isBelowThreshold = self.driveMotor.speed() < stallSpeed
        else:
            stallSpeed = -(currentSpeed // 2)
            isBelowThreshold = self.driveMotor.speed() > stallSpeed

        # --- 3. Evaluate stall condition --- #
        if isBelowThreshold:
            # If motor stays below threshold long enough, it’s stalled
            if stallClock.time() > self.stalledTime:
                self.globalStallTimer.pause()
                self.globalStallTimer.reset()
                self.isTimerRunning = False
                return True
        else:
            # If motor recovered, reset the timer
            self.globalStallTimer.reset()
            self.globalStallTimer.pause()
            self.isTimerRunning = False

        return False


    def determineDirOld(self, exclude=2000):
        checkTimer = StopWatch()
        checkTimer.pause()
        checkTimer.reset()
        self.lookDir(90, speed=1000)
        while self.senseMotor.angle() < 88:
            pass
        
        start = self.mileage()
        target = start - 80
        self.driveMotor.run_target(180, target, wait=False)

        checkTimer.resume()
        largestRight = 0
        while checkTimer.time() < 800:
            dist = self.distSensor.distance()
            if dist > largestRight and dist != exclude:
                largestRight = dist

        checkTimer.pause()
        checkTimer.reset()
        log("Dist RIght:", largestRight, level="DETERMINE DIR")

        self.lookDir(-90, speed=1000)
        while self.senseMotor.angle() > -88:
            pass
        
        self.driveMotor.run_target(180, start, wait=False)

        checkTimer.resume()
        largestLeft = 0
        while checkTimer.time() < 800:
            dist = self.distSensor.distance()
            if dist > largestLeft and dist != exclude:
                largestLeft = dist

        checkTimer.pause()
        checkTimer.reset()

        log("Dist Left:", largestLeft, level="DETERMINE DIR")

        if largestLeft > largestRight:
            direction = -1
        else:
            direction = 1

        log(direction, level="DETERMINE DIR")
        self.center()
        self.driveUntilProximity(-200, 150, reverseCondition=True, heading=30)
        return direction

    def determineDir(self, exclude=2000, measureTime=100):
        try:
            checkTimer = StopWatch()
            checkTimer.pause()
            checkTimer.reset()
        
            checkTimer.resume()
            largestRight = 0
            largestLeft = 0
            while checkTimer.time() < measureTime:
                dists = self.distSensorBack.call("line")

                dist = dists[1]
                if dist > largestRight and dist != exclude:
                    largestRight = dist

                dist = dists[0]
                if dist > largestLeft and dist != exclude:
                    largestLeft = dist

            checkTimer.pause()
            checkTimer.reset()

            log("Dist Right:", largestRight, level="DETERMINE DIR")
            log("Dist Left:", largestLeft, level="DETERMINE DIR")
            log("Backup (Front):", largestLeft, level="DETERMINE DIR")

            if largestLeft > largestRight:
                direction = -1
            else:
                direction = 1

            log(direction, level="DETERMINE DIR")
            return direction
        except:
            log("LMS-ESP 32 Refused to connect!", level="ERROR")
            return self.determineDirOld()
        
    def getTrafficSigns(self):
        if COMPE:
            try:
                data = self.camSensor.call("blob")

                green = data[0:3]
                red = data[3:6]
            
                return green, red
            except:
                print("Error! Problem Encountered while attempting to retreive data from camera!\n Maybe connection is loose?")
                
                return ((0, 0, 0), (0, 0, 0))
        else:
            data = self.camSensor.call("blob")

            green = data[0:3]
            red = data[3:6]
        
            return green, red

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

    def drive(self, dist, initialSpeed, finalSpeed, heading="", stopBool=False, stopDuration=100, decelerate=False):
        heading = HUB.imu.heading() if heading == "" else heading
        start = self.driveMotor.angle()
        target = start + dist

        # Select PID constants once based on initial heading
        baseKP, KI = self._selectPIDConstants(heading, forward=(dist > 0))
        if decelerate == False:
            mappingFunc = linearMap
        else:
            mappingFunc = tLinearMap
        # print(start, target, heading, HUB.imu.heading(), baseKP, KI)
        if (dist > 0):
            while self.driveMotor.angle() < target:
                error = heading - HUB.imu.heading()
                speed = mappingFunc(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
                # print(correction)

                self.move(speed, correction)

            # print(i)
        else:
            while self.driveMotor.angle() > target:
                error = HUB.imu.heading() - heading

                speed = mappingFunc(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

        if stopBool:
            self.eBrake(stopDuration)
        self.resetParams()

    def driveUntilStalled(self, accelDist, initialSpeed, finalSpeed, heading="", decelerate=False):
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

        if decelerate == False:
            mappingFunc = linearMap
        else:
            mappingFunc = tLinearMap
        

        if (accelDist > 0):
            self.driveMotor.control.limits(torque=self.forwardMinTorque)
            self.forwardStallSpeed = finalSpeed // 1.8

            while (self.driveMotor.speed() > self.forwardStallSpeed and stallClock.time() < self.stalledTime):
                error = heading - HUB.imu.heading()
                speed = mappingFunc(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

            self.driveMotor.stop()
            self.driveMotor.control.limits(torque=self.defaultDriveValues[2])
        else:
            self.driveMotor.control.limits(torque=self.backwardMinTorque)
            self.backwardStallSpeed = -(finalSpeed // 2)

            while (self.driveMotor.speed() < self.backwardStallSpeed and stallClock.time() < self.stalledTime):
                error = HUB.imu.heading() - heading

                speed = mappingFunc(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)

                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

            self.driveMotor.stop()
            self.driveMotor.control.limits(torque=self.defaultDriveValues[2])
            # self.drive(-80, initialSpeed, finalSpeed)
        stallClock.pause()
        stallClock.reset()
            
    def driveUntilProximity(self, speed, proximity, heading="", lookHeading=0, selection="front", brake=True, reverseCondition=False):
        heading = HUB.imu.heading() if heading == "" else heading
        self.resetParams()

        baseKP, KI = self._selectPIDConstants(heading, forward=(speed > 0))

        if selection != FRONT:            
            if not reverseCondition:
                def condition(): return self.getDistance(selection) > proximity
            else:
                def condition(): return self.getDistance(selection) < proximity
            # condition = lambda: self.getDistance(selection) > proximity if not reverseCondition else self.getDistance(selection) < proximity
        else:
            if not reverseCondition:
                def condition(): return self.getDistance(selection) > proximity
            else:
                def condition(): 
                    dist = self.getDistance(selection)
                    print(dist, selection)
                    if dist != 2000:
                        return dist < proximity # or dist != 2000
                    return True
            # condition = (
            #     lambda: self.getDistance(selection) > proximity
            #     if not reverseCondition
            #     else lambda: (self.getDistance(selection) != 2000 and self.getDistance(selection) < proximity)
            # )        
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
            if selection == FRONT:
                log(condition(), condition)
                while condition():
                    # if 
                        # log(self.getDistance(selection))
                    error = HUB.imu.heading() - heading
                    KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                    KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                    self.lookDir(lookHeading - HUB.imu.heading(), False)
                    
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = 30 if correction > 30 else correction
                    correction = -35 if correction < -35 else correction
                    # print(error, HUB.imu.heading(), correction)
                    self.lookDir(lookHeading - HUB.imu.heading(), False)
                    self.move(speed, correction)
            else:
                while self.getDistance(selection) > proximity:
                    # print(self.getDistance(selection))
                    error = HUB.imu.heading() - heading
                    KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                    KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                    
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)

                    correction = 48 if correction > 48 else correction
                    correction = -45 if correction < -45 else correction

                    self.lookDir(lookHeading - HUB.imu.heading(), False)
                    self.move(speed, correction)

        if brake:
            self.eBrake(200)

        print(f"Final Distance From Wall: {self.getDistance(selection)}")

    def driveDeterminDir(self, dist, initialSpeed, finalSpeed, heading="", stopBool=False, stopDuration=100, decelerate=False, sideThreshold=200, frontThreshold=200):
        heading = HUB.imu.heading() if heading == "" else heading
        start = self.driveMotor.angle()
        target = start + dist

        # Select PID constants once based on initial heading
        baseKP, KI = self._selectPIDConstants(heading, forward=(dist > 0))
        if decelerate == False:
            mappingFunc = linearMap
        else:
            mappingFunc = tLinearMap

        if (dist > 0):
            ctr = 0
            while ctr < 3:
                if (self.getDistance(LEFT) - self.getDistance(RIGHT) > sideThreshold) or \
                    (self.getDistance(RIGHT) - self.getDistance(LEFT) > sideThreshold) or \
                    (self.getDistance(FRONT) < frontThreshold):
                    ctr += 1
                error = heading - HUB.imu.heading()
                speed = mappingFunc(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
                # print(correction)

                self.move(speed, correction)
        else:
            while (self.getDistance(LEFT) - self.getDistance(RIGHT) > sideThreshold) or \
                    (self.getDistance(RIGHT) - self.getDistance(LEFT) > threshold) or \
                    (self.getDistance(BACK) > frontThreshold):
                error = HUB.imu.heading() - heading

                speed = mappingFunc(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                self.move(speed, correction)

        if stopBool:
            self.eBrake(stopDuration)
        self.resetParams()

        return self.determineDir(measureTime=50)

    def scanAndDrive(self, dist, initialSpeed, finalSpeed, lookHeading, heading="", stopBool=False, stopDuration=100, decelerate=False):

        heading = HUB.imu.heading() if heading == "" else heading
        start = self.driveMotor.angle()
        target = start + dist

        # Select PID constants once based on initial heading
        baseKP, KI = self._selectPIDConstants(heading, forward=(dist > 0))
        if decelerate == False:
            mappingFunc = linearMap
        else:
            mappingFunc = tLinearMap
        # print(start, target, heading, HUB.imu.heading(), baseKP, KI)
        greenDetections = 0
        redDetections = 0

        self.lookDir(lookHeading, asyncBool=False)

        if (dist > 0):
            while self.driveMotor.angle() < target:
                error = heading - HUB.imu.heading()
                speed = mappingFunc(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
                # print(correction)

                tempColor, tempData = self.determineTrafficSignBlob()
                if tempColor != "None" and tempData[2] > MINTHRESHOLD:
                    pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
                    if tempColor == "Green":
                        greenDetections += pixelWeight
                    elif tempColor == "Red":
                        redDetections += pixelWeight

                self.move(speed, correction)

            # print(i)
        else:
            while self.driveMotor.angle() > target:
                error = HUB.imu.heading() - heading

                speed = mappingFunc(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                tempColor, tempData = self.determineTrafficSignBlob()
                if tempColor != "None" and tempData[2] > MINTHRESHOLD:
                    pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
                    if tempColor == "Green":
                        greenDetections += pixelWeight
                    elif tempColor == "Red":
                        redDetections += pixelWeight

                self.move(speed, correction)

        if stopBool:
            self.eBrake(stopDuration)
        self.resetParams()

        return (greenDetections, redDetections)

    def scanUntilStallled(self, accelDist, initialSpeed, finalSpeed, lookHeading, heading="", decelerate=False):
        heading = HUB.imu.heading() if heading == "" else heading
        start = self.driveMotor.angle()
        target = start + accelDist
        self.resetParams()

        greenDetections, redDetections = self.scanAndDrive(accelDist, initialSpeed, finalSpeed, lookHeading, heading=heading)

        # Select PID constants once based on initial heading
        baseKP, KI = self._selectPIDConstants(heading, forward=(accelDist > 0))

        stallClock = StopWatch()
        stallClock.reset()
        stallClock.resume()

        if decelerate == False:
            mappingFunc = linearMap
        else:
            mappingFunc = tLinearMap
        
        # self.lookDir(lookHeading, asyncBool=False)

        if (accelDist > 0):
            self.driveMotor.control.limits(torque=self.forwardMinTorque)
            self.forwardStallSpeed = finalSpeed // 2

            while (self.driveMotor.speed() > self.forwardStallSpeed and stallClock.time() < self.stalledTime):
                error = heading - HUB.imu.heading()
                speed = mappingFunc(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
                KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                tempColor, tempData = self.determineTrafficSignBlob()
                if tempColor != "None" and tempData[2] > MINTHRESHOLD:
                    pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
                    if tempColor == "Green":
                        greenDetections += pixelWeight
                    elif tempColor == "Red":
                        redDetections += pixelWeight

                self.move(speed, correction)

            self.driveMotor.stop()
            self.driveMotor.control.limits(torque=self.defaultDriveValues[2])
        else:
            self.driveMotor.control.limits(torque=self.backwardMinTorque)
            self.backwardStallSpeed = -(finalSpeed // 2.4)

            while (self.driveMotor.speed() < self.backwardStallSpeed and stallClock.time() < self.stalledTime):
                error = HUB.imu.heading() - heading

                speed = mappingFunc(self.driveMotor.angle(), start, target, -initialSpeed, -finalSpeed)
                KP = linearMap(self.driveMotor.speed(), -1000, 0, 0, baseKP)
                KD = linearMap(self.driveMotor.speed(), -1000, 0, self.KDdrive, 0)
                
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)

                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                tempColor, tempData = self.determineTrafficSignBlob()
                if tempColor != "None" and tempData[2] > MINTHRESHOLD:
                    pixelWeight = linearMap(tempData[2], MINTHRESHOLD, 4000, 0.2, 1.0)
                    if tempColor == "Green":
                        greenDetections += pixelWeight
                    elif tempColor == "Red":
                        redDetections += pixelWeight

                self.move(speed, correction)

            self.driveMotor.stop()
            self.driveMotor.control.limits(torque=self.defaultDriveValues[2])
            self.drive(-80, initialSpeed, finalSpeed)
        stallClock.pause()
        stallClock.reset()

        return (greenDetections, redDetections)

    def turn(self, speed, targetAngle, reverse=False):
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
                tolerance = self.forwardTurnRightTolerance * 1.1 if abs(targetError) > ANGLE_KP_THRESHOLD else self.forwardTurnRightTolerance
                toFollow = targetAngle - tolerance
                if DEBUG:
                    log(f"Turn to {targetAngle}deg ending", toFollow)
        
                while HUB.imu.heading() < toFollow:
                    error = targetAngle - HUB.imu.heading()
                    self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                    correction = 45 if correction > 45 else correction
                    correction = 4 if correction < 4 else correction
                    self.move(speed, correction)

            else:
                tolerance = self.forwardTurnLeftTolerance * 1.1 if abs(targetError) > ANGLE_KP_THRESHOLD else self.forwardTurnLeftTolerance
                
                toFollow = targetAngle + tolerance
                if DEBUG:
                    log(f"Turn to {targetAngle}deg ending {tolerance}", targetAngle+tolerance)
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

    def reverseUntilAngleOrWall(self, speed, targetAngle, stopDistance, headingTolerance=3):
        """
        Reverse and turn until reaching targetAngle or until rear distance is too close.
        Stops immediately if wall detected within stopDistance.
        """
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

        if direction > 0:
            if DEBUG:
                log(f"Turn to {targetAngle}deg ending", targetAngle - self.backwardTurnRightTolerance)

            while HUB.imu.heading() < targetAngle - self.backwardTurnRightTolerance:
                if self.getDistance(BACK) < stopDistance:
                    
                    self.eBrake(400)
                    break
                error = HUB.imu.heading() - targetAngle
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = -60 if correction < -60 else correction
                self.move(-speed, correction)
        else:
            if DEBUG:
                log(f"Turn to {targetAngle}deg ending", targetAngle + self.backwardTurnLeftTolerance)
            while HUB.imu.heading() > targetAngle + self.backwardTurnLeftTolerance:
                if self.getDistance(BACK) < stopDistance:
                    self.eBrake(400)
                    break

                # print(self.getDistance(BACK))
                error = HUB.imu.heading() - targetAngle
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = 45 if correction > 45 else correction
                self.move(-speed, correction)


    def turnDriveAndCheckIfSnag(self, turnSpeed, targetAngle, initialSpeed, finalSpeed, driveDist, decelerate=False, stopBool=False):
        turnTimer = StopWatch()
        turnTimer.reset()
        turnTimer.resume()
        self.resetParams()
        current = HUB.imu.heading()
        targetError = targetAngle - current
        direction = 1 if targetError > 0 else -1

        KI = self.KITurn
        KD = self.KDturn

        if direction > 0:
            KP = self.KPturnRightLess if abs(targetError) < ANGLE_KP_THRESHOLD else self.KPturnRightMore
        else:
            KP = self.KPturnLeftLess if abs(targetError) < ANGLE_KP_THRESHOLD else self.KPturnLeftMore

        if direction > 0:
            correction = 100
            tolerance = self.forwardTurnRightTolerance * 1.1 if abs(targetError) > ANGLE_KP_THRESHOLD else self.forwardTurnRightTolerance
            toFollow = targetAngle - tolerance
            if DEBUG:
                log(f"Turn to {targetAngle}deg ending", toFollow)
    
            while HUB.imu.heading() < toFollow and turnTimer.time() < 2000:
                error = targetAngle - HUB.imu.heading()
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = 45 if correction > 45 else correction
                correction = 4 if correction < 4 else correction
                self.move(turnSpeed, correction)

                deltaHeading = self.prevError - error
        else:
            tolerance = self.forwardTurnLeftTolerance * 1.1 if abs(targetError) > ANGLE_KP_THRESHOLD else self.forwardTurnLeftTolerance
            
            toFollow = targetAngle + tolerance
            if DEBUG:
                log(f"Turn to {targetAngle}deg ending {tolerance}", targetAngle+tolerance)
            while HUB.imu.heading() > toFollow and turnTimer.time() < 2000:
                error = targetAngle - HUB.imu.heading()
                self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
                correction = -48 if correction < -48 else correction
                correction = -8 if correction > -8 else correction
                self.move(turnSpeed, correction)

                deltaHeading = self.prevError - error

        # If the final heading is too far off from target, reverse slightly to retry
        if abs(HUB.imu.heading() - targetAngle) >25:
            log("Heading offset too large after turn, reversing to correct")
            log(f"CurrentHeading:", HUB.imu.heading())
            # self.turn(300, -4, True)
            # self.drive(-80, 300, 400, heading=0, stopBool=True, stopDuration=150)
            self.turn(300, 0, True)
            self.drive(driveDist+90, 300, 400, heading=0, stopBool=True, stopDuration=150)
        

        heading = targetAngle
        start = self.driveMotor.angle()
        target = start + driveDist

        baseKP, KI = self._selectPIDConstants(heading, forward=(driveDist > 0))
        mappingFunc = linearMap if not decelerate else tLinearMap

        while self.driveMotor.angle() < target:
            error = heading - HUB.imu.heading()
            speed = mappingFunc(self.driveMotor.angle(), start, target, initialSpeed, finalSpeed)
            KP = linearMap(self.driveMotor.speed(), 0, 1000, 0, baseKP)
            KD = linearMap(self.driveMotor.speed(), 0, 1000, 0, self.KDdrive)

            self.errorSum, self.prevError, correction = pid(KP, KI, KD, error, self.errorSum, self.prevError)
            correction = min(max(correction, MINCORRECTION_DRIVE), MAXCORRECTION_DRIVE)

            self.move(speed, correction)

        if stopBool:
            self.eBrake(stopDuration)

    def remoteControl(self):
        key = ""
        theta = 0
        vel = 0
        while True:
            if keys.poll(0):
                key = stdin.read(1)
                if key == "w": 
                    vel = 1000
                if key == "s": 
                    vel = -800
                if key == "a": 
                    theta -= 40
                    if theta < -40:
                        theta = -40
                if key == "q":
                    theta = 0
                if key == "d": 
                    theta += 40
                    if theta > 40:
                        theta = 40
                if key == " ":
                    vel = 0

            self.move(vel, theta)


# # Avoid Misdownload of Code
if __name__ == "__main__":
    from test import *
    # OpenChallenge()
