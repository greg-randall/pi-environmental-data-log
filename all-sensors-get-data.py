#sensor libs:
import smbus
import bme680
import Adafruit_ADS1x15

from datetime import datetime
import time
import os
from ftplib import FTP
import sys
from ftpconfig import * #credentials for ftp. done this way to keep them from getting added to git
from loggingperiodconfig import *


##########################################################

#setup sensors:
#sound 
soundsensor = Adafruit_ADS1x15.ADS1015()
GAIN = 1 #see datasheet for gain table, 1 = +/-4.096V
soundsensor.start_adc(0, gain=GAIN)

#light
lightsensor = smbus.SMBus(1)
lightsensor.write_byte_data(0x39, 0x00 | 0x80, 0x03)
lightsensor.write_byte_data(0x39, 0x01 | 0x80, 0x02)

#enviromental
enviromentalsensor = bme680.BME680()
enviromentalsensor.set_humidity_oversample(bme680.OS_2X)
enviromentalsensor.set_pressure_oversample(bme680.OS_4X)
enviromentalsensor.set_temperature_oversample(bme680.OS_8X)
enviromentalsensor.set_filter(bme680.FILTER_SIZE_3)
enviromentalsensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
enviromentalsensor.set_gas_heater_temperature(320)
enviromentalsensor.set_gas_heater_duration(150)
enviromentalsensor.select_gas_heater_profile(0)

##########################################################

headers = "time (central), date, cpu temperature C, temperature C, pressure kPa, %RH, voc ohm, visible light lux, infrared light lux, sound dBa\n"

if os.path.exists("data/log.csv"):
  outputfile = open("data/log.csv","a")
  outputfile.write("system restarted\n")
else:
  if os.path.isdir("data"):
    outputfile = open("data/log.csv","a")
    outputfile.write(headers)
  else:
    os.mkdir("data")
    outputfile = open("data/log.csv","a")
    outputfile.write(headers)

  if not os.path.isdir("data/upload"):
    os.mkdir("data/upload")

  if not os.path.isdir("data/uploaded"):
    os.mkdir("data/uploaded")
  

print headers

##########################################################

timeperiodstart = time.time()
try:
  while True:

    #sound
    rawsound = soundsensor.get_last_result()
    sounddba = rawsound / 10.0


    #light
    lightraw = lightsensor.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
    lightraw1 = lightsensor.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    fullspectrumlight = lightraw[1] * 256 + lightraw[0]
    infraredlight = lightraw1[1] * 256 + lightraw1[0]
    visiblelight = fullspectrumlight - infraredlight


    #envriomental
    enviromentalsensor.get_sensor_data()
    temperature = enviromentalsensor.data.temperature
    pressure = enviromentalsensor.data.pressure
    humidity = enviromentalsensor.data.humidity
    if enviromentalsensor.data.heat_stable:
      voc = enviromentalsensor.data.gas_resistance
    else:
      voc = 0

    #cpu temperature
    cputemperature = os.popen("vcgencmd measure_temp").readline()
    cputemperature = cputemperature.replace("temp=","")
    cputemperature = float(cputemperature.replace("'C",""))


##########################################################	

    data = datetime.now().strftime("%H:%M:%S.%f, %m/%d/%Y") + ", " + str(cputemperature) + ", " + str(temperature) + ", " + str(pressure) + ", " + str(humidity) + ", " + str(voc) + ", " + str(visiblelight) + ", " + str(infraredlight) + ", " + str(sounddba)
    print data

    outputfile.write(data + "\n")

    time.sleep(loggingperiod)

    if time.time() - timeperiodstart >= uploadperiod * 60:
      outputfile.close()
      newfilename = str(datetime.now().strftime("log_%m-%d-%Y_%H-%M-%S.csv"))
      os.rename("data/log.csv", "data/upload/" + newfilename)
      outputfile = open("data/log.csv","a")
      outputfile.write(headers)
      timeperiodstart = time.time()
      print "Output CSV Split: " + newfilename
 
except KeyboardInterrupt:
  pass

outputfile.close()
