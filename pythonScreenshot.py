import mss
import mss.tools
import numpy
import cv2 as cv
from PIL import Image

with mss.mss() as sct:
    monitor = sct.monitors[1]

    monitor = {
        # 100px from the top
        "top": int(monitor["top"] + (monitor["height"] - monitor["height"] * 0.2) / 2),
        # 100px from the left
        "left": int(monitor["left"] + (monitor["width"] - monitor["width"] * 0.35) / 2),
        "height": int(monitor["height"] * 0.2),
        "width": int(monitor["width"] * 0.35)
    }

    while(True):
        screenshot = numpy.array(sct.grab(monitor))

        screenshot = Image.frombytes('RGB', screenshot.size, screenshot.bgra, 'raw', 'BGRX').tobytes()


        cv.imshow('Computer Vision', screenshot)

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(25) == ord('q'):
            cv.destroyAllWindows()
            break


