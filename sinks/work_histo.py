#!/usr/bin/python

""" 
  A simple direhose sink that generates a histogram of `last_modification` time
  of the inspected files of a walk. Essentially it provides insight when you're
  typically working on stuff.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2014-02-14
@status: init
"""
import sys
import socket
import datetime
import json
from collections import Counter

RCV_BUFFER_SIZE = 4096 # UDP socket receive buffer size set to 4kB
END_OF_STREAM_MSG = 'EOS'

def build_lmod_hist(dh_port):
  in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
  in_socket.bind(('localhost', dh_port))
  cnt = Counter()
  file_last_mods = []

  print('Listening for incoming data on port %d' %dh_port)  
  # receive the data and build up the lsit of last modifications of files  
  while True: 
    data, addr = in_socket.recvfrom(RCV_BUFFER_SIZE)
    if data == END_OF_STREAM_MSG: 
      break
    package = json.loads(data) 
    file_last_mods.append(package['last_modification'])
  
  print('Data received, generating histogram')
  # now update the histogram
  for last_mod in file_last_mods:
    cnt[last_mod] += 1
    
  for lm, num_files in cnt.items():
    lm_hour = datetime.datetime.fromtimestamp(lm).hour
    print('hour: %d - number of files: %d ' %(lm_hour, num_files))

################################################################################
## main script

if __name__ == '__main__':
  dh_port = 7654
  try:
    dh_port = args[0]
  except:
    pass
  build_lmod_hist(int(dh_port))
