import pyautogui
import time
from logging import info


def click(location):
    pyautogui.moveTo(*location, duration=0.25)
    pyautogui.click(x=location[0], y=location[1])


def wait(delay):
    time.sleep(delay)


def detect(image):
    location = pyautogui.locateCenterOnScreen(image, confidence=0.9)
    if location:
        info(f"Detected {image.filename} on screen.")
        return location
