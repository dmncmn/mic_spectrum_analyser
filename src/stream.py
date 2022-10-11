
from typing import Union
import numpy as np
from src.fft import FFT
from src.mic import Mic


class Stream:

    IS_ALIVE: bool = True

    @staticmethod
    def _check() -> None:
        Stream.IS_ALIVE = Mic.IS_ALIVE

    @staticmethod
    def _listen() -> Union[str, None]:
        Stream._check()
        return Mic().stream_raw_data()

    @staticmethod
    def _prepare(raw_data: str,
                 decimation_factor: int,
                 sensitivity: int) -> np.ndarray:
        return FFT.data_ready_to_plot(raw_data, decimation_factor, sensitivity)

    @staticmethod
    def get_data_ready_to_plot(decimation_factor: int,
                               sensitivity: int) -> Union[np.ndarray, None]:
        raw_data = Stream._listen()
        if raw_data is None:
            return
        return Stream._prepare(raw_data, decimation_factor, sensitivity)
