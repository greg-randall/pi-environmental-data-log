#!/usr/bin/env python
import bme680
import time


def getenviromentaldata(): 
  sensor = bme680.BME680()

  sensor.set_humidity_oversample(bme680.OS_2X)
  sensor.set_pressure_oversample(bme680.OS_4X)
  sensor.set_temperature_oversample(bme680.OS_8X)
  sensor.set_filter(bme680.FILTER_SIZE_3)

  temperature = round((sensor.data.temperature * 1.8) + 32,2)
  pressure = round(sensor.data.pressure * 0.02953,4)
 
  # temperature C, pressure hPa, %RH
  return temperature, pressure, sensor.data.humidity