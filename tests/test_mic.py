
from src.mic import Mic


def test_mic_is_singleton():
    """
    Check that Mic object is singleton
    """
    mic_obj_1 = Mic()
    mic_obj_2 = Mic()
    assert mic_obj_1 is mic_obj_2


def test_mic_stream_is_singleton():
    """
    Check that Mic stream object is singleton too
    """
    mic_obj_1 = Mic().stream
    mic_obj_2 = Mic().stream
    assert mic_obj_1 is mic_obj_2