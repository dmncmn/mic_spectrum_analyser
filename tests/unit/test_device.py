
import pytest
from src.device import Mic, MockDevice


@pytest.mark.parametrize("device", [Mic, MockDevice])
def test_device_is_singleton(device):
    """
    Check that Device object is singleton
    """
    mic_obj_1 = device()
    mic_obj_2 = device()
    assert mic_obj_1 is mic_obj_2


@pytest.mark.parametrize("device", [Mic, MockDevice])
def test_device_stream_is_singleton(device):
    """
    Check that Device stream object is singleton too
    """
    mic_obj_1 = device().stream
    mic_obj_2 = device().stream
    assert mic_obj_1 is mic_obj_2
