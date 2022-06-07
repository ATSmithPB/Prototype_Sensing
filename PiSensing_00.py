#Imports
from http import client
import os
import glob
import time
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#Instantiate InfluxDB Client
token = os.environ.get("INFLUXDB_TOKEN")
org = "atsmitharc@gmail.com"
url = "https://westeurope-1.azure.cloud2.influxdata.com"
client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

#Classes
class DS18B20:
    #Constructors

    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28')
        self._count_devices = len(device_folder)
        self._devices = list()
        i = 0
        while i < self._count_devices:
            self._devices.append(device_folder[i] + '/w1_slave')
            i += 1

    def device_names(self):
        names = list()
        for i in range(self._count_devices):
            names.append(self._devices[i])
            temp = names[i][20:35]
            names[i] = temp
            
            return names

    def _read_temp(self, index):
        f = open(self._devices[index], 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def tempC(self, index = 0):
        lines = self.read_temp(index)
        retries = 5
        while (lines[0].strip()[-3:] != 'YES') and (retries > 0):
            time.sleep(0.1)
            lines = self._read_temp(index)
            retries -= 1

            if retries == 0: 
                return 998
    
    def device_count(self):
        return self._count_devices

#main program startup
degree_sign = u'\xb0' #degree sign
devices = DS18B20()
count = devices.device_count()
names = devices.device_names()
temps = []

while True:
    i = 0
    while i < count:
    temps[i] = devices.tempC(i)
    i = i + 1
    time.sleep(1)
    break

#Send Data to InfluxDB bucket
bucket="Prototype_02_Sensor_Data bucket"
write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="atsmitharc@gmail.com", record=point)
  time.sleep(1) # separate points by 1 second
