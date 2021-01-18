''' Webcam sampling rate and jitter testing program
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

import numpy as np
import matplotlib.pyplot as plt
import webcam2rgb
import time

calltime = np.array([]) #array for storing times of callback execution
deltatime = np.array([]) #array for storing time differences

# create callback method reading camera and storing the time at which function was called
def hasData(retval, brgl, brgr):
    global calltime
    calltime = np.append(calltime, time.perf_counter())

# create instances o camera
# start the thread and stop it after 10 seconds
camera = webcam2rgb.Webcam2rgb()
camera.start(callback=hasData, posl=0.2, posr=0.8, width=1280, height=720, cameraNumber=0)
print("camera samplerate: ", camera.cameraFs(), "Hz")
time.sleep(10)
camera.stop()
print('finished')


#calculate delta time for each execution
for i in range(1, len(calltime)):
    deltatime = np.append(deltatime, calltime[i]-calltime[i-1])

totaltime = calltime[len(calltime)-1]-calltime[0]
tsmpl = totaltime/len(calltime) #true sampling rate
tfs = 1/tsmpl
plt.figure("Jitter over sample No.")
plt.plot((deltatime-tsmpl)*1000)
plt.xlabel("Sample No.")
plt.ylabel("Jitter, ms")
print('Total time measured: %.2f s' % totaltime)
print('Actual sample rate: %.2f Hz' % tfs)
print('Average jitter time: %.2f ms' % np.average(abs(deltatime-tsmpl)*1000))
print("Max jitter time: %.2f ms" % np.max(abs(deltatime-tsmpl)*1000))
print("Min jitter time: %.2f ms" % np.min(abs(deltatime-tsmpl)*1000))
plt.savefig('jitter.svg')
plt.show()