
import os
import sys
import time
import pytest
import pyautogui
import subprocess
import Xlib.display
from typing import Generator
from pyvirtualdisplay.display import Display
from tests.methods.utils import get_new_position
from tests.methods.positions import DEFAULT_APP_REGION, DEFAULT_CLICK_POINT


pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])
d = Display(visible=True, size=(1920, 1080), backend="xvfb", use_xauth=True)
d.start()


@pytest.fixture
def setup() -> Generator:
    """ Run app """
    p = subprocess.Popen([sys.executable, 'main.py', '--device=Mock'])
    time.sleep(1)
    """ Set cursor to default position """
    cursor_pos = get_new_position(DEFAULT_APP_REGION, DEFAULT_CLICK_POINT)
    pyautogui.moveTo(cursor_pos)
    yield
    """ Close app """
    p.terminate()
