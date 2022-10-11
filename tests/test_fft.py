
import pytest
import numpy as np
from src.fft import FFT


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
