import numpy as np
import matplotlib.pyplot as plt
from signals.fourier import fourier
from signals.analysis import ClimbingAgent
from audio.audio import play, record, read, write


def main():
    rate = 44100
    length = 5
    signal = record(rate, length)
    xf, yf = fourier(signal, rate)
    agents = find_peaks(length, yf)
    plot(signal, rate, length, xf, yf, agents)


def plot(signal, rate, delta, xf, yf, agents):
    plt.subplot(2, 1, 1)
    plt.plot(np.arange(len(signal)) / rate, signal)
    plt.subplot(2, 1, 2)
    plt.plot(xf, yf)
    plt.plot([a.position / delta for a in agents], [a.value for a in agents], 'r*')
    plt.show()


def find_peaks(length, yf):
    agent_delta = length * 10  # 10Hz
    agents = [ClimbingAgent(yf, i, agent_delta, 0.005, True) for i in range(agent_delta, len(yf), agent_delta * 2 + 1)]
    agents = list(filter(lambda a: a.climb().is_on_peak, agents))
    # print(len(agents))
    # print([a.position / length for a in agents])
    # print([a.value for a in agents])
    return agents


if __name__ == "__main__":
    main()
