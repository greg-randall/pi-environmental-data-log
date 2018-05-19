#sensor libs:
import smbus
import bme680
import Adafruit_ADS1x15

from datetime import datetime #for the microseconds time
import time #general timing of the program
import os #creating/renaming files and folders
#from ftplib import FTP
#import sys
#from ftpconfig import * #credentials for ftp. done this way to keep them from getting added to git
from loggingperiodconfig import * #configuration information for how often to split the log file and how many readings to make per time

##########################################################

#setup sensors:
#sound-- sound sensor outputs an analog sigal that gets read by the analog to digital converter
soundsensor = Adafruit_ADS1x15.ADS1015()
GAIN = 1 #see datasheet for gain table, 1 = +/-4.096V
soundsensor.start_adc(0, gain=GAIN)

#light
lightsensor = smbus.SMBus(1)
lightsensor.write_byte_data(0x39, 0x00 | 0x80, 0x03)
lightsensor.write_byte_data(0x39, 0x01 | 0x80, 0x02)

#enviromental-- there are a huge number of enviromental configuration possiblites, see the bme680 datasheet
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

#get the serial number of the raspberry pi's cpu to uniquely id the raspberry pi.
try:
  f = open('/proc/cpuinfo','r')
  for line in f:
    if line[0:6]=='Serial':
      cpuserial = line[10:26]
      break
  f.close()
except:
  cpuserial = "ERROR000000000"

print cpuserial

##########################################################

#create and print the headers. headers are used below in the log file creation
headers = "time (central), date, cpu temperature C, temperature C, pressure kPa, %RH, voc ohm, visible light lux, infrared light lux, sound dBa, serial: " + cpuserial + "\n" 
print headers

##########################################################

#setup the folders in case this is a new script run or if things got deleted.
if os.path.exists("data/log.csv"):#if the log file exists open it, and note that the script restarted
  outputfile = open("data/log.csv","a")
  outputfile.write("system restarted\n")
else:#if the log file doesn't exist see if the folder is there. if the folder is there open a new file and write the headers
  if os.path.isdir("data"):
    outputfile = open("data/log.csv","a")
    outputfile.write(headers)
  else:#if the folder isnt there then make it and make a new log file and write the headers
    os.mkdir("data")
    outputfile = open("data/log.csv","a")
    outputfile.write(headers)

  if not os.path.isdir("data/upload"):#make sure the ftp uplaod folder is there. if it's not there create it
    os.mkdir("data/upload")

  if not os.path.isdir("data/uploaded"):#make sure the ftp uplaoded folder is there. if it's not there create it
    os.mkdir("data/uploaded")

##########################################################

timeperiodstart = time.time() #get the current time, so we know when we've waited long enough to split the log file
try: #keeps us from having ugly errors when we kill the process
  while True: #loop forever

    #sound
    rawsound = soundsensor.get_last_result() #get the most recent analog to digital conversion from the sensor
    sounddba = rawsound / 10.0 #given our sensors precision dividing by 10 gives us decibels


    #light
    lightraw = lightsensor.read_i2c_block_data(0x39, 0x0C | 0x80, 2) #read the light sensors
    lightraw1 = lightsensor.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
    fullspectrumlight = lightraw[1] * 256 + lightraw[0] #convert the number to lux
    infraredlight = lightraw1[1] * 256 + lightraw1[0]
    visiblelight = fullspectrumlight - infraredlight #get the visible light from the full spectrum light


    #envriomental
    enviromentalsensor.get_sensor_data() #get the sensor's data
    temperature = enviromentalsensor.data.temperature #rename to freindly vairables
    pressure = enviromentalsensor.data.pressure
    humidity = enviromentalsensor.data.humidity
    if enviromentalsensor.data.heat_stable: #for the first few moments of operation the VOC sensor doesn't give results. so return a zero if there's no data
      voc = enviromentalsensor.data.gas_resistance
    else:
      voc = 0

    #cpu temperature  -- we are curious if the CPU puts out enough heat to make the other sensors drift
    cputemperature = os.popen("vcgencmd measure_temp").readline() #get the cpu temp from the system
    cputemperature = cputemperature.replace("temp=","") #clean some extraneous text from the returned temperature info
    cputemperature = float(cputemperature.replace("'C",""))


##########################################################

    #format the output data. generate time & date plus all the sensors data seperated by commas
    data = datetime.now().strftime("%H:%M:%S.%f, %m/%d/%Y") + ", " + str(cputemperature) + ", " + str(temperature) + ", " + str(pressure) + ", " + str(humidity) + ", " + str(voc) + ", " + str(visiblelight) + ", " + str(infraredlight) + ", " + str(sounddba)
    print data

    outputfile.write(data + "\n") #write the current line of data to the log file

##########################################################

    if time.time() - timeperiodstart >= uploadperiod * 60: #if the log file split time has elapsed split the log otherwise wait
      filesplittingtiming = time.time() #we time the below operation in case it takes a long time we can remove some time from our logging period to get even logging periods

      outputfile.close() #close the current log file
      newfilename = str(datetime.now().strftime("log_%m-%d-%Y_%H-%M-%S.csv")) #generate the name for the new log -- date then time
      os.rename("data/log.csv", "data/upload/" + newfilename) #rename the log file and move it into the folder to be uploaded by ftp
      outputfile = open("data/log.csv","a") #create a new log file
      outputfile.write(headers) #add headers to the new log file
      print "\nOutput CSV Split: " + newfilename + " \n" #notifiy the user of the log file split

      timeperiodstart = time.time() #reset the clock on the log file split

      revisedloggingperiod = loggingperiod - time.time() - filesplittingtiming #figure out how much time the log splitting took
      if revisedloggingperiod < 0: #in case the log splitting took a _long_ time make sure we never wait negative time
          revisedloggingperiod = 0
      time.sleep(revisedloggingperiod) #sleep for the standard logging period minus the time it took to split the file
    else:
      time.sleep(loggingperiod) #if it's not time to split the file wait the normal amount of time

except KeyboardInterrupt:
  outputfile.close()


