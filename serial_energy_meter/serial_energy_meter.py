#!/usr/bin/env python
import serial
import datetime
import struct
import binascii
import numpy as np


print "WTF!"
port = '/dev/ttyUSB0'
print port

ops=open('energy_all_01Dec.csv','a')


###################################################### Energy Meter ############################################################

def crcgen(dataArr,count):
   "Generates the CRC"
   error_word =  np.uint16(0xffff);

   if (count == 0):
      return (error_word);

   for byte in range(count):
      error_word = error_word ^ dataArr[byte];
      for i in range(0,8):
         lsb = error_word & 0x0001;
         if (lsb == 1):
            error_word = error_word-1;
         error_word = error_word/2;
         if (lsb == 1):
            error_word = error_word ^ 0xA001


   return (error_word)

#Volt Array
data_array=[0x09,0x04,0x00,0x00,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
volt_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Current Array
data_array=[0x09,0x04,0x00,0x06,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
current_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Active Power Array
data_array=[0x09,0x04,0x00,0x0C,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
ac_power_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Apparent Power Array
data_array=[0x09,0x04,0x00,0x12,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
app_power_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Reactive Power Array
data_array=[0x09,0x04,0x00,0x18,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
reac_power_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Power Factor
data_array=[0x09,0x04,0x00,0x1E,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
pf_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Phase Angle
data_array=[0x09,0x04,0x00,0x24,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
ph_angle_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Frequency Array
data_array=[0x09,0x04,0x00,0x46,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
f_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Import Active Energy Array
data_array=[0x09,0x04,0x00,0x48,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
imp_ac_energy_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Export Active Energy Array
data_array=[0x09,0x04,0x00,0x4A,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
exp_ac_energy_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Import Reactive Energy Array
data_array=[0x09,0x04,0x00,0x4C,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
imp_reac_energy_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Export Reactive Energy Array
data_array=[0x09,0x04,0x00,0x4E,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
exp_reac_energy_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Total Active Energy Array
data_array=[0x09,0x04,0x01,0x56,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
total_ac_energy_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])

#Total Reactive Energy Array
data_array=[0x09,0x04,0x01,0x58,0x00,0x02]
inp_crc=np.uint16(data_array);
arrayLen = len(data_array);
crc=np.uint16(crcgen(inp_crc,arrayLen));
crc_high = crc >> 8;
crc_low = crc & 0xFF;
total_reac_energy_array=bytearray([data_array[0],data_array[1],data_array[2],data_array[3],data_array[4],data_array[5],crc_low,crc_high])



energy_meter = serial.Serial(
   port,
   baudrate=9600, 
   timeout=1,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS

)


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
   energy_meter.write(volt_array);
   volt_resp = energy_meter.readline();

   energy_meter.write(current_array);
   current_resp = energy_meter.readline();

   energy_meter.write(ac_power_array);
   ac_power_resp = energy_meter.readline();

   energy_meter.write(app_power_array);
   app_power_resp = energy_meter.readline();

   energy_meter.write(reac_power_array);
   reac_power_resp = energy_meter.readline();

   energy_meter.write(pf_array);
   pf_resp = energy_meter.readline();

   energy_meter.write(ph_angle_array);
   ph_angle_resp = energy_meter.readline();

   energy_meter.write(f_array);
   f_resp = energy_meter.readline();
   
   energy_meter.write(imp_ac_energy_array);
   imp_ac_energy_resp = energy_meter.readline();

   energy_meter.write(exp_ac_energy_array);
   exp_ac_energy_resp = energy_meter.readline();

   energy_meter.write(imp_reac_energy_array);
   imp_reac_energy_resp = energy_meter.readline();

   energy_meter.write(exp_reac_energy_array);
   exp_reac_energy_resp = energy_meter.readline();

   energy_meter.write(total_ac_energy_array);
   total_ac_energy_resp = energy_meter.readline();

   energy_meter.write(total_reac_energy_array);
   total_reac_energy_resp = energy_meter.readline();

#   inverter.write(data_array_inverter);
#   inv_resp = inverter.readline();

   now=datetime.datetime.now();

   #Writing to a file
  
   ops.write(str(now)+","+\
   str(binascii.hexlify(volt_resp))+","+\
   str(binascii.hexlify(current_resp))+","+\
   str(binascii.hexlify(ac_power_resp))+","+\
   str(binascii.hexlify(app_power_resp))+","+\
   str(binascii.hexlify(reac_power_resp))+","+\
   str(binascii.hexlify(pf_resp))+","+\
   str(binascii.hexlify(ph_angle_resp))+","+\
   str(binascii.hexlify(f_resp))+","+\
   str(binascii.hexlify(imp_ac_energy_resp))+","+\
   str(binascii.hexlify(exp_ac_energy_resp))+","+\
   str(binascii.hexlify(imp_reac_energy_resp))+","+\
   str(binascii.hexlify(exp_reac_energy_resp))+","+\
   str(binascii.hexlify(total_ac_energy_resp))+","+\
   str(binascii.hexlify(total_reac_energy_resp))+","+\
   #str(binascii.hexlify(inv_resp.strip()))+#
      "\n");

   #ops.write(inv_resp)



   

inverter.close()
energy_meter.close()
   
