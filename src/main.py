import numpy as np
import matplotlib.pyplot as plt
from signals.fourier import fourier
from signals.analysis import ClimbingAgent
from audio.audio import play, record, read, write
from scipy import stats

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
    agents = find_peaks(length, yf)
    plot(signal, rate, length, xf, yf, agents)


def main3():
    from scipy.io import wavfile
    start = 60 * 0
    end = start + 5
    delta = end - start  # Also is equal to the number of samples between integral frequency values
    rate, signal = wavfile.read('Mon28Mar16.wav')
    signal = signal[start * rate:end * rate, 0] / (2. ** 15)  # Left stereo
    rain = analyze(delta, rate, signal)
    print(rain)


def analyze(delta, rate, signal):
    xf, yf = fourier(signal, rate)
    xf = xf[:delta * 17000]
    yf = yf[:delta * 17000]
    # yf = np.log10(yf)
    agent_delta = delta * 100  # 10Hz
    agents = [ClimbingAgent(yf, i, agent_delta, 0., True) for i in range(agent_delta, len(yf), agent_delta * 2 + 1)]
    agents = list(filter(lambda a: a.climb().is_on_peak, agents))
    xa = np.array([a.position / delta for a in agents])
    ya = np.array([a.value for a in agents])
    # print(len(agents))
    # print(list(zip(xa, ya)))
    slope, intercept, r_value, p_value, std_err = stats.linregress(xa, np.sqrt(1. / ya))
    # xr = np.arange(17000)
    # yr = xr * slope + intercept
    # yr = 1. / (yr ** 2)
    # print(slope, intercept, r_value, p_value, std_err)
    # plt.subplot(2, 1, 1)
    # plt.plot(np.arange(len(signal)) / rate, signal)
    # plt.subplot(2, 1, 2)
    # plt.plot(xf, yf)
    # plt.plot(xa, ya, 'r*')
    # plt.plot(xr, yr, 'g')
    # plt.show()
    rain = (r_value - 0.8) / 0.2 if r_value > 0.8 else 0.0
    return rain


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
