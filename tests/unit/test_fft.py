
import allure
import pytest
import numpy as np
from src.fft import FFT


@allure.feature('Test fft')
@allure.story('Check that the real and measured frequency '
              'are the same for measurement error')
@pytest.mark.parametrize("real_freq_hz, sampling_rate_hz",
                         [(20000, 44100), (10000, 44100),
                          (2500, 44100), (1000, 44100), (500, 44100),
                          (10000, 22050), (2500, 22050), (1000, 22050),
                          (500, 22050), (1000, 10000), (500, 10000)])
def test_fft_get_amplitude_spectrum(real_freq_hz, sampling_rate_hz):

    with allure.step("Generate sin in time domain"):
        t: np.ndarray = np.linspace(0,
                                    FFT.FFT_SIZE / sampling_rate_hz,
                                    FFT.FFT_SIZE)
        time_data: np.ndarray = np.sin(2 * np.pi * real_freq_hz * t)

    with allure.step("Get sin in frequency domain"):
        spectrum: np.ndarray = FFT._get_amplitude_spectrum(time_data)

    with allure.step("Measure sin frequency"):
        measured_freq_hz: float = \
            np.argmax(spectrum) * sampling_rate_hz / FFT.FFT_SIZE

    with allure.step("Set measurement error to 5% of real frequency"):
        measurement_error_hz: float = 0.05 * real_freq_hz

    with allure.step("Compare frequencies"):
        assert np.abs(real_freq_hz - measured_freq_hz) < measurement_error_hz


@allure.feature('Test fft')
@allure.story('Check fft spectrum normalization')
@pytest.mark.parametrize("fft_size", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("amplitude", [1, 100])
def test_fft_normalize_spectrum(fft_size, amplitude):

    with allure.step("Generate spectrum as a white noise"):
        FFT.FFT_SIZE = fft_size
        spectrum = np.full(shape=(FFT.FFT_SIZE,), fill_value=amplitude)

    with allure.step("Normalize spectrum"):
        normalized_spectrum = FFT._normalize_spectrum(spectrum)

    with allure.step("Compare spectrums"):
        assert normalized_spectrum[0] * FFT.FFT_SIZE == amplitude


@allure.feature('Test fft')
@allure.story('Check fft spectrum decimation')
@pytest.mark.parametrize("amplitude", [100])
@pytest.mark.parametrize("fft_size", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_fft_decimate_spectrum(amplitude, fft_size, decimation_factor):
    """
    Check fft spectrum decimation
    """
    with allure.step("Generate spectrum as a white noise"):
        FFT.FFT_SIZE = fft_size
        spectrum = np.full(shape=(FFT.FFT_SIZE,), fill_value=amplitude)

    with allure.step("Decimate spectrum"):
        FFT.FFT_DECIMATION_FACTOR = decimation_factor
        decimated_spectrum = FFT._decimate_spectrum(spectrum)

    with allure.step("Compare spectrums"):
        assert len(decimated_spectrum) * decimation_factor == len(spectrum)


@allure.feature('Test fft')
@allure.story('Check fft spectrum scaling')
@pytest.mark.parametrize("level", [1, 2, 4, 8, 16, 32])
@pytest.mark.parametrize("amplitude", [1, 100])
def test_fft_change_spectrum_level(level, amplitude):

    with allure.step("Generate spectrum as a white noise"):
        spectrum = np.full(shape=(FFT.FFT_SIZE,), fill_value=amplitude)

    with allure.step("Change spectrum level"):
        FFT.FFT_LEVEL_FACTOR = level
        scaled_spectrum = FFT._change_spectrum_level(spectrum)

    with allure.step("Compare spectrums"):
        assert scaled_spectrum[0] == amplitude * level


@allure.feature('Test fft')
@allure.story('Check fft time-data smoothing')
@pytest.mark.parametrize("amplitude", [100])
@pytest.mark.parametrize("len_data", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("window", [np.hamming, np.bartlett, np.blackman])
def test_fft_get_smoothed_time_data(amplitude, len_data, window):
    """
    Check fft time-data smoothing
    """
    with allure.step("Generate time-data as a const"):
        time_data = np.full(shape=(len_data,), fill_value=amplitude)

    with allure.step("Get smoothed time-data"):
        smoothed_data = time_data * window(len(time_data))

    with allure.step("Get smoothed time-data by fft"):
        fft_smoothed_data = FFT._get_smoothed_time_data(time_data, window)

    with allure.step("Compare signals"):
        assert np.array_equal(smoothed_data, fft_smoothed_data)
