#!/usr/bin/python

""" 
  A simple direhose sink that generates a histogram of `last_modification` time
  of the inspected files of a walk. Essentially it provides insight when you're
  typically working on stuff.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2014-02-14
@status: init
"""
from __future__ import division
import sys
import socket
import datetime
import json
from collections import Counter

HIST_WIDTH = 80 # max. width of histogram in characters
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
    sys.stdout.write('.')
  
  print('\nData received, generating histogram ...')
  # now update the histogram
  for last_mod in file_last_mods:
    lm_hour = datetime.datetime.fromtimestamp(last_mod).hour
    cnt[lm_hour] += 1
  
  max_num =  cnt.most_common(1)[0][1]
  norm_factor = HIST_WIDTH / max_num
  for lm_hour, num_files in cnt.items():
    norm_num_files = num_files * norm_factor
    
    if norm_num_files < 1:
      norm_num_files = 1
    
    if lm_hour < 10:
      print(' %dh: ' %(lm_hour) + '*'*int(norm_num_files) + ' '*(HIST_WIDTH - int(norm_num_files)) + ' (%d)' %(num_files))
    else:
      print('%dh: ' %(lm_hour) + '*'*int(norm_num_files) + ' '*(HIST_WIDTH - int(norm_num_files)) + ' (%d)' %(num_files))

################################################################################
## main script

if __name__ == '__main__':
  dh_port = 7654
  try:
    dh_port = args[0]
  except:
    pass
  build_lmod_hist(int(dh_port))
