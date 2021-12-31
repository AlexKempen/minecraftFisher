import mss
import mss.tools

import numpy as np
import cv2 as cv
from PIL import Image
import matplotlib.pyplot as plt
import time
import pyautogui
import math
import keyboard
import sys

terminateProgram = False
pauseProgram = False

with mss.mss() as sct:
    monitor = sct.monitors[1]

    screenshotArea = {
        "top": int(monitor["top"] + (monitor["height"] - monitor["height"] * 0.5) / 2),
        "left": int(monitor["left"] + (monitor["width"] - monitor["width"] * 0.5) / 2),
        "height": int(monitor["height"] * 0.5),
        "width": int(monitor["width"] * 0.5)
    }


def getImage(area=screenshotArea):
    screenshot = sct.grab(area)
    image = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX')
    return np.array(image)

def bar_percentage(cast_bar_image):
    shape = cast_bar_image.shape
    firstBackPixel = 1
    middleIndex = math.floor(shape[0] / 2)
    for y in range(shape[1]):
        if cast_bar_image.item(middleIndex, y, 2) > 100 and cast_bar_image.item(middleIndex, y, 2) < 150:
            firstBackPixel = y
            break
    return firstBackPixel / shape[1] * 100

def cast_bobber():
    pyautogui.mouseDown(button='left')
    cast_bar_template = cv.imread('castBarTemplate.png',0)
    screen_image = cv.cvtColor(getImage(), cv.COLOR_BGR2GRAY)

    result = cv.matchTemplate(screen_image, cast_bar_template, cv.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    w, h = cast_bar_template.shape[::-1]
    # top_left = max_loc
    # bottom_right  = (top_left[0] + w, top_left[1] + h)
    # cv.rectangle(screen_image, top_left, bottom_right, 255, 3)
    # plt.imshow(screen_image)
    # plt.show()

    cast_bar_area = {
        "top": screenshotArea["top"] + max_loc[1],
        "left": screenshotArea["left"] + max_loc[0],
        "height": h,
        "width": w
    }

    time.sleep(0.6) # wait for the bar to fill up a bit
    while not terminateProgram:
        cast_bar_image = getImage(cast_bar_area)

        bar_percent = bar_percentage(cast_bar_image)
        if (bar_percent > 95):
            break
    
    pyautogui.mouseUp(button='left')
    return cast_bar_area

def has_exclamation_mark(wait_image):
    shape = wait_image.shape
    for x in range(shape[0]):
        for y in range(shape[1]):
            pass


def wait_for_fish(cast_bar_area):
    time.sleep(1.5) # wait for bobber to hit water
    wait_area = {
        "top": int(cast_bar_area["top"] + (cast_bar_area["height"] - monitor["height"] * 0.2) / 2),
        "left": int(cast_bar_area["left"] + (cast_bar_area["width"] - monitor["width"] * 0.075) / 2),
        "height": int(monitor["height"] * 0.2),
        "width": int(monitor["width"] * 0.075)
    }
    template = cv.imread('exclamationMarkTemplate.png', cv.IMREAD_COLOR)

    sum = 0
    count = 0
    while not terminateProgram:
        wait_image = getImage(wait_area)
        result = cv.matchTemplate(wait_image, template, cv.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        max_val /= 10000
        if count <= 15:
            sum += max_val
            count += 1
            continue
        if (max_val - sum/count) > 1.0: # heuristic - depends on template size
            pyautogui.mouseDown(button='left')
            time.sleep(0.1)
            pyautogui.mouseUp(button='left')
            break

# initial catch recognition
def fish_area():
    screenshot = getImage()


def is_junk():
    screenshot = getImage()
    junk_template = cv.imread('junkTemplate.png', cv.IMREAD_COLOR)
    result1 = cv.matchTemplate(screenshot, junk_template, cv.TM_CCOEFF)
    junk_max_val = cv.minMaxLoc(result1)[2]

    fish_game_template = cv.imread('fishGameTemplate.png', cv.IMREAD_COLOR)

def is_legendary_fish(fish_area_image):
    legendary_fish_template = cv.imread('legendaryFishTemplate.png', cv.IMREAD_COLOR)
    result1 = cv.matchTemplate(fish_area_image, legendary_fish_template, cv.TM_CCOEFF)
    legendary_max_val = cv.minMaxLoc(result1)[2]

    fish_template = cv.imread('fishTemplate.png', cv.IMREAD_COLOR)
    result2 = cv.matchTemplate(fish_area_image, fish_template, cv.TM_CCOEFF)
    standard_max_val = cv.minMaxLoc(result2)[2]
    return legendary_max_val / np.size(legendary_fish_template) > standard_max_val / np.size(fish_template) # true if legendary is greater than standard

def bar_size():
    pass

# PID loop recognition
def has_treasure():
    pass

def catch_progress():
    pass

def fish_location():
    pass

def bar_location():
    pass

def catch_fish():
    if is_junk():
        pyautogui.leftClick()
        return
    
    pass
    # win the fishing minigame

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


print("Press \'g\' to begin fishing.")
keyboard.wait('g')
print("Beginning fishing. Press \'g\' to pause and \'control + g\' to terminate.")

keyboard.add_hotkey('ctrl + g', terminate)
keyboard.add_hotkey('g', pause)

while not terminateProgram:
    if pauseProgram:
        time.sleep(0.5)
        continue

    cast_bar_area = cast_bobber()
    wait_for_fish(cast_bar_area)
    pauseProgram = True
    continue
    catch_fish()

sys.exit()
