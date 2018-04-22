# Distributed with a free-will license.
# Use it any way you want, profit or free, provided it fits in the licenses of its associated works.
# TSL2561
# This code is designed to work with the TSL2561_I2CS I2C Mini Module available from ControlEverything.com.
# https://www.controleverything.com/content/Light?sku=TSL2561_I2CS#tabs-0-product_tabset-2

#changed the script into a function that returns the visible, infrared, and full spectrum data


import smbus
import time


def getlightdata():

  bus = smbus.SMBus(1)
  bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
  bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

  time.sleep(0.5)

  data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
  data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)

  ch0 = data[1] * 256 + data[0]
  ch1 = data1[1] * 256 + data1[0]
 
  #visible, infrared
  return ch0-ch1, ch1