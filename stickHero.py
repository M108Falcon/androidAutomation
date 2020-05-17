import numpy
from PIL import Image
from ppadb.client import Client         # ADB api, lets you integrate adb shell with python
import time

# Setting up adb shell service
adb = Client(host="127.0.0.1", port = 5037)     # default hostname = localhost, default port = 5037
devices = adb.devices()                         # initalise adb module

# Method checks if devices are connected
if len(devices) == 0:
    print("No device Connected")
    quit()

device = devices[0]                             # If device detected, make it primary device.

# driver program
while True:
    image = device.screencap()                  # Take screenshot of mobile device

    with open("screen.png", "wb") as f:         # Open Screenshot as binary file and write to it
        f.write(image)
        
    image = Image.open("screen.png")            
    image = numpy.array(image, dtype = numpy.uint8)     # convert image into numpy array

    # Following method looks for black pixels in pillars, :3 represents to include only rgb values and not alpha values
    # 1680 was my screen's Y coordinate from where black pillar started, adjust the value according to your screen.
    pixels = [list(i[:3]) for i in image[1680]]                 
    
    # Finding transition from black pixel in pillar to color to again black pixel in pillars
    transitions = []
    ignore = True
    black = True

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        # Finding last black pixel in first pillar(widthwise)
        if ignore and (r+g+b) != 0:
            continue
        ignore = False

        #Finding transition to color
        if black and (r+g+b) != 0:
            black = not black
            transitions.append(i)
            continue

        # Finding transtition back to black
        if not black and (r+g+b) == 0:
            black = not black
            transitions.append(i)
            continue

    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 -target1
    center = (gap + target/2) * 0.99 # Distance formula and then getting 99% of distance to improve accuracy a bit
    print(center)

    # I calculated the time required to hold the screen to print required length of pixels,
    # It came out to be 1 pixel/millisecond so we can directly substitue value of required distance
    device.shell(f"input touchscreen swipe 600 600 600 600 {int(center)}")
    time.sleep(2.5)
