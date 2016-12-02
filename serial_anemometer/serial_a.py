#!/usr/bin/env python
import serial
import time
import re
import datetime
#import struct


print "WTF!"
port = '/dev/ttyUSB1'  #/dev/ttyUSB0

#Instrument 1



numberOfTimes = 10
print port

ops=open('anemometer_01Dec.csv','a')

#Anemometer
anemometer = serial.Serial(
    port,
    baudrate=19200, 
	timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

cnt=0
while True:

	anemometer.sendBreak()
	time.sleep(1)
	anemometer.write('M1aa\r'.encode())
	anemometer_response = anemometer.readlines()
	M1_resp_str=re.sub('\ +',' ',str(anemometer_response))
	
	
	anemometer.sendBreak()
	time.sleep(1)
	anemometer.write('M2aa\r'.encode())
	anemometer_response = anemometer.readlines()
	M2_resp_str=re.sub('\ +',' ',str(anemometer_response))
	
	
	anemometer.sendBreak()
	time.sleep(1)
	anemometer.write('M3aa\r'.encode())
	anemometer_response = anemometer.readlines()
	M3_resp_str=re.sub('\ +',' ',str(anemometer_response))
	
	anemometer.sendBreak()
	time.sleep(1)
	anemometer.write('M4aa\r'.encode())
	anemometer_response = anemometer.readlines()
	M4_resp_str=re.sub('\ +',' ',str(anemometer_response))
	
	anemometer.sendBreak()
	time.sleep(1)
	anemometer.write('M7nn\r'.encode())
	anemometer_response = anemometer.readlines()
	M7_resp_str=re.sub('\ +',' ',str(anemometer_response))

	now=datetime.datetime.now()
	anemoout=str(now)+","+str(M1_resp_str)+str(M2_resp_str)+str(M3_resp_str)+str(M4_resp_str)+str(M7_resp_str)+"\n"
	ops.write(anemoout)
	
ops.close()
anemometer.close()
