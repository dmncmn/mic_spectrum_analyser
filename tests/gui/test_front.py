
import allure
import pytest
import pyautogui
from tests.methods.utils import screenshots, allure_attach_screenshot, \
    assert_screenshots, get_new_position
from tests.methods.positions import *


@allure.feature('Test front')
@allure.story('Check that the window is moved by holding down '
              'the left mouse button')
@pytest.mark.parametrize("offset_x, offset_y",
                         [(0, 100), (100, 0), (100, 100),
                          (0, -100), (-100, 0), (-100, -100)])
def test_front_draggable_window(setup, teardown, offset_x, offset_y):

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Drag window to new position"):
        pyautogui.moveTo(get_new_position(DEFAULT_APP_REGION,
                                          DEFAULT_CLICK_POINT))
        cursor_pos = get_new_position(DEFAULT_APP_REGION, DEFAULT_CLICK_POINT)
        cursor_pos = get_new_position(cursor_pos, (offset_x, offset_y))
        pyautogui.dragTo(cursor_pos)

    with allure.step("Take a screenshot"):
        new_app_pos = get_new_position(DEFAULT_APP_REGION, (offset_x, offset_y))
        img = pyautogui.screenshot(screenshots[1], region=new_app_pos)
        allure_attach_screenshot(img)

    with allure.step("Compare screenshots"):
        assert_screenshots(True)


@allure.feature('Test front')
@allure.story('Check that the window closes by click the close button')
def test_front_close_button(setup):

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Click the close button"):
        pyautogui.click(get_new_position(DEFAULT_APP_REGION,
                                         CLOSE_BUTTON_CLICK_POINT))

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Compare screenshots"):
        assert_screenshots(False)


@allure.feature('Test front')
@allure.story('Check that the window opacity changes by wheel')
@pytest.mark.parametrize("up_down", [-1, 1])
def test_front_change_opacity_up_down(setup, teardown, up_down):

    with allure.step("Change opacity to -1"):
        pyautogui.scroll(-1)

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Scroll"):
        pyautogui.scroll(up_down)

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Compare screenshots"):
        assert_screenshots(False)


@allure.feature('Test front')
@allure.story('Check that the window size changes by SizeGrip')
@pytest.mark.parametrize("offset_x, offset_y", [(200, 100), (-200, -100)])
def test_front_size_grip(setup, teardown, offset_x, offset_y):

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[0], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Click and drag by SizeGrip"):
        size_grip_pos = get_new_position(DEFAULT_APP_REGION,
                                         SIZE_GRIP_CLICK_POINT)
        pyautogui.moveTo(size_grip_pos)
        pyautogui.dragTo(get_new_position(size_grip_pos, (offset_x, offset_y)))

    with allure.step("Take a screenshot"):
        img = pyautogui.screenshot(screenshots[1], region=DEFAULT_APP_REGION)
        allure_attach_screenshot(img)

    with allure.step("Compare screenshots"):
        assert_screenshots(False)
