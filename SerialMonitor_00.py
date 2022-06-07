import serial
import os
import time
import csv
import io

#Instantiate a new serial connection
ser = serial.Serial('/dev/ttyACM0')
ser.baudrate = 115200
ser._bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.timeout = 1 #Specifies a read timeout in sec

def receiving(ser):
    global last_received
    buffer_string = b''
    while True:
        buffer_string = buffer_string + ser.read(ser.inWaiting())
        if '\n' in buffer_string:
            lines = buffer_string.split('\n')
            last_received = lines[-2]
            buffer_string = lines[-1]
    return last_received

ser_bytes = receiving(ser)
decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
print(decoded_bytes)
with open('/home/atsmithpb/Desktop/currentCLK.csv', "w") as f:
    f.write(decoded_bytes)