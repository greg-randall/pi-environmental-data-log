import tsl2561read
import bme680read
import time


print "temperature F, pressure inch inHg, %RH, visible light lux, infrared light lux"

outputfile = open("log.csv","w")

try:
  while True:
    data = time.strftime("%x %X,", time.gmtime()) + " " + ", ".join(map(str,bme680read.getenviromentaldata() + tsl2561read.getlightdata()))
    print data

    data = data + "\n"
    outputfile.write(data)

    time.sleep(2)
 
except KeyboardInterrupt:
  pass