def play(signal, rate):
    import pyaudio

    if signal.ndim == 1:
        frames, channels = signal.size, 1
    else:
        frames, channels = signal.shape

    signal = _buffer(signal)

    with Nostderr():
        audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paFloat32,
                        channels=channels,
                        rate=rate,
                        output=True)

    stream.write(signal, frames)

    stream.stop_stream()
    stream.close()
    audio.terminate()


def record(rate, length, channels=1, buffer_size=0):
    if buffer_size == 0:
        buffer_size = rate  # By default one second buffer

    import pyaudio

    with Nostderr():
        audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paFloat32,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=buffer_size)

    signal = bytearray()
    for i in range(rate * length // buffer_size):
        signal += stream.read(buffer_size)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    return _array(signal, channels)


def read(file):
    import numpy as np
    from scipy.io import wavfile

    rate, signal = wavfile.read(file)
    if signal.dtype == np.uint8:
        signal = (signal / (2. ** 8)).astype(np.float32)
    elif signal.dtype == np.int8:
        signal = (signal / (2. ** 7)).astype(np.float32)
    elif signal.dtype == np.int16:
        signal = (signal / (2. ** 15)).astype(np.float32)
    elif signal.dtype == np.float32:
        pass
    else:  # int24 or other
        import sys
        print('Unhandled bit deep', file=sys.stderr)

    return signal, rate


def write(file, rate, signal):
    import numpy as np
    from scipy.io import wavfile

    signal = (signal * (2. ** 15)).astype(np.int16)
    wavfile.write(file, rate, signal)


def _buffer(array):
    return array.astype('float32').tobytes()


def _array(buffer, channels):
    import numpy as np

    array = np.frombuffer(buffer, dtype='float32')
    if channels > 1:
        array.shape = -1, channels
    return array


class Nostderr():
    def __init__(self):
        self.old_stderr = None

    def __enter__(self):
        import sys
        import os
        devnull = os.open(os.devnull, os.O_WRONLY)
        self.old_stderr = os.dup(2)
        sys.stderr.flush()
        os.dup2(devnull, 2)
        os.close(devnull)
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        import sys
        import os
        os.dup2(self.old_stderr, 2)
        os.close(self.old_stderr)
