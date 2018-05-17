import time
from datetime import datetime
import os
from ftplib import FTP
from ftpconfig import * #credentials for ftp. done this way to keep them from getting added to git

while True:
  filestoupload = os.listdir('data/upload')
  if len(filestoupload)>0:
    print "Found " + str(len(filestoupload)) + " file(s) to upload: "
    try:
      ftp = FTP()
      ftp.connect(SERVER, PORT)
      ftp.login(USER, PASS)

 
      filelist = []
      ftp.retrlines('LIST', filelist.append)

      found = False
      for f in filelist:
        filename = f.split()[-1]
        if filename == 'pi-env-data':
          found = True
          ftp.cwd('pi-env-data')
          break
      if not found:
        ftp.mkd('pi-env-data')
        ftp.cwd('pi-env-data')
    
      for f in filestoupload:
        print f + "\n" 
        ftp.storbinary('STOR ' + f, open("data/upload/" + f))
        os.rename("data/upload/" + f,"data/uploaded/" + f)
      ftp.close()
    except:
      print SERVER + " not available. Will retry shortly."
  
  print "Waiting 30 seconds. Current time: " + datetime.now().strftime("%H:%M:%S.%f")
  time.sleep(30)
