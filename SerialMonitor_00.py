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

#Returns last full line from Serial buffer
def receiving(s):
    last_received = b''
    buffer_string = b''
    while True:
        buffer_string = buffer_string + s.read(s.inWaiting())
        if b'\n' in buffer_string:
            lines = buffer_string.split(b'\n')
            last_received = lines[-2]
            buffer_string = lines[-1]
            if len(lines) >= 3:
                return last_received
            
#Decode last full line from serial buffer and write to file
ser_bytes = receiving(ser)
decoded_bytes = str(ser_bytes[0:len(ser_bytes)].decode("utf-8"))
print(decoded_bytes)
with open('/home/atsmithpb/Desktop/currentCLK.csv', "w") as f:
    f.write(decoded_bytes)