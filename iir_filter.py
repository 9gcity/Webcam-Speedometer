''' IIR Filter Class Implementation
    Copyright (C) 2020  Gautam Gupta, Darius Nikiperavicius

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class IIR2Filter:
    def __init__(self, coefficient):
        self.b0 = coefficient[0]  # FIR coeff b0
        self.b1 = coefficient[1]  # FIR coeff b1
        self.b2 = coefficient[2]  # FIR coeff b2
        self.a1 = coefficient[4]  # IIR coeff a1
        self.a2 = coefficient[5]  # IIR coeff a2
        self.buffer1 = 0  # First delay buffer
        self.buffer2 = 0  # Second delay buffer
        self.input_acc = 0  # Input accumulator
        self.output_acc = 0  # Output accumulator

    def filter(self, input):
        # Calculate the accumulators
        self.input_acc = input - (self.a1 * self.buffer1) - (self.a2 * self.buffer2)
        self.output_acc = (self.b0 * self.input_acc) + (self.b1 * self.buffer1) + (self.b2 * self.buffer2)

        # Update the delay line
        self.buffer2 = self.buffer1
        self.buffer1 = self.input_acc

        return self.output_acc


class IIRFilter:
    def __init__(self, coefficients):
        self.coefficients = coefficients  # The coefficients for the filter
        self.fil = []  # Set up the filter array
        for i in range(0, len(self.coefficients)):  # Loop to create the Direct Form 2 IIR filters
            self.fil.append(IIR2Filter(self.coefficients[i]))

    def filter(self, inp):  # Function to take in input and send it through the filter array
        out = 0
        for i in range(0, len(self.coefficients)):
            out = self.fil[i].filter(inp)
            inp = out
        return out


if __name__ == '__main__':  # UNIT TEST IMPLEMENTATION
    fs = 30  # sampling freq
    fc = np.array([5, 10])  # cutoff freq
    order = 2  # filter order
    coeff = signal.butter(order, 2 * fc / fs, output='sos', btype="bandpass")  # 2*fc/fs normalises fc to nyquist
    b, a = signal.butter(order, 2 * fc / fs, btype="bandpass")  # 2*fc/fs normalises fc to nyquist

    test = IIRFilter(coeff)
    deltaimp = np.zeros(500)  # creating a delta impulse
    deltaimp[0] = 1
    testout = np.zeros(500)
    finaloutput = np.zeros(251)
    for i in range(0, len(deltaimp)):
        testout[i] = test.filter(deltaimp[i])
    testout = 20 * np.log10(np.abs(np.fft.fft(testout)))
    for i in range(0, len(deltaimp)):
        if i <= 250:
            finaloutput[i] = testout[i]
    fxaxis = np.linspace(0, fs/2, len(finaloutput))
    plt.figure('Our Filter CLass Implementation superimposed onto Freqz Implementation')
    plt.plot(fxaxis, finaloutput, label="Our Implementation")

    w, h = signal.freqz(b, a)
    plt.plot(np.linspace(0, fs / 2, 512), 20 * np.log10(np.abs(h)), label="Freqz Implementation")
    plt.legend()
    plt.xlabel("Frequency (in Hz)")
    plt.ylabel("Amplitude, dB")
    plt.show()

