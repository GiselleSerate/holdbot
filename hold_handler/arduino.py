import serial # For controlling the Uno
import time # DEBUG for sleeping
# Recommended Pi port.
# arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
# Port corresponding to COM3 when running through WSL
try:
	arduinoSerialData = serial.Serial('/dev/ttyACM0',9600)
except: 
	arduinoSerialData = serial.Serial('/dev/ttyACM1',9600)
def alert_action():
	currTime = int(round(time.time()))
	oldTime = currTime
	currTime = int(round(time.time()))
	if(oldTime == currTime):
		pass
		#continue
	if currTime % 10 == 5:
		arduinoSerialData.write(b'2')
	#	print('TX: 1')
	elif currTime % 10 == 0:
		arduinoSerialData.write(b'0')
		print('TX: 0')


while True:
	alert_action()
	time.sleep(0.5)
