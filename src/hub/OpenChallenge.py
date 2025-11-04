from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from umath import ceil
from dissociating import *
printInfo()

def turnLeft(sannisLivisa, targetHeading, turnErrorKp, KI, turnErrorKd, MAXSPEED, turnTolerance):
    # global turnTolerance
    sannisLivisa.distSensor.lights.on([100, 0, 100, 0])
    while HUB.imu.heading() > targetHeading + turnTolerance:
        error = targetHeading - HUB.imu.heading()
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(
            turnErrorKp, KI, turnErrorKd, error,
            sannisLivisa.errorSum, sannisLivisa.prevError
        )
        correction = -48 if correction < -48 else correction
        sannisLivisa.move(MAXSPEED, correction)
    sannisLivisa.distSensor.lights.off()

def turnRight(sannisLivisa, targetHeading, turnErrorKp, KI, turnErrorKd, MAXSPEED, turnTolerance):
    # global turnTolerance
    sannisLivisa.distSensor.lights.on([0, 100, 0, 100])
    while HUB.imu.heading() < targetHeading - turnTolerance:
        error = targetHeading - HUB.imu.heading()
        # print(error)
        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(
            turnErrorKp, KI, turnErrorKd, error,
            sannisLivisa.errorSum, sannisLivisa.prevError
        )
        correction = 45 if correction > 45 else correction
        sannisLivisa.move(MAXSPEED, correction)
    sannisLivisa.distSensor.lights.off()

def OpenChallenge():
    HUB.imu.reset_heading(0)
    MAXSPEED = 770
    sannisLivisa = FE(Port.A, Port.B, Port.C, Port.F, Port.D, Port.E, camEnabled=True)
    sannisLivisa.distSensor.lights.on([100, 100, 100, 100])
    sannisLivisa.center()

    #TODO, fallback if no direction detected, use old if too close to wall (Not Done)

    direction = sannisLivisa.driveDeterminDir(500, 600, 700, decelerate=True, sideThreshold=600, frontThreshold=350)
    
    print("STARTED CLOCKWISE" if direction > 0 else "STARTED COUNTERCLOCKWISE")

    currentLap = 0
    targetHeading = 0

    sannisLivisa.forwardTurnRightTolerance = 16
    sannisLivisa.forwardTurnLeftTolerance  = 19
    KDdrive = sannisLivisa.KDdrive

    # -------------------------------
    # Direction-specific configuration
    # -------------------------------
    if direction > 0:
        baseKP = 4.15
        KI = 0.0000004
        turnErrorKp = 0.98
        turnErrorKd = 0.04
        distSensor = RIGHT
        targetProximity = 645
        targetProximityFront = 505
        safetyDistance = 705
        endTarget = 1610
        minimumDistance = 300
        leftThreshold = 150
        rightThreshold = 40

        turnTolerance = sannisLivisa.forwardTurnRightTolerance
        lightList = [0, 100, 0, 100]
        turnFunc = turnRight

    else:
        baseKP = 4.6
        KI = 0.0000004
        turnErrorKp = 0.97
        turnErrorKd = 0.02
        distSensor = LEFT
        targetProximity = 638
        targetProximityFront = 618
        safetyDistance = 718
        minimumDistance = 300
        endTarget = 1380
        leftThreshold = 60
        rightThreshold = 150

        turnTolerance = sannisLivisa.forwardTurnLeftTolerance
        lightList = [100, 0, 100, 0]
        turnFunc = turnLeft

    otherSafetyDistance = 1000
    sannisLivisa.KDdrive = 0.08

    sannisLivisa.senseMotor.run_target(1000, 0, wait=False)

    # -------------------------------
    # Main Lap Loop
    # -------------------------------
    while currentLap < 3:
        t = 0
        correction = 0
        if currentLap == 0:
            targetHeading += 90 * direction
            if direction < 0:
                targetHeading -= 0.9

            sannisLivisa.resetParams()
            turnFunc(sannisLivisa, targetHeading, turnErrorKp, KI, turnErrorKd, MAXSPEED, turnTolerance)
            currentLap += 0.25
            continue

        elif currentLap <= 1:
            lastRot = sannisLivisa.driveMotor.angle()
            distTraveled = 0

            while sannisLivisa.getDistance(FRONT) < safetyDistance or distTraveled < otherSafetyDistance:
                leftAdjust = 0
                rightAdjust = 0

                if sannisLivisa.getDistance(LEFT) < leftThreshold or sannisLivisa.getDistance(RIGHT) < rightThreshold:
                    leftAdjust = sannisLivisa.getDistance(LEFT)
                    rightAdjust = sannisLivisa.getDistance(RIGHT)

                error = rightAdjust + targetHeading - HUB.imu.heading() - leftAdjust
                KP = baseKP
                KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

                sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(
                    KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError,
                    maxSum=355, minSum=-355
                )

                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                # print(correction, error, leftAdjust, rightAdjust, targetHeading - HUB.imu.heading())
                sannisLivisa.move(MAXSPEED, correction)
                distTraveled = sannisLivisa.driveMotor.angle() - lastRot

            while sannisLivisa.getDistance(distSensor) < targetProximity and sannisLivisa.getDistance("front") > targetProximityFront:
                leftAdjust = 0
                rightAdjust = 0

                if sannisLivisa.getDistance(LEFT) < leftThreshold or sannisLivisa.getDistance(RIGHT) < rightThreshold:
                    leftAdjust = sannisLivisa.getDistance(LEFT)
                    rightAdjust = sannisLivisa.getDistance(RIGHT)

                error = rightAdjust + targetHeading - HUB.imu.heading() - leftAdjust
                KP = baseKP
                KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

                sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(
                    KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError,
                    maxSum=355, minSum=-355
                )

                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
                sannisLivisa.move(MAXSPEED, correction)

            distTraveled = sannisLivisa.driveMotor.angle() - lastRot
            # roundedDist = ceil(distTraveled / 100) * 100
            roundedDist = distTraveled

            sannisLivisa.record(str(currentLap)[1::], roundedDist + 30)
            # log(f"Recorded Distance (Rounded): {roundedDist}, (Not Rounded): {distTraveled}", level="INFO")

            # print(f"sannisLivisa.getDistance(distSensor) < targetProximity: {sannisLivisa.getDistance(distSensor) < targetProximity}")
            # print(f"sannisLivisa.getDistance(\"front\") > targetProximityFront: {sannisLivisa.getDistance('front') > targetProximityFront}")

        else:
            #TODO, remeber  the recorded distance ( GOOD )
            lastRot = sannisLivisa.driveMotor.angle()
            distTraveled = 0
            distToTravel = sannisLivisa.remember(str(currentLap)[1::])
            while distTraveled < distToTravel and \
                    sannisLivisa.getDistance("front") > minimumDistance:
                leftAdjust = 0
                rightAdjust = 0
                distTraveled = sannisLivisa.driveMotor.angle() - lastRot
                if sannisLivisa.getDistance(LEFT) < leftThreshold or sannisLivisa.getDistance(RIGHT) < rightThreshold:
                    leftAdjust = sannisLivisa.getDistance(LEFT)
                    rightAdjust = sannisLivisa.getDistance(RIGHT)

                error = rightAdjust + targetHeading - HUB.imu.heading() - leftAdjust
                KP = baseKP
                KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

                sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(
                    KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError,
                    maxSum=355, minSum=-355
                )

                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
                # print(MAXSPEED, correction)
                sannisLivisa.move(MAXSPEED, correction)

        print(HUB.imu.heading(), targetHeading, 90*direction)
        targetHeading += 90 * direction

        if direction < 0:
            targetHeading -= 0.12
        else:
            targetHeading += 0.25

        # sannisLivisa.resetParams()
        turnFunc(sannisLivisa, targetHeading, turnErrorKp, KI, turnErrorKd, MAXSPEED, turnTolerance)
        currentLap += 0.25

    # -------------------------------
    # Final Centering
    # -------------------------------
    sannisLivisa.drive(300, MAXSPEED, MAXSPEED - 100, heading=targetHeading)
    while sannisLivisa.getDistance("front") > endTarget:
        error = targetHeading - HUB.imu.heading()
        KP = baseKP
        KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(
            KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError,
            maxSum=55, minSum=-55
        )

        correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
        correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
        sannisLivisa.move(MAXSPEED, correction)

    sannisLivisa.eBrake(1000)
    print(sannisLivisa.memory, sannisLivisa.getDistance(FRONT))


def format_ms(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    millis = ms % 1000
    return f"{minutes}m {seconds}s {millis}ms"


if __name__ == "__main__":
    try:
        timer = StopWatch()
        timer.reset()
        timer.resume()
        HUB.display.off()
        HUB.light.on(Color.BLUE)
        OpenChallenge()
    finally:
        timer.pause()
        print(format_ms(timer.time()))
