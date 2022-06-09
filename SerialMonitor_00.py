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
#Returns the last full line in a serial stream
def readLatestLine(s):
    print("Reading Latest Line...")
    s.flushInput()
    latestLine = s.readline()
    return latestLine

loopDelay = 5 #seconds
#Main loop that uploads a serial data to InfluxDB every n seconds
while True:
    ser_bytes = readLatestLine(ser)
    print("Decoding...")
    decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    print(decoded_bytes)
    serData = decoded_bytes.split(',')
    
    #Initialize InfluxDB client
    token = "-V7PacrGpoiuPn0BUyThutSyoGOAAiwKEhP5YHBkNeR_ZawOzUuF2i-ywf-JopOUfZ_9rCLCJ_74mEP0xiIE4A=="
    org = "atsmitharc@gmail.com"
    url = "https://westeurope-1.azure.cloud2.influxdata.com"
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

    #Write to InfluxDB with point structure to bucket
    myBucket = "Prototype_02_Sensor_Data"
    write_api = client.write_api(write_options=SYNCHRONOUS)
       
    DBpoint = (
    Point("Session 2")
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
