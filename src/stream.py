
from typing import Union
import numpy as np
from src.fft import FFT
from src.selector import DeviceSelector


class StreamAdapter:

    """ Device stream data to plot data adapter """

    IS_ALIVE: bool = True
    DECIMATION: int = 1
    LEVEL: int = 1

    @staticmethod
    def _data_in() -> Union[str, None]:
        StreamAdapter.IS_ALIVE = DeviceSelector().device_is_alive
        return DeviceSelector().stream_data

    @staticmethod
    def _data_out(raw_data: str) -> tuple[float, np.ndarray, np.ndarray]:
        FFT.FFT_SIZE = DeviceSelector().size_data
        FFT.FFT_DECIMATION_FACTOR = StreamAdapter.DECIMATION
        FFT.FFT_LEVEL_FACTOR = StreamAdapter.LEVEL
        y_data = FFT.data_ready_to_plot(raw_data)
        max_freq: float = DeviceSelector().sampling_rate / 2
        x_res: float = \
            max_freq / FFT.FFT_HALF_SPECTRUM_SIZE * FFT.FFT_DECIMATION_FACTOR
        x_data: np.ndarray = np.arange(0, max_freq, x_res)
        return x_res, x_data, y_data

    @staticmethod
    def get_data_ready_to_plot() -> Union[np.ndarray, None]:
        raw_data = StreamAdapter._data_in()
        if raw_data is None:
            return
        return StreamAdapter._data_out(raw_data)
