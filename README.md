===================================================================================================
READ ME - WEBCAM SPEEDOMETER PROGRAM
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
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

=====================================================================================================

1. SETUP

To use this program, you must have downloaded in the same folder iir_filter.py and webcam2rgb.py. You
also need to install OpenCV libraries. This can be done by typing the following code into your terminal
	pip3 install opencv-contrib-python
	pip3 install opencv-python

2. DISTANCE TO CAMERA

3. ADDITIONAL NOTES
	
	3.1 iir_filter.py contains an additional unit test in order to verify the validity of the IIR
	filter implementation. Additional information can be found in the report included.
	
	3.2 jittercalc.py is also included in the folder, which can be run to check the jitter in your
	webcam readings. This also requires the Open CV library to be installed. Additional information 
	can be found in the report included.

	3.3 Coefficients for the IIR filter implementation are calculated using the Butterworth formula,
	but this can be modified for user's specifications.

4. SCALING PARAMETERS
	4.1 param_a and param_b are linear function parameters which must derived for specific webcam hardware.
	This can be done by taking two photos of a object of fixed length L, one at distance d1 and another
	at d2. Then in photo editing software or otherwise the length of the object in pixels must be measured
	for each photo, wpx1 and wpx2. The scaling factor is param_a*d+param_b. Thus two equation can be written
	down: L=wpx1*(param_a*d1+param_b);L=wpx2*(param_a*d2+param_b). Solve these simultaneous equations for 
	param_a and param_b and enter them into the program. 

5. Youtube links to the demonstration:
	Before filtering: https://www.youtube.com/watch?v=Rva1DnmSsbg
	After filtering: https://www.youtube.com/watch?v=AtqBpBm9rSI
	
