#!/usr/bin/env python
import csv
from itertools import islice


########################## Functions ########################################### 
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
   if(len(arrResp)==18):
      scale = 16; nbits = 8;
      v3=arrResp[6:8];v2=arrResp[8:10];v1=arrResp[10:12];v0=arrResp[12:14];
      val3=bin(int(v3,scale))[2:].zfill(nbits);val2=bin(int(v2,scale))[2:].zfill(nbits);
      val1=bin(int(v1,scale))[2:].zfill(nbits);val0=bin(int(v0,scale))[2:].zfill(nbits)
      arrVal=translateNum(val3,val2,val1,val0)
      retStr=str(arrVal)+","
      return retStr;
   else:
      return "None,";



#Variable Lists 
now			=	[];
voltage		=	[];
current		=	[];
ac_power	=	[];
app_power	=	[];
reac_power	=	[];
pf			=	[];
ph_angle 	=	[];
freq		=	[];
imp_ac 		=	[];
exp_ac 		=	[];
imp_reac 	=	[];
exp_reac	=	[];
total_ac	=	[];
total_reac 	=	[];
#inv 		=	[];
   
f=open('energy_all_22Nov.csv','r');
res=open('decoded_result.csv','w');
   
for l in f:
   data=l.split(',');
   if(len(data)==16):
      now.append(data[0]);
      voltage.append(data[1]);
      current		.append(data[2]);
      ac_power	.append(data[3]);
      app_power	.append(data[4]);
      reac_power	.append(data[5]);
      pf			.append(data[6]);
      ph_angle 	.append(data[7]);
      freq		.append(data[8]);
      imp_ac 		.append(data[9]);
      exp_ac 		.append(data[10]);
      imp_reac 	.append(data[11]);
      exp_reac	.append(data[12]);
      total_ac	.append(data[13]);
      total_reac 	.append(data[14]);
      #inv 		.append(data[15]);


for n in range(0,len(now)):
   voltage_string    = pprocess(voltage[n]);
   current_string    = pprocess(current[n]);
   ac_power_string   = pprocess(ac_power[n]);
   app_power_string  = pprocess(app_power[n]);
   reac_power_string = pprocess(reac_power[n]);
   pf_string         = pprocess(pf[n]);
   ph_angle_string   = pprocess(ph_angle[n]);
   freq_string       = pprocess(freq[n]);
   imp_ac_string     = pprocess(imp_ac[n]);
   exp_ac_string     = pprocess(exp_ac[n]); 
   imp_reac_string   = pprocess(imp_reac[n]);
   exp_reac_string   = pprocess(exp_reac[n]);
   total_ac_string   = pprocess(total_ac[n]);
   total_reac_string = pprocess(total_reac[n]);
   #inv
   res.write(now[n]+","+voltage_string+current_string+ac_power_string+app_power_string+reac_power_string+pf_string+ph_angle_string+freq_string+imp_ac_string+exp_ac_string+imp_reac_string+exp_reac_string+total_ac_string+total_reac_string+"\n")
