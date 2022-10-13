
from src.selector import DeviceSelector


def test_selector_is_singleton():
    """
    Check that Device selector object is singleton
    """
    selector_obj_1 = DeviceSelector()
    selector_obj_2 = DeviceSelector()
    assert selector_obj_1 is selector_obj_2
