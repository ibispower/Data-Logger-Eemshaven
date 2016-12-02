#!/usr/bin/env python
import csv
from itertools import islice


all_data=open('inverter_12Oct_2.csv','r')
processed_inverter=open('inverter_p_12Oct_2.csv','w')
processed_inverter.write("Time,DC Input Voltage,DC Input Current,Total Energy,Grid Voltage,Grid Current,Grid Frequency,Inverter Temperature\n")

for row in islice(all_data, 0, None, 2):
	split_row=row.split(',');
	data=split_row[1];
	if(len(data)==53):
		dc_input_voltage_h		=	data[10]+data[11]+data[8]+data[9];
		dc_input_current_h		=	data[14]+data[15]+data[12]+data[13];
		grid_voltage_h			=	data[18]+data[19]+data[16]+data[17];
		grid_current_h			=	data[22]+data[23]+data[20]+data[21];
		inverter_temperature_h	=	data[26]+data[27]+data[24]+data[25];
		total_energy_h			=	data[34]+data[35]+data[32]+data[33]+data[30]+data[31]+data[28]+data[29];
		grid_frequency_h		=	data[50]+data[51]+data[48]+data[49];
		
		dc_input_voltage		=	int(dc_input_voltage_h,16)/10;
		dc_input_current		=	int(dc_input_current_h,16)/10;
		dc_input_power			= 	dc_input_current*dc_input_voltage;
		grid_voltage			=	int(grid_voltage_h,16)/10;
		grid_current			=	int(grid_current_h,16)/10;
		inverter_temperature	=	int(inverter_temperature_h,16)/10;
		total_energy			=	int(total_energy_h,16);
		grid_frequency			=	int(grid_frequency_h,16)/100;
		processed_inverter.write(split_row[0]+","+str(dc_input_voltage)+","+str(dc_input_current)+","+str(total_energy)+","+str(grid_voltage)+","+str(grid_current)+","+str(grid_frequency)+","+str(inverter_temperature)+"\n")
