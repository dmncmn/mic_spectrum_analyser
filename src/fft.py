
import numpy as np
from typing import Callable


class FFT:

    """ FFT module for convert time domain data to frequency domain """

    FFT_SIZE = 1024
    FFT_HALF_SPECTRUM_SIZE = FFT_SIZE // 2
    FFT_DECIMATION_FACTOR = 1
    FFT_LEVEL_FACTOR = 1

    @staticmethod
    def _get_time_data(raw_data: bytes) -> np.ndarray:
        return np.frombuffer(raw_data, np.int16)

    @staticmethod
    def _get_smoothed_time_data(
            time_data: np.ndarray,
            window: Callable[[int], np.ndarray] = np.hamming) \
            -> np.ndarray:
        return time_data * window(len(time_data))

    @staticmethod
    def _get_amplitude_spectrum(time_data: np.ndarray) -> np.ndarray:
        return np.abs(np.fft.fft(time_data)[:FFT.FFT_HALF_SPECTRUM_SIZE])

    @staticmethod
    def _decimate_spectrum(spectrum: np.ndarray) -> np.ndarray:
        if FFT.FFT_DECIMATION_FACTOR == 1:
            return spectrum
        return spectrum[::FFT.FFT_DECIMATION_FACTOR]

    @staticmethod
    def _normalize_spectrum(spectrum: np.ndarray) -> np.ndarray:
        return spectrum / FFT.FFT_SIZE

    @staticmethod
    def _change_spectrum_level(spectrum: np.ndarray) -> np.ndarray:
        if FFT.FFT_LEVEL_FACTOR == 1:
            return spectrum
        return spectrum * FFT.FFT_LEVEL_FACTOR

    @staticmethod
    def data_ready_to_plot(raw_data: bytes) -> np.ndarray:
        data = FFT._get_time_data(raw_data)
        data = FFT._get_smoothed_time_data(data)
        data = FFT._get_amplitude_spectrum(data)
        data = FFT._decimate_spectrum(data)
        data = FFT._change_spectrum_level(data)
        data = FFT._normalize_spectrum(data)
        return data
