
import sys
import subprocess
import time
import pytest
import pyautogui

from src.styles import *
from PIL import Image, ImageChops
from functools import wraps

DESKTOP_RESOLUTION: tuple = 1920, 1080
DEFAULT_APP_REGION: tuple = (
    (DESKTOP_RESOLUTION[0] - WINDOW_WIDTH) // 2,
    (DESKTOP_RESOLUTION[1] - WINDOW_HEIGHT) // 2,
    WINDOW_WIDTH, WINDOW_HEIGHT)


@pytest.fixture
def setup():
    """
    Setup fixture that opens and closes the app
    """
    subprocess.Popen([sys.executable, 'main.py'])
    time.sleep(5)
    yield
    pyautogui.hotkey('alt', 'F4')


def compare(similar: bool = True,
            picture_1: str = "1.png",
            picture_2: str = "2.png"):
    """
    Custom decorator to compare pictures
    """
    def dec(func):
        @wraps(func)
        def wrapper(setup):
            pyautogui.screenshot(picture_1, region=DEFAULT_APP_REGION)
            func(setup)
            pyautogui.screenshot(picture_2, region=DEFAULT_APP_REGION)
            before, after = Image.open(picture_1), Image.open(picture_2)
            diff = ImageChops.difference(before, after).getbbox()
            assert bool(diff) != similar
        return wrapper
    return dec


@compare(similar=True, picture_1="tests/pics/window.png")
def test_front_opened_window(setup):
    """
    Check that the window opens
    """
    ...


@compare(similar=False)
def test_front_draggable_window(setup):
    """
    Check that the window drags by left click
    """
    position_1: tuple = DEFAULT_APP_REGION[0]+10, DEFAULT_APP_REGION[1]+10
    position_2: tuple = DEFAULT_APP_REGION[0]+100, DEFAULT_APP_REGION[1]+100
    pyautogui.moveTo(position_1)
    pyautogui.dragTo(position_2, button='left')


@compare(similar=False)
def test_front_fullscreen_window(setup):
    """
    Check that the window opens in full screen by double click
    """
    position: tuple = DEFAULT_APP_REGION[0]+10, DEFAULT_APP_REGION[1]+10
    pyautogui.doubleClick(position)


@compare(similar=False)
def test_front_resizable_window(setup):
    """
    Check that window resizes by SizeGrip
    """
    position_1: tuple = DEFAULT_APP_REGION[0] + WINDOW_WIDTH - 15, \
                        DEFAULT_APP_REGION[1] + WINDOW_HEIGHT - 15
    position_2: tuple = DEFAULT_APP_REGION[0] + WINDOW_WIDTH + 100, \
                        DEFAULT_APP_REGION[1] + WINDOW_HEIGHT + 100
    pyautogui.moveTo(position_1)
    pyautogui.click()
    pyautogui.dragTo(position_2, button='left')
