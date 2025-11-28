from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from dissociating import *

HUB.imu.reset_heading(0)
printInfo()
WALLING_ERROR_TOLERANCE = 7.5
TURNDURATION = 1000
NOWALLING = False

def Obstacle(sannisLivisa):
    # sannisLivisa = FE(Port.A, Port.B, Port.C, Port.F, Port.D, Port.E, camEnabled=True)
    sannisLivisa.distSensor.lights.off()
    sannisLivisa.center()
    direction = sannisLivisa.determineDir()
    
    outAngle = 49 if direction > 0 else -49
    proximity = 50 if direction > 0 else 43
    # sannisLivisa.drive(-120, 200, 300, heading=60*direction)
    # sannisLivisa.driveUntilProximity(-120, 60, heading=60*direction, selection="back")

    tolerance = 19 if direction > 0 else 20
    if direction > 0:
        sannisLivisa.reverseUntilAngleOrWall(180, 35, 53, maxDist=90)
        # sannisLivisa.turn(250, 32, True)
        sannisLivisa.getDistance(BACK)
        targetHeading = HUB.imu.heading() + 70 - tolerance
        while HUB.imu.heading() < targetHeading:
            sannisLivisa.move(550, outAngle)
        # sannisLivisa.drive(90, 600, 800, heading=92*direction)
        sannisLivisa.eBrake(200)
        sannisLivisa.turn(500, 97, True)
    else:
        sannisLivisa.reverseUntilAngleOrWall(200, -30, 65, maxDist=90)
        # sannisLivisa.turn(250, -30, True)
        targetHeading = HUB.imu.heading() - 70 + tolerance
        while HUB.imu.heading() > targetHeading:
            sannisLivisa.move(550, outAngle)
        sannisLivisa.turn(500, -95, True)


    # print(HUB.imu.heading())
    # sannisLivisa.turn(400, 30*direction, reverse=True)
    sannisLivisa.drive(100, 500, 600, heading=90*direction)
    sannisLivisa.driveUntilStalled(-250, 500, 600, heading=90*direction)

    
    # -- Correct if not flush with wall -- #
    # checkIfFlushWithWall(sannisLivisa, WALLING_ERROR_TOLERANCE, 10, 600, 90 * direction, TURNDURATION, 40 * direction)

    
    sannisLivisa.eBrake(200)

    # sannisLivisa.kc()
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
from ObsClockwiseNoWall import ClockwiseNoWall
from ObsCounterNoWall import CounterNoWall

def main():
    timer = StopWatch()
    timer.reset()
    timer.resume()
    
    sannisLivisa = FE(Port.A, Port.B, Port.E, Port.F, Port.D, Port.C, camEnabled=True)
    file = Obstacle(sannisLivisa)
    HUB.imu.reset_heading(0)
    if not NOWALLING:
        if file == "clockwise":
            Clockwise(sannisLivisa)
        else:
            Counter(sannisLivisa)

    else:
        beep()
        if file == "clockwise":
            ClockwiseNoWall(sannisLivisa)
        else:
            CounterNoWall(sannisLivisa)

    timer.pause()
    print(format_ms(timer.time()))

if __name__ == "__main__":
    # wait(5000)
    main()
