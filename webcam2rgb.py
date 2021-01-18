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
    
import cv2
import threading

class Webcam2rgb():

    def start(self, callback, posl, posr, cameraNumber=0, width = None, height = None, fps = None, directShow = False):
        self.callback = callback
        self.posl = posl
        self.posr = posr
        try:
            self.cam = cv2.VideoCapture(cameraNumber + (cv2.CAP_DSHOW if directShow else cv2.CAP_ANY)) 
            if not self.cam.isOpened():
                print('opening camera')
                self.cam.open(0)
       
            if width:
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
            if height:
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
            if fps:
                self.cam.set(cv2.CAP_PROP_FPS, fps)
            self.running = True
            self.thread = threading.Thread(target = self.calc_BRG)
            self.thread.start()
            self.ret_val = True
        except:
            self.running = False
            self.ret_val = False

    def stop(self):
        self.running = False
        self.thread.join()
        self.cam.release()

    def calc_BRG(self):
        while self.running:
            try:
                self.ret_val = False
                self.ret_val, img = self.cam.read()
                h, w, c = img.shape
                brgl = img[int(h/2),int(w*self.posl)]
                brgr = img[int(h/2),int(w*self.posr)]
                self.callback(self.ret_val,brgl, brgr)
            except:
                self.running = False

    def cameraFs(self):
        return self.cam.get(cv2.CAP_PROP_FPS)