#!/usr/bin/python

# THIS FILE IS MANAGED BY PUPPET - DO NOT MANUALLY EDIT

import sys
import socket
import time
import csv
import fileinput

def removeDuplicate ( filename ):
  presentInCsv = set() # set for fast O(1) amortized lookup
  for line in fileinput.FileInput( filename, inplace=1):
    if line in presentInCsv: continue # skip duplicate

    presentInCsv.add(line)
    print line, # standard output is now redirected to the file
  return;

if len(sys.argv) < 4:
    print "Syntax Error: " + sys.argv[0] + " [hostname] [port] [tcp or udp]"
    sys.exit(1)

host = sys.argv[1]
port = int(sys.argv[2])
# type => ["tcp" or "udp"]
type = sys.argv[3].lower()
csvfilename = '/var/local/porttestreport.csv'
csvfile = open(csvfilename, 'ab')
writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

while 1 :
  if type == "udp":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  else:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(5)
  try:
    if type == "udp":
      s.sendto("--TEST LINE--", (host, port))
      recv, svr = s.recvfrom(255)
      s.shutdown(2)
      print "Success connecting to " + host + " on UDP port: " + str(port)
      writer.writerow([host,str(port),"ENABLED"])
      csvfile.close()
      sys.exit(0)
    else:
      s.connect((host, port))
      s.shutdown(2)
      print "Success connecting to " + host + " on TCP port: " + str(port)
      writer.writerow([host,str(port),"ENABLED"])
      csvfile.close()
      sys.exit(0)
  except Exception, e:
    try:
      errno, errtxt = e
    except ValueError:
      print "Cannot connect to " + host + " on port: " + str(port)
      writer.writerow([host,str(port),"DISABLED"])
      csvfile.close()
      removeDuplicate(csvfilename)
      sys.exit(1)
    else:
      if errno == 107:
        print "Success connecting to " + host + " on UDP port: " + str(port)
        writer.writerow([host,str(port),"ENABLED"])
        csvfile.close()
        sys.exit(0)
      else:
        print "Cannot connect to " + host + " on port: " + str(port)
        writer.writerow([host,str(port),"DISABLED"])
        csvfile.close()
        removeDuplicate(csvfilename)
        sys.exit(1)

  s.close
  time.sleep(1)

