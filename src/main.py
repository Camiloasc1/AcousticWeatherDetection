import numpy as np

from audio.audio import record
from signals.analysis import find_peaks, climb
from signals.fourier import fourier


def main():
    rate = 44100
    length = 5
    while True:
        signal = record(rate, length)
        rain = analyze(length, rate, signal)
        print(rain)


def analyze(length, rate, signal):
    # import matplotlib.pyplot as plt
    xf, yf = fourier(signal, rate)
    # xf = xf[:length * 5000]
    yf = yf[:length * 5000]
    # yf = np.log10(yf)
    agents_signal = find_peaks(signal, rate, 100, 0.01)
    # xa_signal = np.array([a.position / rate for a in agents_signal])
    ya_signal = np.array([a.value for a in agents_signal])

    # plt.subplot(2, 1, 1)
    # plt.plot(np.arange(len(signal)) / rate, signal)
    # plt.plot(xa_signal, ya_signal, 'r*')

    agents_spectrum = climb(yf, length, 1, 0.0001, 1)
    xa_spectrum = np.array([a.position / length for a in agents_spectrum])
    ya_spectrum = np.array([a.value for a in agents_spectrum])

    # plt.subplot(2, 1, 2)
    # plt.plot(xf, yf)
    # plt.plot(xa_spectrum, ya_spectrum, 'r*')
    #
    # plt.show()

    area = np.trapz(ya_spectrum, xa_spectrum)
    avg = np.average(ya_signal)
    # var = np.var(ya_signal)
    std = np.std(ya_signal)
    area_factor = (1 - (48. - area) / 48.)
    volume_factor = avg - std
    # print(volume_factor, area_factor, area)
    rain = np.sqrt(clamp01(volume_factor) * clamp01(area_factor))
    return rain


def clamp01(value):
    if value > 1.:
        return 1.
    if value < 0.:
        return 0.
    return value


if __name__ == "__main__":
    main()
