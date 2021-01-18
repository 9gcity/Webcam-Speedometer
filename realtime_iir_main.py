''' Program to measure object speed using a webcam
    Copyright (C) 2020  Bernd Porr, Gautam Gupta, Darius Nikiperavicius

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
    
import numpy as np
from scipy import signal
import iir_filter as iir
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import webcam2rgb
import time

class RealtimePlotWindow:
    def __init__(self, channel: str, yscale):
        # create a plot window
        self.fig, self.ax = plt.subplots()
        self.yscale = yscale
        plt.title(f"Channel: {channel}")
        # that's our plotbuffer
        self.plotbuffer = np.zeros(500)
        # create an empty line
        self.line, = self.ax.plot(self.plotbuffer)
        # axis
        self.ax.set_ylim(0, 1)
        # That's our ringbuffer which accumluates the samples
        # It's emptied every time when the plot window below
        # does a repaint
        self.ringbuffer = []
        # add any initialisation code here (filters etc)
        # start the animation
        self.ani = animation.FuncAnimation(self.fig, self.update, interval=100)

    # updates the plot
    def update(self, data):
        # add new data to the buffer
        self.plotbuffer = np.append(self.plotbuffer, self.ringbuffer)
        # only keep the 500 newest ones and discard the old ones
        self.plotbuffer = self.plotbuffer[-500:]
        self.ringbuffer = []
        # set the new 500 points of channel 9
        self.line.set_ydata(self.plotbuffer)
        self.ax.set_ylim(0, self.yscale)
        return self.line

    # appends data to the ringbuffer
    def addData(self, v):
        self.ringbuffer.append(v)

class velocity:
    def __init__(self, th, d, wpx, a, b):  # th- thershold for detection
        self.flag = 2
        self.t1 = 0
        self.deltatime = 0
        self.th = th
        scale = a*d + b  # linear formula for px/cm factor calculation
        self.width = wpx / scale  # width in cm at distance d
        self.speed = 0
        self.speed_array = []

    def calc(self, left, right):
        self.speed_array = [left, right]
        if max(self.speed_array) > self.th:
            if self.flag == 2:
                self.t1 = time.time()
                self.flag = self.speed_array.index(max(self.speed_array))
            if self.flag != self.speed_array.index(max(self.speed_array)) and self.flag != 2:
                self.deltatime = time.time() - self.t1
                # print(self.deltatime)
                self.speed = self.width / self.deltatime / 100  # divide by 100 for m/s
                print('Object speed is: %.2f m/s' % self.speed)
                self.flag = 2


print("Please enter object distance to the camera in cm:")
d_to_cam = int(input())
#-----------------Filter parameters------------------
fs = 30  # sampling freq
fc = np.array([3, 8])  # cutoff freq
order = 4  # filter order
coeff = signal.butter(order, 2 * fc / fs, output='sos', btype="bandpass")  # 2*fc/fs normalises fc to nyquist
threshold = 10
#----------------------------------------------------

#----------------Camera parameters-------------------
#Linear formula parameters specific to acer 575g laptop:
param_a = -1.25 
param_b = 75
#Webcam resolution:
cam_width = 1280
cam_height= 720
#Detector pixels position:
pos_l = 1/5  #Fractional position of the left pixel
pos_r = 4/5  #Fractional position of the right pixel
# Distance between two measurment points in pixels (on the sensor):
wpx = int(pos_r*cam_width)-int(pos_l*cam_width)
#----------------------------------------------------

#create filters
highpass1 = iir.IIRFilter(coeff)
highpass2 = iir.IIRFilter(coeff)

#create the velocity calculation instance
vel = velocity(threshold, d_to_cam, wpx, param_a, param_b) 

#create plots
realtimePlotWindowLeft = RealtimePlotWindow("Left", 50)
realtimePlotWindowRight = RealtimePlotWindow("Right", 50)
realtimePlotWindowLeftunf = RealtimePlotWindow("Left_unfiltered", 255)
realtimePlotWindowRightunf = RealtimePlotWindow("Right,unfiltered", 255)


# create callback method reading camera and plotting in windows
def hasData(retval, brgl, brgr):
    left = highpass1.filter(brgl[2])
    right = highpass2.filter(brgr[2])
    vel.calc(left, right)
    realtimePlotWindowLeft.addData(left)
    realtimePlotWindowRight.addData(right)
    realtimePlotWindowLeftunf.addData(brgl[2])
    realtimePlotWindowRightunf.addData(brgr[2])

# create instances of camera
# start the thread and stop it when we close the plot windows
camera = webcam2rgb.Webcam2rgb()
camera.start(callback=hasData, posl=pos_l, posr=pos_r, width=cam_width, height=cam_height, cameraNumber=0)
plt.show()
camera.stop()
print('finished')