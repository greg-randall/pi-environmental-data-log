# pi-environmental-data-log

Log temperature (ambient & cpu), pressure, relative humidity, total VOC, infrared & visible light, and loudness.
Then upload that information and upload to a FTP server. 


Initial Setup:
	When setting up initally duplicate ftpconfig-blank.py and rename it ftpconfig.py and fill in your information.
	You may want to adjust the logging period and log split period in loggingperiodconfig.py .
	
	
	You'll need to add a couple of lines to /etc/rc.local, something like:
	cd /home/pi/Desktop/pi-environmental-data-log/
	lxterminal -e python ftp-upload-data.py 
	lxterminal -e python all-sensors-get-data.py
	



You'll need to isntall these libraries
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
	
	    interfacing using ADS1015 used notes from the dfrobotics website
	
