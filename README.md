# pi-environmental-data-log

Log temperature, pressure, relative humidity, total VOC, infrared & visible light, and loudness.
Then upload that information and upload to a FTP server. 



When setting up initally duplicate ftpconfig-blank.py and rename it ftpconfig.py and fill in your information.



You'll need to add a couple of lines to /etc/rc.local, something like:
cd /home/pi/Desktop/pi-environmental-data-log/
lxterminal -e python ftp-upload-data.py 
lxterminal -e python all-sensors-get-data.py




You'll need to isntall these libraries
TSL2561:
  Visible & IR Light Sensor:
    https://github.com/ControlEverythingCommunity/TSL2561.git
    
    using the sample python


BME680:
  Temperature, Humidity, Pressure, VOC:
    https://github.com/pimoroni/bme680

    using the sample python

ADS1015:
  Analog to Digital Data Converter
    https://github.com/adafruit/Adafruit_Python_ADS1X15

    using the sample python

Gravity Sound Level Meter v1.0
  Decibel meter that outputs voltage

    interfacing using ADS1015 used notes from the dfrobotics website

