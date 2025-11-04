from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from dissociating import *

HUB.imu.reset_heading(0)
printInfo()
WALLING_ERROR_TOLERANCE = 9.5
TURNDURATION = 1000

def Obstacle():
    sannisLivisa = FE(Port.A, Port.B, Port.C, Port.F, Port.D, Port.E, camEnabled=True)
    sannisLivisa.distSensor.lights.on()
    sannisLivisa.center()
    direction = sannisLivisa.determineDir()
    
    outAngle = 49 if direction > 0 else -49
    proximity = 50 if direction > 0 else 43
    # sannisLivisa.drive(-120, 200, 300, heading=60*direction)
    # sannisLivisa.driveUntilProximity(-120, 60, heading=60*direction, selection="back")

    tolerance = 19 if direction > 0 else 20
    if direction > 0:
        sannisLivisa.reverseUntilAngleOrWall(200, 16, 40)
        targetHeading = HUB.imu.heading() + 80 - tolerance
        while HUB.imu.heading() < targetHeading:
            sannisLivisa.move(550, outAngle)
    else:
        sannisLivisa.reverseUntilAngleOrWall(200, -22, 40)
        targetHeading = HUB.imu.heading() - 80 + tolerance
        while HUB.imu.heading() > targetHeading:
            sannisLivisa.move(550, outAngle)


    # sannisLivisa.drive(20, 600, 800, heading=60*direction)
    sannisLivisa.eBrake(200)
    print(HUB.imu.heading())
    # sannisLivisa.turn(400, 30*direction, reverse=True)
    sannisLivisa.driveUntilStalled(-410, 400, 500, heading=90*direction)

    # -- Correct if not flush with wall -- #
    checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 10, 600, 90 * direction, TURNDURATION, 40 * direction)

    
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
    
    sannisLivisa = FE(Port.A, Port.B, Port.C, Port.F, Port.D, Port.E, camEnabled=True)
    if file == "clockwise":
        Clockwise(sannisLivisa)
    else:
        Counter(sannisLivisa)

    timer.pause()
    print(format_ms(timer.time()))

if __name__ == "__main__":
    main()
