from machine import Pin, time_pulse_us
from pupremote import PUPRemoteSensor
import time

pr = PUPRemoteSensor(power=False)
pr.add_channel('line', 'hhh')
pr.process()

# --- Setup Ultrasonic Sensors ---
# Sensor 1: Trig = GPIO 21, Echo = GPIO 20
trig1 = Pin(21, Pin.OUT)
echo1 = Pin(22, Pin.IN)

# Sensor 2: Trig = GPIO 32, Echo = GPIO 33
trig2 = Pin(32, Pin.OUT)
echo2 = Pin(33, Pin.IN)

trig3 = Pin(26, Pin.OUT)
echo3 = Pin(27, Pin.IN)

# --- Distance Measurement Function (returns mm) ---
def getDistance(trig, echo):
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    try:
        duration = time_pulse_us(echo, 1, 800000)  # timeout 30 ms
        
        distanceMm = (duration / 2) / 2.91
        return int(distanceMm)
    except OSError:
        return -1

while True:
    distance1 = getDistance(trig1, echo1)
    distance2 = getDistance(trig2, echo2)
    distance3 = getDistance(trig3, echo3)

    # print("Sensor1:", distance1, "mm | Sensor2:", distance2, "mm", "| Sensor3:", distance2, "mm")

    # Send data to SPIKE hub
    pr.update_channel('line', distance1, distance2, distance3)
    pr.process()

    time.sleep(0.05)

