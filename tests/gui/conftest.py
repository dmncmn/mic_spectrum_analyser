
import sys
import time
import pytest
import pyautogui
import subprocess

from tests.methods.utils import *
from tests.methods.positions import *


@pytest.fixture
def setup():
    """ Run app """
    subprocess.Popen([sys.executable, 'main.py', '--device=Mock'])
    time.sleep(3)
    """ Set cursor to default position """
    cursor_pos = get_new_position(DEFAULT_APP_REGION, DEFAULT_CLICK_POINT)
    pyautogui.moveTo(cursor_pos)


@pytest.fixture
def teardown():
    """ Close app """
    yield
    pyautogui.hotkey('alt', 'F4')


@pytest.fixture
def assert_screenshots(same):
    """ Assert screenshots pair and remove them """
    yield
    try:
        assert images_are_similar(*screenshots) == same
    except AssertionError as e:
        raise e
    finally:
        remove_image(screenshots[0])
        remove_image(screenshots[1])
