import numpy
from PIL import Image
from ppadb.client import Client
import time

adb = Client(host="127.0.0.1", port = 5037)
devices = adb.devices()

if len(devices) == 0:
    print("No device Connected")
    quit()

device = devices[0]
while True:
    image = device.screencap()

    with open("screen.png", "wb") as f:
        f.write(image)
        
    image = Image.open("screen.png")
    image = numpy.array(image, dtype = numpy.uint8)

    pixels = [list(i[:3]) for i in image[1680]]

    transitions = []
    ignore = True
    black = True

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        if ignore and (r+g+b) != 0:
            continue
        ignore = False

        if black and (r+g+b) != 0:
            black = not black
            transitions.append(i)
            continue

        if not black and (r+g+b) == 0:
            black = not black
            transitions.append(i)
            continue

    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 -target1
    center = gap + target/2
    print(center)

    device.shell(f"input touchscreen swipe 600 600 600 600 {int(center)}")
    time.sleep(2.5)
