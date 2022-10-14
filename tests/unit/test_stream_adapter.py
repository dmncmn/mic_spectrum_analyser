
import pytest
import numpy as np
from src.selector import DeviceSelector
from src.stream import StreamAdapter
from src.fft import FFT


def test_stream_adapter_data_in_():
    """
    Check that data from Device selector and at adapter input is the same
    """
    data = DeviceSelector(device='Mock').device().stream_raw_data()
    data_in = StreamAdapter._data_in()
    assert data == data_in


@pytest.mark.parametrize("level", [1, 100])
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_(level, decimation_factor):
    """
    Check that data from FFT and adapter outputs is the same
    """
    raw_data = DeviceSelector(device='Mock').device().stream_raw_data()
    data = FFT.data_ready_to_plot(raw_data, decimation_factor, level)
    data_out = StreamAdapter._data_out(raw_data, decimation_factor, level)
    assert np.array_equal(data, data_out)
