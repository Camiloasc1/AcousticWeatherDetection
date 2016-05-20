import numpy as np
import time
from threading import Thread
from audio.audio import record
from signals.analysis import find_peaks, climb
from signals.fourier import fourier

import gi

RUN = True
RATE = 44100
LENGTH = 5
SLEEP = 10
PATH = '../img/'
SIZE = 2

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf


class Handler:
    def __init__(self, gui):
        self.gui = gui

    def onButtonPressed(self, button):
        print("Hello World!")


class GUI:
    def __init__(self, file):
        self.width = 256 * SIZE
        self.height = 160 * SIZE

        self.builder = Gtk.Builder()
        self.builder.add_from_file(file)
        self.builder.connect_signals(Handler(self))

        self.window = self.builder.get_object("MainWindow")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()

        self.image = self.builder.get_object("Image")
        self.record = self.builder.get_object("Record")
        self.spinner = self.builder.get_object("Spinner")
        self.scale = self.builder.get_object("Scale")
        self.adjustment = self.builder.get_object("Adjustment")

        self.clear = GdkPixbuf.Pixbuf.new_from_file_at_size(PATH + 'weather-clear.jpg', self.width, self.height)
        self.soft = GdkPixbuf.Pixbuf.new_from_file_at_size(PATH + 'weather-showers.jpg', self.width, self.height)
        self.hard = GdkPixbuf.Pixbuf.new_from_file_at_size(PATH + 'weather-overcast.jpg', self.width, self.height)
        self.storm = GdkPixbuf.Pixbuf.new_from_file_at_size(PATH + 'weather-storm.jpg', self.width, self.height)
        self.set_rain(0.)

    def set_rain(self, rain):
        self.adjustment.set_value(rain)
        if rain < 0.25:
            self.image.set_from_pixbuf(self.clear)
        elif rain < 0.50:
            self.image.set_from_pixbuf(self.soft)
        elif rain < 0.75:
            self.image.set_from_pixbuf(self.hard)
        else:
            self.image.set_from_pixbuf(self.storm)

    def start_record(self):
        self.spinner.start()
        self.record.set_active(True)

    def stop_record(self):
        self.spinner.stop()
        self.record.set_active(False)


def main():
    global RUN
    gui = GUI("GUI.glade")
    t = Thread(target=record_loop, args=(gui,))
    t.start()
    Gtk.main()
    RUN = False
    t.join()


def record_loop(gui):
    while RUN:
        gui.start_record()
        signal = record(RATE, LENGTH)
        rain = analyze(LENGTH, RATE, signal)
        gui.set_rain(rain)
        gui.stop_record()
        print(rain)

        time.sleep(SLEEP)


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
