import numpy as np


def fourier(signal, sample_rate):
    # n = int(signal.size / 2)
    n = int(len(signal) / 2)
    x = np.linspace(0., n, n) * (sample_rate / 2 / n)
    y = np.abs(np.fft.fft(signal)[:n]) / n
    return x, y
