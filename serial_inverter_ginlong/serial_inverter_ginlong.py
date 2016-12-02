#!/usr/bin/env python
import serial
import datetime
import struct
import binascii
import numpy as np


print "WTF!"
port = '/dev/ttyUSB0'
print port

ops=open('inverter_01Dec.csv','a')




#################################################################   Inverter ############################################################################

data_array_inverter=bytearray([0x7E,0x06,0xA1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xA7]) 

#inverter
inverter = serial.Serial(
    port,
    baudrate=9600, 
	timeout=1,
	#parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

########################################################################################################################################################


while True:
   
   inverter.write(data_array_inverter);
   inv_resp = inverter.readline();

   now=datetime.datetime.now();

   #Writing to a file
  
   ops.write(str(now)+","+str(binascii.hexlify(inv_resp.strip()))+"\n");

   



   

inverter.close()
   
