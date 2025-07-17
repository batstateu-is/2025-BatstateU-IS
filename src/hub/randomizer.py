# Code for Randomization of Game Field

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from urandom import randint
from dissociating import clearOutput

hub = PrimeHub()
clearOutput()

def strongRandom36():
    total = 0
    for _ in range(10):
        total ^= randint(0, 255)
        total += int(hub.imu.heading())
        total ^= randint(0, 255)
        wait(1)
    return 1 + (abs(total) % 36)

def coin_flip():
    return "Heads" if randint(0, 1) == 0 else "Tails"

# Return the Positioni of Obstacles on Field
for _ in range(4):
    print(strongRandom36())
    wait(200)

print(f"{coin_flip()}+{coin_flip()}")

