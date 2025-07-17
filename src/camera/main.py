import sensor, time
import pyb
from micropython import const
from pupremote import PUPRemoteSensor

DEBUG = const(False)

redLed = pyb.LED(1)
greenLed = pyb.LED(2)

camera = PUPRemoteSensor(power=True)
camera.add_channel('blob', to_hub_fmt='hhhhhhhh')

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(True)
sensor.set_hmirror(True)

screenWidth = sensor.width()
screenHeight = sensor.height()

roiX = int(0.0 * screenWidth)
roiY = int(0.3 * screenHeight)
roiWidth = screenWidth - roiX * 2
roiHeight = screenHeight - roiY
roi = (roiX, roiY, roiWidth, roiHeight)
print(roi)

sensor.set_windowing(roi)
sensor.set_framerate(1000)
sensor.skip_frames(time=500)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False, exposure_us=14000)

greenThreshold = (0, 60, -128, -15, -128, 127)
redThreshold = const((0, 35, 0, 127, 1, 127))

targetGreen = (int(screenWidth * 0.9), 120)
targetRed = (int(screenWidth * 0.17), screenHeight * 2 // 3)

def findDominantBlob(blobs, roiHeight):
    bestBlob = None
    maxPixels = 0
    for b in blobs:
        if (b.h() > b.w() or (b.y() + b.h()) == roiHeight) and b.pixels() > maxPixels:
            bestBlob = b
            maxPixels = b.pixels()
    return bestBlob

def indicateBlob(gPixels, rPixels):
    if gPixels > rPixels:
        greenLed.on()
        redLed.off()
    elif rPixels > gPixels:
        redLed.on()
        greenLed.off()
    else:
        redLed.off()
        greenLed.off()

while True:
    img = sensor.snapshot()

    greenBlobs = img.find_blobs([greenThreshold], pixels_threshold=250)
    greenBlob = findDominantBlob(greenBlobs, roiHeight)
    greenCx, greenCy, greenPixels = 0, 0, 0
    if greenBlob:
        greenCx = greenBlob.cx()
        greenCy = greenBlob.cy()
        greenPixels = greenBlob.pixels()
        # img.draw_rectangle(greenBlob.rect(), color=(218, 66, 44), thickness=1)

    redBlobs = img.find_blobs([redThreshold], pixels_threshold=250)
    redBlob = findDominantBlob(redBlobs, roiHeight)
    redCx, redCy, redPixels = 0, 0, 0
    if redBlob:
        redCx = redBlob.cx()
        redCy = redBlob.cy()
        redPixels = redBlob.pixels()
        # img.draw_rectangle(redBlob.rect(), color=(68, 214, 44), thickness=1)

    indicateBlob(greenPixels, redPixels)
    targetX = greenCx if greenPixels > redPixels else redCx

    print(greenCx, greenCy, greenPixels, redCx, redCy, redPixels)
    camera.update_channel('blob', greenCx, greenCy, greenPixels, redCx, redCy, redPixels)
    camera.process()