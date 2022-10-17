
import allure
import pytest
from src.device import Mic, MockDevice


@allure.feature('Test device')
@allure.story('Check that Device object is singleton')
@pytest.mark.parametrize("device", [Mic, MockDevice])
def test_device_is_singleton(device):
    mic_obj_1 = device()
    mic_obj_2 = device()
    assert mic_obj_1 is mic_obj_2


@allure.feature('Test device')
@allure.story('Check that Device stream object is singleton too')
@pytest.mark.parametrize("device", [Mic, MockDevice])
def test_device_stream_is_singleton(device):
    mic_obj_1 = device().stream
    mic_obj_2 = device().stream
    assert mic_obj_1 is mic_obj_2
