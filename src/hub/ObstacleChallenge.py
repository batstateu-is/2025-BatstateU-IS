from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from dissociating import *

HUB.imu.reset_heading(0)
printInfo()
WALLING_ERROR_TOLERANCE = 4.5
TURNDURATION = 800

def Obstacle():
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.C, Port.D, Port.F)
    sannisLivisa.center()
    direction = sannisLivisa.determineDir()
    
    outAngle = 49 if direction > 0 else -49
    proximity = 50 if direction > 0 else 43

    sannisLivisa.drive(-120, 200, 300, heading=60*direction)
    sannisLivisa.eBrake(200)

    tolerance = 19 if direction > 0 else -20
    targetHeading = abs(HUB.imu.heading()) + 90*direction - tolerance
    log(targetHeading)
    while abs(HUB.imu.heading()) < abs(targetHeading):
        sannisLivisa.move(550, outAngle)

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

    # sannisLivisa.drive(20, 600, 800, heading=60*direction)
    sannisLivisa.eBrake(200)
    print(HUB.imu.heading())
    # sannisLivisa.turn(400, 30*direction, reverse=True)
    sannisLivisa.driveUntilStalled(-500, 600, 800, heading=90*direction)
    HUB.imu.reset_heading(0)

    sannisLivisa.kc()
    if direction > 0:
        return "clockwise"
    else:
        pass

def format_ms(ms):
    minutes = ms // 60000
    seconds = (ms % 60000) // 1000
    millis = ms % 1000
    return f"{minutes}m {seconds}s {millis}ms"

from ObstacleClockwise import Clockwise
from ObstacleCounter import Counter

def main():
    timer = StopWatch()
    timer.reset()
    timer.resume()
    file = Obstacle()
    
    
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.C, Port.D, Port.F)
    if file == "clockwise":
        Clockwise(sannisLivisa)
    else:
        Counter(sannisLivisa)

    timer.pause()
    print(format_ms(timer.time()))

if __name__ == "__main__":
    main()