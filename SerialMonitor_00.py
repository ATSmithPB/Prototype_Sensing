#Imports
import serial
import datetime
import os
import time
import csv
import io
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

sessionName = "Session 4"
#Instantiate a new serial connection
ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200
ser._bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.timeout = 1  #Specifies a read timeout in sec
print("Serial Connection Made...")

#Functions
#Returns last full line of a serial stream as string, and removes tail "\n"
def readLatestLine(s):
    while True:
        s.flushInput()
        latestLine = s.readline()
        decodedLine = str(latestLine.decode("utf-8"))
        if len(decodedLine) > 3:
            if decodedLine[0] != "s" and decodedLine[len(decodedLine)-1] != "n" :
                print("Invalid Line, trying again...")
            else:
                return decodedLine[1:len(decodedLine)-2] 
        
loopDelay = 20 #seconds
#Main loop that uploads a serial data to InfluxDB every n seconds
while True:
    serStr = readLatestLine(ser)
    print(serStr)
    serData = serStr.split(',')
    #Initialize InfluxDB client
    token = "-V7PacrGpoiuPn0BUyThutSyoGOAAiwKEhP5YHBkNeR_ZawOzUuF2i-ywf-JopOUfZ_9rCLCJ_74mEP0xiIE4A=="
    org = "atsmitharc@gmail.com"
    url = "https://westeurope-1.azure.cloud2.influxdata.com"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    #Write to InfluxDB with point structure to bucket
    myBucket = "Prototype_02_Sensor_Data"
    write_api = client.write_api(write_options=SYNCHRONOUS)
       
    DBpoint = (
    Point(sessionName)
    .tag("Loc", "55,40,56,N,12,36,15,E")
    .field("A_00", float(serData[0]))
    .field("T_00", float(serData[1]))
    .field("A_01", float(serData[2]))
    .field("T_01", float(serData[3]))
    .field("A_02", float(serData[4]))
    .field("T_02", float(serData[5]))
    .field("A_03", float(serData[6]))
    .field("T_03", float(serData[7]))
    .field("A_04", float(serData[8]))
    .field("T_04", float(serData[9]))
    .field("A_05", float(serData[10]))
    .field("T_05", float(serData[11]))
    #.time(time.time())
    )
    
    print("Uploading...")
        
    write_api.write(bucket = myBucket, org = org, record=DBpoint)

    print("Send Success!")

    time.sleep(loopDelay) # run code every n second
