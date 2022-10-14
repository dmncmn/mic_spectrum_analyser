
from typing import Union
import numpy as np
from src.fft import FFT
from src.selector import DeviceSelector


class StreamAdapter:

    """ Device stream data to plot data adapter """

    IS_ALIVE: bool = True

    @staticmethod
    def _check() -> None:
        StreamAdapter.IS_ALIVE = DeviceSelector.IS_ALIVE

    @staticmethod
    def _data_in() -> Union[str, None]:
        StreamAdapter._check()
        return DeviceSelector().device().stream_raw_data()

    @staticmethod
    def _data_out(raw_data: str,
                  decimation_factor: int,
                  sensitivity: float) -> np.ndarray:
        return FFT.data_ready_to_plot(raw_data, decimation_factor, sensitivity)

    @staticmethod
    def get_data_ready_to_plot(decimation_factor: int,
                               sensitivity: float) -> Union[np.ndarray, None]:
        raw_data = StreamAdapter._data_in()
        if raw_data is None:
            return
        return StreamAdapter._data_out(raw_data, decimation_factor, sensitivity)
