#! /usr/bin/python3
# _*_ coding: utf-8 _*_

import socket
from time import sleep
import matplotlib.pyplot as plt
import math
import statistics

host = '192.168.0.1'
port = 2111

# Open Socket Connection
serverConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverConnection.connect((host, port))
	
# Start Data Received
serverConnection.send(str.encode("\x02sEN LMDscandata 1\x03"))
reply = serverConnection.recv(1024) # Respoince of LiDAR

# Collect Data
rowData = []
for i in range(0, 11):
	rowData.append(serverConnection.recv(1024))

# Data Processing
initEnvironement = []
for i in range(0, int(rowData[0].decode('utf-8').split(' ')[25], 16)):
	valueAngle = []
	for j in range(0, 11):
		if int(rowData[j].decode('utf-8').split(' ')[26+i], 16)/1000 >= 0.02:
			valueAngle.append(int(rowData[j].decode('utf-8').split(' ')[26+i], 16)/1000)
		else:
			valueAngle.append(10)
	initEnvironement.append(statistics.median(valueAngle)) # Calculed median on 11 values

# Defind List of Angles
angle = []
for i in range(0, 181):
	angle.append(math.radians(i))

# Stop  Data Received
serverConnection.send(str.encode("\x02sEN LMDscandata 0\x03"))

# Close Socket Connection
serverConnection.close()

# Plot Data Received
plt.polar(angle, initEnvironement, color='#ffa500', ls='-', label='H')
plt.title('LiDAR SICK TiM561')
plt.show()

