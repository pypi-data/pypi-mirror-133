from threading import Event

import time
import datetime
from pynput.keyboard import Controller, Key, Listener


def get_target_time(time):
    """
    Get a datime object for the next occurence of the given time

    Args:
        time (str): An ISO time (e.g.: "08:30").

    Returns:
        datetime.datetime: Datetime of the next occurrence of such a time.

    """
    target_time = datetime.datetime.combine(datetime.date.today(), datetime.time.fromisoformat(time))
    if target_time < datetime.datetime.now():
        target_time += datetime.timedelta(days=1)

    return target_time


# Stop flag
repeat = True
# Sleep event
sleep = Event()


def on_press(key):
    """Handler to mark the stop flag when ESC is pressed"""
    global repeat, sleep
    if key == Key.esc:
        repeat = False
        sleep.set()


listener = Listener(on_press=on_press)

listener.start()

keyboard = Controller()


def activity(sleep_time=10, stop_time=None, monitor=None):
    """

    Args:
        sleep_time (float): Time to sleep between actions.
        stop_time (datetime.datetime): A time to stop.
        monitor (callable): A function to call after every step.

    """
    global repeat
    repeat = True
    while repeat:
        sleep.wait(sleep_time)
        if not repeat:  # If pressed during sleep
            break

        if stop_time is not None and datetime.datetime.now() >= stop_time:
            repeat = False
            break

        with keyboard.pressed(Key.ctrl):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)

        time.sleep(0.5)

        with keyboard.pressed(Key.ctrl):
            with keyboard.pressed(Key.shift):
                keyboard.press(Key.tab)
                keyboard.release(Key.tab)

        if monitor is not None:
            monitor()
