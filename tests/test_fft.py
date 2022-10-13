
import pytest
import numpy as np
from src.fft import FFT


@pytest.mark.parametrize("real_freq_hz, sampling_rate_hz",
                         [(20000, 44100), (10000, 44100),
                          (2500, 44100), (1000, 44100), (500, 44100),
                          (10000, 22050), (2500, 22050), (1000, 22050),
                          (500, 22050), (1000, 10000), (500, 10000)])
def test_fft_get_amplitude_spectrum(real_freq_hz,
                                    sampling_rate_hz, fft_size=1024):
    """
    Check that the real and measured frequency are
    the same for measurement error
    """
    # Generate sin in time domain
    t: np.ndarray = np.linspace(0, fft_size / sampling_rate_hz, fft_size)
    time_data: np.ndarray = np.sin(2 * np.pi * real_freq_hz * t)

    # Get sin in frequency domain
    FFT.FFT_SIZE = fft_size
    spectrum: np.ndarray = FFT._get_amplitude_spectrum(time_data)

    # Measure sin frequency
    measured_freq: float = np.argmax(spectrum) * sampling_rate_hz / fft_size

    # Set measurement error to 5% of real frequency
    measurement_error_hz: float = 0.05 * real_freq_hz

    assert np.abs(real_freq_hz - measured_freq) < measurement_error_hz


@pytest.mark.parametrize("fft_size", [1024, 512, 256, 128, 64])
def test_fft_normalize_spectrum(fft_size):
    """
    Check fft spectrum normalization
    """
    FFT.FFT_SIZE = fft_size
    spectrum = np.full((FFT.FFT_SIZE,), FFT.FFT_SIZE)
    normalized_spectrum = FFT._normalize_spectrum(spectrum)
    assert normalized_spectrum[0] * FFT.FFT_SIZE == spectrum[0]


@pytest.mark.parametrize("fft_size", [1024, 512, 256, 128, 64])
@pytest.mark.parametrize("decimation_factor", [1, 2, 4, 8, 16, 32])
def test_fft_decimate_spectrum(fft_size, decimation_factor):
    """
    Check that fft spectrum decimation
    """
    FFT.FFT_SIZE = fft_size
    spectrum = np.full((FFT.FFT_SIZE,), FFT.FFT_SIZE)
    decimated_spectrum = FFT._decimate_spectrum(spectrum, decimation_factor)
    assert len(decimated_spectrum) * decimation_factor == len(spectrum)


@pytest.mark.parametrize("level", [1, 2, 4, 8, 16, 32])
def test_fft_change_spectrum_level(level, fft_size=64):
    """
    Check fft spectrum scaling
    """
    FFT.FFT_SIZE = fft_size
    spectrum = np.full((FFT.FFT_SIZE,), FFT.FFT_SIZE)
    scaled_spectrum = FFT._change_spectrum_level(spectrum, level)
    assert spectrum[0] * level == scaled_spectrum[0]
