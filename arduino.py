import serial # For controlling the Uno
import time # DEBUG for sleeping
# Recommended Pi port.
# arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
# Port corresponding to COM3 when running through WSL
arduinoSerialData = serial.Serial('/dev/ttyS3',9600)
currTime = int(round(time.time()))
while 1:
	while(arduinoSerialData.in_waiting>0):
		#print('RX: ', end='')
		c = arduinoSerialData.read()
		print(c)

	oldTime = currTime
	currTime = int(round(time.time()))
	if(oldTime == currTime):
		continue
	if currTime % 10 == 5:
		arduinoSerialData.write('1')
		print('TX: 1')
	elif currTime % 10 == 0:
		arduinoSerialData.write('0')
		print('TX: 0')