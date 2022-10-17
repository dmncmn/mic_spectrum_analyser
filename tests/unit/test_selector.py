
import allure
from src.selector import DeviceSelector


@allure.feature('Test selector')
@allure.story('Check that Device selector object is singleton')
def test_selector_is_singleton():
    selector_obj_1 = DeviceSelector()
    selector_obj_2 = DeviceSelector()
    assert selector_obj_1 is selector_obj_2
