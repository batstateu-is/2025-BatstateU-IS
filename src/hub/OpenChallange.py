from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from umath import ceil
import umath
from dissociating import *

HUB.imu.reset_heading(0)
printInfo()

def determineDirection(sannisLivisa: FE):
    sannisLivisa.driveUntilProximity(500, 430, heading=0)
    sannisLivisa.eBrake(100)

    return sannisLivisa.determineDir()

# print()

def OpenChallenge():
    MAXSPEED = 2000
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.C, Port.D, Port.F, camEnabled=False)
    sannisLivisa.center()
    # direction = sannisLivisa.driveUntilLine(500, 400, 500)
    direction = determineDirection(sannisLivisa)
    print("STARTED CLOCKWISE" if direction > 0 else "STARTED COUNTERCLOCKWISE")

    sannisLivisa.center()

    # Direction-specific constants
    targetProximity = 535 if direction > 0 else 578
    endTarget = 1610 if direction > 0 else 1380

    currentLap = 0
    targetHeading = 0

    sannisLivisa.forwardTurnRightTolerance = 16
    sannisLivisa.forwardTurnLeftTolerance  = 18

    KDdrive = sannisLivisa.KDdrive
    
    lightList = [100, 0, 100, 0] if direction > 0 else [0, 100, 0, 100]
    if direction > 0:
        baseKP = 0.81
        KI = 0.00024
        turnErrorKp = 0.31
        turnErrorKd = 0.066
    else:
        baseKP = 0.8
        KI = 0.00015
        turnErrorKp = 0.45
        turnErrorKd = 0.09

    while currentLap < 3:
        sannisLivisa.resetParams()
        log(targetHeading, HUB.imu.heading())
        t = 0  # for blinking animation time

        if currentLap != 0:
            while sannisLivisa.distSensor.distance() > targetProximity:
                error = targetHeading - HUB.imu.heading()
                KP = baseKP
                KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

                sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError, maxSum=355, minSum=355)
                if correction >= 0:
                    correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
                else:
                    correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

                sannisLivisa.move(MAXSPEED, correction)

                brightness = int(50 + 50 * umath.sin(umath.radians(t)))  # value from 0 to 100
                blinkList = [int((b / 100) * brightness) for b in lightList]
                sannisLivisa.distSensor.lights.on(blinkList)

                t = (t + 45) % 360  # increase time, loop every 360 degrees

        sannisLivisa.lookDir(90 * direction, asyncBool=False)
        targetHeading += 90 * direction

        if direction > 0:
            targetHeading += 0.04
        else:
            pass
            targetHeading += -0.13
        
        
        sannisLivisa.resetParams()

        if direction > 0:
            sannisLivisa.distSensor.lights.on([100, 0, 100, 0])
            while HUB.imu.heading() < targetHeading - sannisLivisa.forwardTurnRightTolerance:
                error = targetHeading - HUB.imu.heading()
                sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(turnErrorKp, KI, turnErrorKd, error, sannisLivisa.errorSum, sannisLivisa.prevError)
                correction = 45 if correction > 45 else correction

                if correction < 3:
                    break
                sannisLivisa.move(MAXSPEED, correction)
            sannisLivisa.distSensor.lights.off()
        else:
            sannisLivisa.distSensor.lights.on([0, 100, 0, 100])
            while HUB.imu.heading() > targetHeading + sannisLivisa.forwardTurnLeftTolerance:
                error = targetHeading - HUB.imu.heading()
                # print(error)
                sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(turnErrorKp, KI, turnErrorKd, error, sannisLivisa.errorSum, sannisLivisa.prevError)
                correction = -48 if correction < -48 else correction
                if correction > -3:
                    break
                sannisLivisa.move(MAXSPEED, correction)
            sannisLivisa.distSensor.lights.off()

        currentLap += 0.25
        sannisLivisa.lookDir(0, asyncBool=False, speed=200)

        while abs(sannisLivisa.senseMotor.angle()) > 5:
            error = targetHeading - HUB.imu.heading()
            KP = baseKP
            KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

            sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError, maxSum=355, minSum=355)

            if correction >= 0:
                correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
            else:
                correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction

            sannisLivisa.move(MAXSPEED, correction)

        # HUB.speaker.beep(500)
        beep()

    while abs(sannisLivisa.senseMotor.angle()) > 2 or sannisLivisa.getDistance("front") > endTarget:
        error = targetHeading - HUB.imu.heading()
        KP = baseKP
        KD = linearMap(sannisLivisa.driveMotor.speed(), 0, 1000, 0, KDdrive)

        sannisLivisa.errorSum, sannisLivisa.prevError, correction = pid(KP, KI, KD, error, sannisLivisa.errorSum, sannisLivisa.prevError, maxSum=55, minSum=55)
        if correction >= 0:
            correction = MAXCORRECTION_DRIVE if correction > MAXCORRECTION_DRIVE else correction
        else:
            correction = MINCORRECTION_DRIVE if correction < MINCORRECTION_DRIVE else correction
        sannisLivisa.move(MAXSPEED, correction)

    sannisLivisa.eBrake(1000)

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
        HUB.light.on(Color.BLUE)  # Open Challenge indicator
        OpenChallenge()

    finally:
        timer.pause()
        print(format_ms(timer.time()))
