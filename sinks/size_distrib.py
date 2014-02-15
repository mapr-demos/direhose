#!/usr/bin/python

""" 
  A simple direhose sink that generates a distribution of the `size` of the 
  inspected files of a walk. 

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

RCV_BUFFER_SIZE = 4096 # UDP socket receive buffer size set to 4kB
END_OF_STREAM_MSG = 'EOS'


def median(lst):
  lstlen = len(lst)
  if not lstlen%2:
    return (lst[(int(lstlen/2))-1]+lst[int(lstlen/2)])/2.0
  return lst[int(lstlen/2)]

def pretty_print_fsize(label, fsize):
  if fsize < 1024:
    print('%s: %d Bytes' %(label, fsize))
  else:
    print('%s: %0.1f kB' %(label, fsize/1024))

def build_size_dist(dh_port):
  in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
  in_socket.bind(('localhost', dh_port))
  file_sizes = []
  overall_fsize = 0
  file_cat = {
    'small' : 0,  # size < 10kB
    'medium' : 0, # 10kB < size < 10MB (= 10*1024*1024)
    'large' : 0, # size > 10MB
  }

  print('Listening for incoming data on port %d' %dh_port)  
  # receive the data and build up the lsit of last modifications of files  
  while True: 
    data, addr = in_socket.recvfrom(RCV_BUFFER_SIZE)
    if data == END_OF_STREAM_MSG: 
      break
    package = json.loads(data) 
    file_sizes.append(package['size'])
    sys.stdout.write('.')
  
  print('\nData received, generating distribution ...')
  print('Total number of files/directories: %d' %(len(file_sizes)))
  for fsize in file_sizes:
    overall_fsize += fsize
    if fsize < (10*1024):
      file_cat['small'] += 1
    elif fsize < (10*1024*1024):
      file_cat['medium'] += 1
    else:
      file_cat['large'] += 1

  smallest = min(file_sizes)    
  largest = max(file_sizes)
  median_size = median(file_sizes)
  avg_size = overall_fsize / len(file_sizes)
  pretty_print_fsize('Total size of files/directoriesllest', overall_fsize)
  pretty_print_fsize('Smallest', smallest)
  pretty_print_fsize('Largest', largest)
  pretty_print_fsize('Median', median_size)
  pretty_print_fsize('Average', avg_size)  
  print('Distribution:')
  print(' %d small files (less than 10kB)' %(file_cat['small']))
  print(' %d medium files (between 10kB and 10MB)' %(file_cat['medium']))
  print(' %d large files (more than 10MB)' %(file_cat['large']))
  
  
################################################################################
## main script

if __name__ == '__main__':
  dh_port = 7654
  try:
    dh_port = args[0]
  except:
    pass
  build_size_dist(int(dh_port))
