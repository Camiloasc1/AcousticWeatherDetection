import numpy as np
import matplotlib.pyplot as plt
from signals.fourier import fourier
from signals.analysis import ClimbingAgent
from audio.audio import play, record, read, write


def main():
    rate = 44100
    length = 5
    while True:
        signal = record(rate, length)
        rain = analyze(length, rate, signal)
        print(rain)


def main2():
    rate = 44100
    length = 5
    signal = record(rate, length)
    xf, yf = fourier(signal, rate)
    agents = find_peaks(yf, length, 0.1, 0.005)
    plot(signal, rate, length, xf, yf, agents)


def main3():
    from scipy.io import wavfile
    start = 60 * 0 + 0
    end = start + 5
    delta = end - start  # Also is equal to the number of samples between integral values of frequency
    rate, signal = wavfile.read('Mon28Mar16.wav')
    signal = signal[start * rate:end * rate, 0] / (2. ** 15)  # Left stereo
    rain = analyze(delta, rate, signal)
    print(rain)


def analyze(length, rate, signal):
    xf, yf = fourier(signal, rate)
    # xf = xf[:length * 5000]
    # yf = yf[:length * 5000]
    # yf = np.log10(yf)
    agents_signal = find_peaks(signal, rate, 100, 0.01)
    xa_signal = np.array([a.position / rate for a in agents_signal])
    ya_signal = np.array([a.value for a in agents_signal])

    # plt.subplot(2, 1, 1)
    # plt.plot(np.arange(len(signal)) / rate, signal)
    # plt.plot(xa_signal, ya_signal, 'r*')

    agents_spectrum = find_peaks(yf, length, 0.1, 0.0001)
    xa_spectrum = np.array([a.position / length for a in agents_spectrum])
    ya_spectrum = np.array([a.value for a in agents_spectrum])

    # plt.subplot(2, 1, 2)
    # plt.plot(xf, yf)
    # plt.plot(xa_spectrum, ya_spectrum, 'r*')

    # plt.show()

    area = np.trapz(ya_spectrum, xa_spectrum)
    print(area)
    rain = np.average(ya_signal)
    return rain


def plot(signal, rate, delta, xf, yf, agents):
    plt.subplot(2, 1, 1)
    plt.plot(np.arange(len(signal)) / rate, signal)
    plt.subplot(2, 1, 2)
    plt.plot(xf, yf)
    plt.plot([a.position / delta for a in agents], [a.value for a in agents], 'r*')
    plt.show()


def find_peaks(world, rate, delta, height):
    """
    Find peaks in a samples list using ClimbingAgents.

    :param world:Samples
    :type world:list
    :param rate:Amount of samples per unit
    :type rate:int
    :param delta:Amount of agents per unit
    :type delta:float
    :param height:Minimum height
    :type height:float
    :return:A list with the ClimbingAgents
    :rtype:list
    """

    agent_delta = int(rate / delta)
    agents = [ClimbingAgent(world, i, agent_delta, height, True) for i in
              range(agent_delta, len(world), agent_delta * 2 + 1)]
    agents = list(filter(lambda a: a.climb().is_on_peak, agents))
    return agents


if __name__ == "__main__":
    main3()
