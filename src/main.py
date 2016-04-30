import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from signals.fourier import fourier
from signals.analysis import ClimbingAgent

start = 0
end = 15
delta = end - start  # Also is equal to the number of samples between integral frequency values
fs, signal = wavfile.read('Mon28Mar16.wav')
signal = signal[start * fs:end * fs, 0] / (2. ** 15)  # Left stereo

xf, yf = fourier(signal, fs)
xf = xf[:delta * 2500]
yf = yf[:delta * 2500]

agent_delta = delta * 10  # 10Hz
agents = [ClimbingAgent(yf, i, agent_delta, 0.005, True) for i in range(agent_delta, len(yf), agent_delta * 2 + 1)]
agents = list(filter(lambda a: a.climb().is_on_peak, agents))
plt.subplot(2, 1, 1)
plt.plot(np.arange(len(signal)), signal)
plt.subplot(2, 1, 2)
plt.plot(xf, yf)
plt.plot([a.position / delta for a in agents], [a.value for a in agents], 'r*', label='Interesting Points')
plt.show()
