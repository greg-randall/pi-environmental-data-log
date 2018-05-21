# pi-environmental-data-log

Log temperature (ambient & cpu), pressure, relative humidity, total VOC, infrared & visible light, and loudness.
Then upload that information to a FTP server.


Initial Setup:
  When setting up initially duplicate ftpconfig-blank.py and rename it ftpconfig.py and fill in your information.
  You may want to adjust the time between data points (loggingperiod) and log split period (uploadperiod) in loggingperiodconfig.py .


  You'll need to add a couple of lines to /etc/rc.local, to make the logging system work when the computer boots.
  cd /home/pi/Desktop/pi-environmental-data-log/
  screen -d python ftp-upload-data.py
  screen -d python all-sensors-get-data.py




You'll need to install these libraries
  TSL2561:
    Visible & IR Light Sensor:
      https://github.com/ControlEverythingCommunity/TSL2561.git


  BME680:
    Temperature, Humidity, Pressure, VOC:
      https://github.com/pimoroni/bme680


  ADS1015:
    Analog to Digital Data Converter
      https://github.com/adafruit/Adafruit_Python_ADS1X15


  Gravity Sound Level Meter v1.0
    Decibel meter that outputs voltage
      Use the above ADS1015 and notes from the dfrobotics website


**General Parts**
| Cost | Item | Source | Link |
|--|--|--|--|
| $10.00 | Raspberry Pi Zero W | Adafruit | https://www.adafruit.com/product/3400 |
| $8.49 | SanDisk 16 GB Micro SDHC | Amazon | http://a.co/7qehPkj |
| $5.00 | USB Wall Charger of at least 1.2A | Amazon | Pick a good/cheap one, $5 is a guess. |
| $5.00 | USB A to Micro B | Amazon | http://a.co/i85njBl |
| $10.00 | Good Quality Enclosure | Amazon | Pick a good/cheap one, $10 is a guess. |


**Sensors**
| Cost | Item | Source | Link |
|--|--|--|--|
| $2.46 | DS3231 Real Time Clock Module 3.3V/5V with battery | Amazon | http://a.co/i9cgYlo |
| $22.50 | BME680 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor | Adafruit | https://www.adafruit.com/product/3660 |
| $5.95 | TSL2561 Digital Luminosity/Lux/Light Sensor Breakout | Adafruit | https://www.adafruit.com/product/439 |
| $39.50 | Gravity Analog Sound Level Meter | Robotshop | https://www.robotshop.com/en/gravity-analog-sound-level-meter.html |
| $9.95 | ADS1015 12-Bit ADC - 4 Channel with Programmable Gain | Adafruit | https://www.adafruit.com/product/1083
