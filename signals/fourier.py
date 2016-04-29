import numpy as np


def fourier(signal, fs):
    # n = int(signal.size / 2)
    n = int(len(signal) / 2)
    x = np.linspace(0.0, n, n) * (fs / 2 / n)
    y = np.abs(np.fft.fft(signal)[:n]) / n
    return x, y
