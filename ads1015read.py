# Simple demo of continuous ADC conversion mode for channel 0 of the ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain

import time
import Adafruit_ADS1x15

def getsounddata():
  adc = Adafruit_ADS1x15.ADS1015()
  GAIN = 1
  value = adc.get_last_result()

  return value
