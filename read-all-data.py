import tsl2561read
import bme680read
import ads1015read

import time
import os.path

#logging period in seconds:
loggingperiod = 2


headers = "time & date, temperature F, pressure inHg, %RH, visible light lux, infrared light lux, sound\n"

if os.path.exists("log.csv"):
  outputfile = open("log.csv","a")
else:
  outputfile = open("log.csv","a")
  outputfile.write(headers)

print headers

try:
  while True:
    data = time.strftime("%X %x,", time.gmtime()) + " " + ", ".join(map(str,bme680read.getenviromentaldata() + tsl2561read.getlightdata())) + ", " + str(ads1015read.getsounddata())
    print data

    data = data + "\n"
    outputfile.write(data)

    time.sleep(loggingperiod)
 
except KeyboardInterrupt:
  pass