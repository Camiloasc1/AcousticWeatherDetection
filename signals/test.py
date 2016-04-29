import numpy as np
import matplotlib.pyplot as plt

from signals.fourier import fourier


def test():
    fs = 100
    length = 100.0
    n = fs * length

    x = np.linspace(0., length, n)
    y = np.sin(10. * 2. * np.pi * x)
    y += 0.75 * np.sin(20. * 2. * np.pi * x)
    y += 0.5 * np.sin(30. * 2. * np.pi * x)
    y += 0.25 * np.sin(40. * 2. * np.pi * x)
    xf, yf = fourier(y, fs)

    plt.subplot(2, 1, 1)
    plt.plot(x, y)
    plt.subplot(2, 1, 2)
    plt.plot(xf, yf)
    plt.show()


if __name__ == "__main__":
    test()
