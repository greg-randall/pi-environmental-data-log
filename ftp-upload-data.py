#import time
from datetime import datetime
import os
from ftplib import FTP
from ftpconfig import * #credentials for ftp. done this way to keep them from getting added to git

while True: #loop forever
  filestoupload = os.listdir('data/upload') #get a list of the files you need to upload
  if len(filestoupload)>0: #check if there are files to upload
    print "Found " + str(len(filestoupload)) + " file(s) to upload: " #list the file count to upload
    try: #make sure the ftp stuff actually works, if it doesn't we'll throw an error message
      #initate ftp connection using the the information in the ftp config file
      ftp = FTP()
      ftp.connect(SERVER, PORT)
      ftp.login(USER, PASS)

      #get list of files on the ftp server to see if the folder we need to upload to exisits
      filelist = []
      ftp.retrlines('LIST', filelist.append)
      found = False
      for f in filelist: #look through file list to find if the folder is there
        filename = f.split()[-1]
        if filename == 'pi-env-data': #if we find the folder change directories and break the loop
          found = True
          ftp.cwd('pi-env-data')
          break
      if not found: #if we didn't find the folder create the folder and then go into that directory
        ftp.mkd('pi-env-data')
        ftp.cwd('pi-env-data')

      for f in filestoupload: #loop through the files we need to upload
        print f + "\n" #list the file we're currently uploading
        ftp.storbinary('STOR ' + f, open("data/upload/" + f)) #upload the file
        os.rename("data/upload/" + f,"data/uploaded/" + f) #move the file we just uploaded into the uploaded directory
      ftp.close() #after all of the uploads close the ftp connection
    except:
      print "Could not access " + SERVER + ". Will retry shortly." #if we can't get to the server then list that it failed

  print "Waiting 30 seconds. Current time: " + datetime.now().strftime("%H:%M:%S.%f") #wait statment before checking for new files to upload, time is there to help debugging
  time.sleep(30) #wait until we check the folders again
