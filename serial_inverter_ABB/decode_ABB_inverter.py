#!/usr/bin/env python

def translateNum(val3,val2,val1,val0):
   """Calculates the value from the inverter as given on Pg.9 of the communication protocol"""
   
   rval0=val0[::-1]; #Reverse the string
   rval1=val1[::-1]; #Reverse the string
   rval2=val2[::-1]; #Reverse the string
   rval3=val3[::-1]; #Reverse the string
   val=rval0+rval1+rval2+rval3;

   exponent=0;mantissa=0;
   
   sgn = int(val[31]);

   
   for i in range(23,31):
      exponent=exponent+int(val[i])*(2**(i-23));
      
   for i in range(0,22):
      mantissa=mantissa+int(val[22-i])*(2**(-i-1));
   
   retVal=(-1)**sgn * (1+mantissa) * 2**(exponent-127) 
   return retVal

def pprocess(arrResp):
   """Post Process the output from the inverter"""
   scale = 16; nbits = 8;
   v3=arrResp[4:6];v2=arrResp[6:8];v1=arrResp[8:10];v0=arrResp[10:12];
   val3=bin(int(v3,scale))[2:].zfill(nbits);val2=bin(int(v2,scale))[2:].zfill(nbits);
   val1=bin(int(v1,scale))[2:].zfill(nbits);val0=bin(int(v0,scale))[2:].zfill(nbits)
   arrVal=translateNum(val3,val2,val1,val0)
   retStr=str(arrVal)+","
   return retStr;

   
f=open('inverter.csv','r');
g=open('inverter_2.csv','a');  
g.write("Now,Grid_Voltage,Grid_Current,Grid_Power,Input_1_Voltage,Input_1_Current,Input_2_Voltage,Input_2_Current\n");
count=0  
for l in f:
	
   now=(l.strip().split(","))[0];
   grid_voltage_resp=(l.strip().split(","))[1];
   grid_current_resp=(l.strip().split(","))[2];
   grid_power_resp=(l.strip().split(","))[3];
   input_1_voltage_resp=(l.strip().split(","))[4];
   input_1_current_resp=(l.strip().split(","))[5];
   input_2_voltage_resp=(l.strip().split(","))[6];
   input_2_current_resp=(l.strip().split(","))[7];

   if(grid_voltage_resp!="" and grid_current_resp!="" and grid_power_resp!="" and input_1_voltage_resp!="" and input_1_current_resp!="" and input_2_voltage_resp!="" and input_2_current_resp!=""):
      gvResp=pprocess(grid_voltage_resp);
      gcResp=pprocess(grid_current_resp);
      gpResp=pprocess(grid_power_resp);
      i1vResp=pprocess(input_1_voltage_resp);
      i1cResp=pprocess(input_1_current_resp);
      i2vResp=pprocess(input_2_voltage_resp);
      i2cResp=pprocess(input_2_current_resp);
      prStr=now+","+gvResp+gcResp+gpResp+i1vResp+i1cResp+i2vResp+i2cResp+"\n";
      g.write(prStr)
      
f.close()
g.close()
	
