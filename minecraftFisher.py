
import mss
import mss.tools
import numpy as np
# import cv2 as cv
from PIL import Image
# import matplotlib.pyplot as plt
import time
import pyautogui
import keyboard
import sys

terminateProgram = False
pauseProgram = False

def getImage():
    screenshot = sct.grab(screenshotArea)
    image = Image.frombytes('RGB', screenshot.size,
                            screenshot.bgra, 'raw', 'BGRX')
    return np.array(image)


def hasBobber():
    image = getImage()
    shape = np.shape(image)
    for x in range(shape[0]):
        for y in range(shape[1]):
            red = image.item(x, y, 0)
            if red > 160 and image.item(x, y, 1) < 130 and image.item(x, y, 2) < 130:
                return True
    return False


def terminate():
    print('Terminating program.')
    global terminateProgram
    terminateProgram = True


def pause():
    global pauseProgram
    pauseProgram = not pauseProgram
    if not pauseProgram:
        print("Resuming fishing.")
    else:
        print("Pausing fishing. Press \'g\' to resume.")
        # reel in
        if hasBobber():
            pyautogui.rightClick()

def cast():
    pyautogui.rightClick()
    time.sleep(2.10) # wait for bobber to settle

print("Press \'g\' to begin fishing.")
keyboard.wait('g')
print("Beginning fishing. Press \'g\' to pause and \'control + g\' to terminate.")

keyboard.add_hotkey('ctrl+g', terminate)
keyboard.add_hotkey('g', pause)

with mss.mss() as sct:
    monitor = sct.monitors[1]

    screenshotArea = {
        # 100px from the top
        "top": int(monitor["top"] + (monitor["height"] - monitor["height"] * 0.4) / 2),
        # 100px from the left
        "left": int(monitor["left"] + (monitor["width"] - monitor["width"] * 0.25) / 2),
        "height": int(monitor["height"] * 0.4),
        "width": int(monitor["width"] * 0.25)
    }

    # initial cast
    if not hasBobber():
        cast()

    caught = False
    while not terminateProgram:
        if pauseProgram:
            time.sleep(0.45)
            continue

        if not hasBobber():
            if caught:
                cast()
                continue

            pyautogui.rightClick()
            time.sleep(0.5) # wait for item to reel in
            cast()
            caught = True
        else:
            caught = False
    sys.exit()
