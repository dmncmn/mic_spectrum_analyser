
import numpy as np


class FFT:

    FFT_SIZE = 1024
    HALF_SPECTRUM_SIZE = FFT_SIZE // 2
    FFT_DEFAULT_DECIMATION_FACTOR = 1
    FFT_DEFAULT_LEVEL_FACTOR = 1

    @staticmethod
    def _get_time_data(raw_data: str) -> np.array:
        return np.fromstring(raw_data, np.int16)

    @staticmethod
    def _get_amplitude_spectrum(time_data: np.array) -> np.array:
        return np.abs(np.fft.fft(time_data))[:FFT.HALF_SPECTRUM_SIZE]

    @staticmethod
    def _decimate_spectrum(spectrum: np.array,
                           factor: int = FFT_DEFAULT_DECIMATION_FACTOR) -> np.array:
        if factor == 1:
            return spectrum
        return spectrum[::factor]

    @staticmethod
    def _normalize_spectrum(spectrum: np.array) -> np.array:
        return spectrum / FFT.FFT_SIZE

    @staticmethod
    def _change_spectrum_level(spectrum: np.array,
                               level: int = FFT_DEFAULT_LEVEL_FACTOR) -> np.array:
        if level == 1:
            return spectrum
        return spectrum * level

    @staticmethod
    def data_ready_to_plot(raw_data: str,
                           decimation_factor: int,
                           sensitivity_level: int) -> np.array:
        data = FFT._get_time_data(raw_data)
        data = FFT._get_amplitude_spectrum(data)
        data = FFT._decimate_spectrum(data, decimation_factor)
        data = FFT._normalize_spectrum(data)
        data = FFT._change_spectrum_level(data, sensitivity_level)
        return data
