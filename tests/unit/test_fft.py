
import pytest
import numpy as np
from src.fft import FFT


@pytest.mark.parametrize("real_freq_hz, sampling_rate_hz",
                         [(20000, 44100), (10000, 44100),
                          (2500, 44100), (1000, 44100), (500, 44100),
                          (10000, 22050), (2500, 22050), (1000, 22050),
                          (500, 22050), (1000, 10000), (500, 10000)])
def test_fft_get_amplitude_spectrum(real_freq_hz, sampling_rate_hz):
    """
    Check that the real and measured frequency are
    the same for measurement error
    """
    # Generate sin in time domain
    t: np.ndarray = np.linspace(0,
                                FFT.FFT_SIZE / sampling_rate_hz,
                                FFT.FFT_SIZE)
    time_data: np.ndarray = np.sin(2 * np.pi * real_freq_hz * t)
    # Get sin in frequency domain
    spectrum: np.ndarray = FFT._get_amplitude_spectrum(time_data)
    # Measure sin frequency
    measured_freq_hz: float = \
        np.argmax(spectrum) * sampling_rate_hz / FFT.FFT_SIZE
    # Set measurement error to 5% of real frequency
    measurement_error_hz: float = 0.05 * real_freq_hz

    assert np.abs(real_freq_hz - measured_freq_hz) < measurement_error_hz


@pytest.mark.parametrize("fft_size", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("amplitude", [1, 100])
def test_fft_normalize_spectrum(fft_size, amplitude):
    """
    Check fft spectrum normalization
    """
    # Let spectrum be like spectrum of white noise
    FFT.FFT_SIZE = fft_size
    spectrum = np.full(shape=(FFT.FFT_SIZE,), fill_value=amplitude)
    normalized_spectrum = FFT._normalize_spectrum(spectrum)
    assert normalized_spectrum[0] * FFT.FFT_SIZE == amplitude


@pytest.mark.parametrize("amplitude", [100])
@pytest.mark.parametrize("fft_size", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("decimation_factor", [1, 8, 32])
def test_fft_decimate_spectrum(amplitude, fft_size, decimation_factor):
    """
    Check fft spectrum decimation
    """
    # Let spectrum be like spectrum of white noise
    FFT.FFT_SIZE = fft_size
    spectrum = np.full(shape=(FFT.FFT_SIZE,), fill_value=amplitude)
    FFT.FFT_DECIMATION_FACTOR = decimation_factor
    decimated_spectrum = FFT._decimate_spectrum(spectrum)
    assert len(decimated_spectrum) * decimation_factor == len(spectrum)


@pytest.mark.parametrize("level", [1, 2, 4, 8, 16, 32])
@pytest.mark.parametrize("amplitude", [1, 100])
def test_fft_change_spectrum_level(level, amplitude):
    """
    Check fft spectrum scaling
    """
    # Let spectrum be like spectrum of white noise
    spectrum = np.full(shape=(FFT.FFT_SIZE,), fill_value=amplitude)
    FFT.FFT_LEVEL_FACTOR = level
    scaled_spectrum = FFT._change_spectrum_level(spectrum)
    assert scaled_spectrum[0] == amplitude * level


@pytest.mark.parametrize("amplitude", [100])
@pytest.mark.parametrize("len_data", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("window", [np.hamming, np.bartlett, np.blackman])
def test_fft_get_smoothed_time_data(amplitude, len_data, window):
    """
    Check fft time-data smoothing
    """
    # Let time-data be like const
    time_data = np.full(shape=(len_data,), fill_value=amplitude)
    smoothed_data = time_data * window(len(time_data))
    fft_smoothed_data = FFT._get_smoothed_time_data(time_data, window)
    assert np.array_equal(smoothed_data, fft_smoothed_data)
