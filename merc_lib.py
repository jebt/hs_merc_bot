import pyautogui
import time


def click(location):
    pyautogui.moveTo(*location, duration=0.25)
    pyautogui.click(x=location[0], y=location[1])


def wait(delay):
    time.sleep(delay)
