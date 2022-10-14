
import pytest
import pyautogui
from tests.methods.utils import *
from tests.methods.positions import *


@pytest.mark.parametrize('same', [True])
@pytest.mark.parametrize("offset_x, offset_y",
                         [(0, 100), (100, 0), (100, 100),
                          (0, -100), (-100, 0), (-100, -100)])
def test_front_draggable_window(setup, teardown, assert_screenshots,
                                same, offset_x, offset_y):
    """
    Check that the window is moved by holding down the left mouse button
    """
    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)

    pyautogui.moveTo(get_new_position(DEFAULT_APP_REGION, DEFAULT_CLICK_POINT))
    cursor_pos = get_new_position(DEFAULT_APP_REGION, DEFAULT_CLICK_POINT)
    cursor_pos = get_new_position(cursor_pos, (offset_x, offset_y))
    pyautogui.dragTo(cursor_pos)

    new_app_pos = get_new_position(DEFAULT_APP_REGION, (offset_x, offset_y))
    pyautogui.screenshot(screenshots[1], region=new_app_pos)


@pytest.mark.parametrize('same', [False])
def test_front_close_button(setup, assert_screenshots, same):
    """
    Check that the window closes by click the close button
    """
    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    pyautogui.click(get_new_position(DEFAULT_APP_REGION, CLOSE_BUTTON_CLICK_POINT))
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)


@pytest.mark.parametrize('same', [False])
@pytest.mark.parametrize("up_down", [-1, 1])
def test_front_change_opacity_up_down(setup, teardown, assert_screenshots,
                                      same, up_down):
    """
    Check that the window opacity changes by wheel
    """
    pyautogui.scroll(-1)

    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    pyautogui.scroll(up_down)
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)


@pytest.mark.parametrize('same', [False])
def test_front_window_full_screen_on(setup, teardown, assert_screenshots,
                                     same):
    """
    Check that the window opens at full screen
    by double click
    """

    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    pyautogui.doubleClick()
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)


@pytest.mark.parametrize('same', [False])
def test_front_window_full_screen_off(setup, teardown, assert_screenshots,
                                      same):
    """
    Check that the window returns to normal from full screen
    by double click
    """
    pyautogui.doubleClick()

    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    pyautogui.doubleClick()
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)


@pytest.mark.parametrize('same', [False])
@pytest.mark.parametrize("offset_x", [100, 200])
def test_front_left_slider(setup, teardown, assert_screenshots,
                                  same, offset_x):
    """
    Check that the bar graph changes by left slider
    """
    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    handle_pos = get_new_position(DEFAULT_APP_REGION, LEFT_SLIDER_CLICK_POINT)
    pyautogui.moveTo(handle_pos)
    pyautogui.click()
    pyautogui.dragTo(get_new_position(handle_pos, (offset_x, 0)))
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)


@pytest.mark.parametrize('same', [False])
@pytest.mark.parametrize("offset_x", [100, 200])
def test_front_right_slider(setup, teardown, assert_screenshots,
                            same, offset_x):
    """
    Check that the bar graph changes by right slider
    """
    pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
    handle_pos = get_new_position(DEFAULT_APP_REGION, RIGHT_SLIDER_CLICK_POINT)
    pyautogui.moveTo(handle_pos)
    pyautogui.click()
    pyautogui.dragTo(get_new_position(handle_pos, (offset_x, 0)))
    pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)
