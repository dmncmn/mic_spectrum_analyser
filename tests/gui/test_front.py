
import sys
import subprocess
import time
import pytest
import pyautogui

from tests.methods.utils import *


@pytest.fixture
def setup():
    subprocess.Popen([sys.executable, 'main.py', '--device=Mock'])
    time.sleep(5)


@pytest.fixture
def teardown():
    yield
    pyautogui.hotkey('alt', 'F4')


@pytest.mark.parametrize("offset_x, offset_y",
                         [(0, 100), (100, 0), (100, 100),
                          (0, -100), (-100, 0), (-100, -100)])
def test_front_draggable_window(setup, teardown, offset_x, offset_y):
    """
    Check that the window is moved by holding down the left mouse button
    """
    cursor_pos: tuple
    new_app_pos: tuple
    offset: tuple = offset_x, offset_y
    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    cursor_pos = get_new_position(DEFAULT_APP_REGION, DEFAULT_CLICK_POINT)
    pyautogui.moveTo(cursor_pos)
    cursor_pos = get_new_position(cursor_pos, offset)
    pyautogui.dragTo(cursor_pos)
    new_app_pos = get_new_position(DEFAULT_APP_REGION, offset)
    pyautogui.screenshot(screenshots[1], region=new_app_pos)
    try:
        assert images_are_similar(*screenshots), \
            "Images differ"
    except AssertionError as e:
        raise e
    finally:
        remove_image(screenshots[0])
        remove_image(screenshots[1])


def test_close_button(setup):
    """
    Check that the window closes by click the close button
    """
    cursor_pos: tuple
    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    cursor_pos = get_new_position(DEFAULT_APP_REGION, CLOSE_BUTTON_CLICK_POINT)
    pyautogui.moveTo(cursor_pos)
    pyautogui.click()
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)
    try:
        assert not images_are_similar(*screenshots), \
            "Images do not differ"
    except AssertionError as e:
        raise e
    finally:
        remove_image(screenshots[0])
        remove_image(screenshots[1])
