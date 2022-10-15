
import pytest
import numpy as np
from src.selector import DeviceSelector
from src.stream import StreamAdapter
from src.fft import FFT
from src.styles import *


def test_stream_adapter_data_in_():
    """
    Check that data from Device selector and at adapter input is the same
    """
    data = DeviceSelector(device='Mock').stream_data
    data_in = StreamAdapter._data_in()
    assert data == data_in


@pytest.mark.parametrize("level", [1, 100])
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_y(level, decimation_factor):
    """
    Check that data from FFT and adapter Y output is the same
    """
    raw_data = DeviceSelector(device='Mock').stream_data

    FFT.FFT_SIZE = DeviceSelector().size_data
    FFT.FFT_LEVEL_FACTOR = level
    FFT.FFT_DECIMATION_FACTOR = decimation_factor
    data = FFT.data_ready_to_plot(raw_data)

    StreamAdapter.LEVEL = level
    StreamAdapter.DECIMATION = decimation_factor
    _, _, data_y = StreamAdapter._data_out(raw_data)

    assert np.array_equal(data, data_y)


@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_same_x_y(decimation_factor):
    """
    Check that X, Y dimensions of adapter output is the same
    """
    raw_data = DeviceSelector(device='Mock').stream_data
    StreamAdapter.DECIMATION = decimation_factor
    _, data_x, data_y = StreamAdapter._data_out(raw_data)
    assert len(data_x) == len(data_y)


@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_x_res(decimation_factor):
    """
    Check that X resolution calculates correctly
    """
    raw_data = DeviceSelector(device='Mock').stream_data
    StreamAdapter.DECIMATION = decimation_factor
    data_x_res, data_x, _ = StreamAdapter._data_out(raw_data)
    assert data_x_res * len(data_x) == PLOT_X_MAX_VALUE
