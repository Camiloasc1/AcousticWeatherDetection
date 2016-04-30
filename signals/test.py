import numpy as np
import matplotlib.pyplot as plt

from signals.fourier import fourier
from signals.analysis import ClimbingAgent


def test_fourier():
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


def test_agent():
    values = [1, 2, 3, 2, 1]
    delta = 2
    agent = ClimbingAgent(values, 4, delta, 1)
    print([i for i in agent.range()])
    print([i for i in agent.range(True)])
    agent.climb()
    print([i for i in agent.range()])
    print([i for i in agent.range(True)])
    print([i for i in range(delta, 15, delta * 2 + 1)])


if __name__ == "__main__":
    # test_fourier()
    test_agent()
