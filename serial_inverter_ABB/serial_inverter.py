#!/usr/bin/env python
import serial
import time
import struct
import ctypes
import numpy as np
import datetime

print "WTF!"
port = '/dev/ttyUSB1'
numberOfTimes = 1
print port

POLY=0x8408

def crcgen(dataArr,count):
   "Generates the CRC"
   crc =  np.uint16(0xffff);
   data = np.uint16(0xffff);
   cntr = 0;

   if (count == 0):
      return (~crc);
   
   while (count):
      data=0xff & dataArr[cntr];

      for i in range(0,8):
         if ((crc & 0x0001) ^ (data & 0x0001)):
            crc = (crc >> 1) ^ POLY;
         else:
            crc >>=  1;
         data >>= 1;
         
      cntr=cntr + 1;
      count=count-1;

   return (~crc)



def genCommand (dataArr):
   """Generates Command to be sent to inverter"""
   inp_crc=np.uint16(dataArr);
   arrayLen = len(dataArr);
   crc=np.uint16(crcgen(inp_crc,arrayLen));
   crc_high = crc >> 8;
   crc_low = crc & 0xFF;
   #   print (crc_high,crc_low)
   sendStr=bytearray([dataArr[0],dataArr[1],dataArr[2],dataArr[3],dataArr[4],dataArr[5],dataArr[6],dataArr[7],crc_low,crc_high])
   return (sendStr)
   
def requestGridVoltage(address):
    """Generates the data array to be sent to inverter for requesting grid voltage. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,1,0,0,0,0,0]);
    return (data_array)
    
def requestGridCurrent(address):
    """Generates the data array to be sent to inverter for requesting grid current. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,2,0,0,0,0,0]);
    return (data_array)

def requestGridPower(address):
    """Generates the data array to be sent to inverter for requesting grid power. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,3,0,0,0,0,0]);
    return (data_array)

def requestInpVolt1(address):
    """Generates the data array to be sent to inverter for requesting input 1 voltage. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,23,0,0,0,0,0]);
    return (data_array)

def requestInpCurrent1(address):
    """Generates the data array to be sent to inverter for requesting input 1 current. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,25,0,0,0,0,0]);
    return (data_array)

def requestInpVolt2(address):
    """Generates the data array to be sent to inverter for requesting input 2 voltage. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,26,0,0,0,0,0]);
    return (data_array)

def requestInpCurrent2(address):
    """Generates the data array to be sent to inverter for requesting input 2 current. As per the instructions given on Pg. 8 of the communication protocol"""
    data_array=([address,59,27,0,0,0,0,0]);
    return (data_array)

    



   
#inverter
inverter = serial.Serial(
    port,
    baudrate=19200, 
	timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

address=6
respRange = 8 # 8 byte answer response
inv_file=open("inverter_response30June.csv","a")
inv_file.write("Now,Grid_Voltage,Grid_Current,Grid_Power,Input_1_Voltage,Input_1_Current,Input_2_Voltage,Input_2_Current\n")

while True:
   
   voltGArr=requestGridVoltage(address);
   sendLst=genCommand(voltGArr);
   inverter.write(sendLst);
   inv_resp = inverter.read(size=10);
   vGResp= inv_resp.encode("hex")
      
   currGArr=requestGridCurrent(address);
   sendLst=genCommand(currGArr);
   inverter.write(sendLst);
   inv_resp=inverter.read(size=10);
   cGResp= inv_resp.encode("hex");

   powGArr=requestGridPower(address);
   sendLst=genCommand(powGArr);
   inverter.write(sendLst);
   inv_resp=inverter.read(size=10);
   pGResp= inv_resp.encode("hex");

   inpV1Arr=requestInpVolt1(address);
   sendLst=genCommand(inpV1Arr);
   inverter.write(sendLst);
   inv_resp=inverter.read(size=10);
   inpV1Resp= inv_resp.encode("hex")

   inpC1Arr=requestInpCurrent1(address);
   sendLst=genCommand(inpC1Arr);
   inverter.write(sendLst);
   inv_resp=inverter.read(size=10);
   inpC1Resp= inv_resp.encode("hex")

   inpV2Arr=requestInpVolt2(address);
   sendLst=genCommand(inpV2Arr);
   inverter.write(sendLst);
   inv_resp=inverter.read(size=10);
   inpV2Resp= inv_resp.encode("hex")
   
   inpC2Arr=requestInpCurrent2(address);
   sendLst=genCommand(inpC2Arr);
   inverter.write(sendLst);
   inv_resp=inverter.read(size=10);
   inpC2Resp= inv_resp.encode("hex")

   now = datetime.datetime.now();

#   print str(now)+","+vGResp+cGResp+pGResp+inpV1Resp+inpC1Resp+inpV2Resp+inpC2Resp
   inv_file.write(str(now)+","+vGResp+","+cGResp+","+pGResp+","+inpV1Resp+","+inpC1Resp+","+inpV2Resp+","+inpC2Resp+"\n");
   
   

inverter.close()
   
