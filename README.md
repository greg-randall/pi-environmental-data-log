# pi-environmental-data-log

Log temperature (ambient & cpu), pressure, relative humidity, total VOC, infrared & visible light, and loudness. Then upload that information to a FTP server.

---

Initial Setup:
When setting up initially duplicate ftpconfig-blank.py and rename it ftpconfig.py and fill in your information. You may want to adjust the time between data points (loggingperiod) and log split period (uploadperiod) in loggingperiodconfig.py .

You'll need to add a couple of lines to /etc/rc.local, to make the logging system work when the computer boots.

```
cd /home/pi/Desktop/pi-environmental-data-log/
screen -d python ftp-upload-data.py
screen -d python all-sensors-get-data.py
```

You'll need to install libraries for these sensors

Sensor | Purpose | Library
--|--|--
TSL2561 | Visible & IR Light Sensor | https://github.com/ControlEverythingCommunity/TSL2561.git
BME680 | Temperature, Humidity, Pressure, VOC | https://github.com/pimoroni/bme680
ADS1015 | Analog to Digital Data Converter | https://github.com/adafruit/Adafruit_Python_ADS1X15
Gravity Sound Level Meter | Decibel meter that outputs voltage uses ADS1015 | https://www.robotshop.com/en/gravity-analog-sound-level-meter.html

---

**Making one big CSV**

For analysis of your data you'll probably need to combine all your split files into a single CSV. For Linux/Mac here's how it do it (if you're on Windows install Cygwin before you follow these directions):

1. Cd to the folder where you've put your CSV files. 
2. Combine all your files into a single file: cat *.csv > all.csv 
3. Remove all the CSV headers that will be sprinkled throughout the file: grep -i -v 'serial' all-files.csv > all-files-no-headers.csv
4. Discover if the system lost power during your data collection: grep -i -B2 -A2 'restart' all-files-no-headers.csv
5. If there are reboots look the line preceding "system restarted" and see if the data is complete. Typically during a power loss there will only be a partial line of data, if the system shut down gracefully you should get a complete line of data. Most people will want to delete partial lines of data: sed -n '/system restarted/{n;x;d;};x;1d;p;${x;p;}' all-files-no-headers.csv  > all-files-no-headers-reboot-cleaned.csv  (see https://stackoverflow.com/a/7378865/4896819 for more information on this sed command)
6. If you need the header back at the top of your combined csv file take one of your source log files and run the following command on it: sed -n '1p;' log_05-24-2018_16-54-55.csv | cat - all-files-no-headers-reboot-cleaned.csv > final-combined-cleaned.csv

---

**General Parts**

Cost | Item | Source | Link
--|--|--|--
$10.00 | Raspberry Pi Zero W | Adafruit | https://www.adafruit.com/product/3400
$8.49 | SanDisk 16 GB Micro SDHC | Amazon | http://a.co/7qehPkj
$5.00 | USB Wall Charger of at least 1.2A | Amazon | Pick a good/cheap one, $5 is a guess
$5.00 | USB A to Micro B | Amazon | http://a.co/i85njBl
$10.00 | Good Quality Enclosure | Amazon | Pick a good/cheap one, $10 is a guess


**Sensors**

Cost | Item | Source | Link
--|--|--|--
$2.46 | DS3231 Real Time Clock Module 3.3V/5V with battery | Amazon | http://a.co/i9cgYlo
$22.50 | BME680 Breakout - Air Quality, Temperature, Pressure, Humidity Sensor | Adafruit | https://www.adafruit.com/product/3660
$5.95 | TSL2561 Digital Luminosity/Lux/Light Sensor Breakout | Adafruit | https://www.adafruit.com/product/439
$39.50 | Gravity Analog Sound Level Meter | Robotshop | https://www.robotshop.com/en/gravity-analog-sound-level-meter.html
$9.95 | ADS1015 12-Bit ADC - 4 Channel with Programmable Gain | Adafruit | https://www.adafruit.com/product/1083
