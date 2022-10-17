
from typing import Optional, Tuple
import numpy as np
from src.fft import FFT
from src.selector import DeviceSelector


class StreamAdapter:

    """ Device stream data to plot data adapter """

    IS_ALIVE: bool = True
    DECIMATION: int = 1
    LEVEL: int = 1

    @staticmethod
    def _data_in() -> bytes:
        StreamAdapter.IS_ALIVE = DeviceSelector().device_is_alive
        return DeviceSelector().stream_data

    @staticmethod
    def _data_out(raw_data: bytes) -> Tuple[float, np.ndarray, np.ndarray]:
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
    def get_data_ready_to_plot() -> \
            Optional[Tuple[float, np.ndarray, np.ndarray]]:
        raw_data = StreamAdapter._data_in()
        if StreamAdapter.IS_ALIVE and raw_data:
            data_out = StreamAdapter._data_out(raw_data)
        else:
            data_out = None
        return data_out
