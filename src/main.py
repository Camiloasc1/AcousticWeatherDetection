from signals.fourier import fourier
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt

start = 0
end = 15
fs, signal = wavfile.read('Mon28Mar16.wav')
signal = signal[start * fs:end * fs, 0] / (2. ** 15)  # Left stereo

xf, yf = fourier(signal, fs)
plt.subplot(2, 1, 1)
plt.plot(np.arange(len(signal)), signal)
plt.subplot(2, 1, 2)
plt.plot(xf, yf)
plt.show()
