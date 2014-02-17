#!/usr/bin/python

""" 
  A simple direhose sink that generates a summary of the types of the
  inspected files of a walk based on the file extension.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2014-02-17
@status: init
"""
from __future__ import division
import sys
import os
import socket
import datetime
import json
from collections import Counter

RCV_BUFFER_SIZE = 4096 # UDP socket receive buffer size set to 4kB
END_OF_STREAM_MSG = 'EOS'


def build_filetype_summary(dh_port):
  in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
  in_socket.bind(('localhost', dh_port))
  cnt = Counter()
  total_file_num = 0
  unknown_count = 0
  file_types = []

  print('Listening for incoming data on port %d' %dh_port)  
  # receive the data and build up the list of file types
  while True: 
    data, addr = in_socket.recvfrom(RCV_BUFFER_SIZE)
    if data == END_OF_STREAM_MSG: 
      break
    package = json.loads(data)
    file_ext = os.path.splitext(package['name'])[1]
    if file_ext != '':
      file_types.append(file_ext)
    else:
      unknown_count += 1
    total_file_num += 1
    sys.stdout.write('.')
    
  print('\nData received, generating file types summary ...')
  for file_type in file_types:
    cnt[file_type] += 1
 
  print('Of the overall %d files and directories inspected:' %(total_file_num))
  print(' %0.3f%% (%d) are of unknown type.' %((unknown_count/total_file_num)*100, unknown_count))

  for file_type, num_files in cnt.most_common():
    rel_occurance = (num_files/total_file_num)*100
    print(' %0.3f%% (%d) are of type %s' %(rel_occurance, num_files, file_type))
  

################################################################################
## main script

if __name__ == '__main__':
  dh_port = 7654
  try:
    dh_port = args[0]
  except:
    pass
  build_filetype_summary(int(dh_port))
