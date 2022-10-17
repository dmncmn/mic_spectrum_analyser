
import allure
import pytest
import numpy as np
import src.styles as s
from src.selector import DeviceSelector
from src.stream import StreamAdapter
from src.fft import FFT


@allure.feature('Test stream adapter')
@allure.story('Check that data from Device selector '
              'and at adapter input is the same')
def test_stream_adapter_data_in_():

    with allure.step("Get raw data from device"):
        raw_data = DeviceSelector(device='Mock').stream_data

    with allure.step("Get stream adapter data in"):
        data_in = StreamAdapter._data_in()

    with allure.step("Compare data"):
        assert raw_data == data_in


@allure.feature('Test stream adapter')
@allure.story('Check that data from FFT and adapter Y output is the same')
@pytest.mark.parametrize("level", [1, 100])
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_y(level, decimation_factor):

    with allure.step("Get raw data from device"):
        raw_data = DeviceSelector(device='Mock').stream_data

    with allure.step("Get data from FFT"):
        FFT.FFT_SIZE = DeviceSelector().size_data
        FFT.FFT_LEVEL_FACTOR = level
        FFT.FFT_DECIMATION_FACTOR = decimation_factor
        data = FFT.data_ready_to_plot(raw_data)

    with allure.step("Get data from stream adapter"):
        StreamAdapter.LEVEL = level
        StreamAdapter.DECIMATION = decimation_factor
        _, _, data_y = StreamAdapter._data_out(raw_data)

    with allure.step("Compare data"):
        assert np.array_equal(data, data_y)


@allure.feature('Test stream adapter')
@allure.story('Check that X, Y dimensions of adapter output is the same')
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_same_x_y(decimation_factor):

    with allure.step("Get raw data from device"):
        raw_data = DeviceSelector(device='Mock').stream_data

    with allure.step("Get X, Y data"):
        StreamAdapter.DECIMATION = decimation_factor
        _, data_x, data_y = StreamAdapter._data_out(raw_data)

    with allure.step("Compare X, Y size"):
        assert len(data_x) == len(data_y)


@allure.feature('Test stream adapter')
@allure.story('Check that X resolution calculates correctly')
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_stream_adapter_data_out_x_res(decimation_factor):

    with allure.step("Get raw data from device"):
        raw_data = DeviceSelector(device='Mock').stream_data

    with allure.step("Get X resolution and X data"):
        StreamAdapter.DECIMATION = decimation_factor
        data_x_res, data_x, _ = StreamAdapter._data_out(raw_data)

    with allure.step("Check resolution"):
        assert data_x_res * len(data_x) == s.PLOT_X_MAX_VALUE
