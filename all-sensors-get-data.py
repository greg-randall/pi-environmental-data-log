#sensor libs:
import smbus
import bme680
import Adafruit_ADS1x15

import time
import os.path

##########################################################

#logging period in seconds:
loggingperiod = 1

##########################################################

#setup sensors:
#sound 
soundsensor = Adafruit_ADS1x15.ADS1015()
GAIN = 1
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

headers = "time (central), date, temperature F, pressure inHg, %RH, voc ohm, visible light lux, infrared light lux, sound dBa\n"

if os.path.exists("log.csv"):
  outputfile = open("log.csv","a")
else:
  outputfile = open("log.csv","a")
  outputfile.write(headers)

outputfile.write("system restarted\n")

print headers

##########################################################

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
    rawtemperature = enviromentalsensor.data.temperature
    rawpressure = enviromentalsensor.data.pressure
    humidity = enviromentalsensor.data.humidity
    temperature =  round((rawtemperature * 1.8) + 32,2)
    pressure = round(rawpressure * 0.02953,4)
    if enviromentalsensor.data.heat_stable:
      voc = enviromentalsensor.data.gas_resistance
    else:
      voc = 0

##########################################################	

    data = time.strftime("%X, %x", time.localtime()) + ", " + str(temperature) + ", " + str(pressure) + ", " + str(humidity) + ", " + str(voc) + ", " + str(visiblelight) + ", " + str(infraredlight) + ", " + str(sounddba)
    print data

    outputfile.write(data + "\n")

    time.sleep(loggingperiod)
 
except KeyboardInterrupt:
  pass

outputfile.close()
