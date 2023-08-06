# Actions to keep activity

import time
from random import randint

from pynput.keyboard import Controller, Key
from pynput.mouse import Controller as MouseController

keyboard = Controller()
mouse = MouseController()


def control_tab():
    with keyboard.pressed(Key.ctrl):
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)


def wiggle_mouse():
    position = mouse.position
    mouse.move(randint(-5, 5), randint(-5, 5))
    time.sleep(0.5)
    mouse.position = position


def shift():
    keyboard.press(Key.shift)
    time.sleep(0.1)
    keyboard.release(Key.shift)


actions = {"control-tab": control_tab, "wiggle-mouse": wiggle_mouse, "shift": shift}
action_descriptions = {"control-tab": "Press Ctrl+Tab (cycle tabs)",
                       "wiggle-mouse": "Slightly move the mouse, returning to the original position",
                       "shift": "Press and release shift"}
