#!/usr/bin/python

""" 
  Traverses POSIX compliant filesystems and generates a data stream out
  of the discovered file and directory information.

@author: Michael Hausenblas, http://mhausenblas.info/#i
@since: 2014-02-11
@status: init
"""
import sys
import os
import socket
import logging
import string
import datetime
import json

################################################################################
## config

DEBUG = False

# defines host and port to stream the data out via UDP
STREAM_HOST = 127.0.0.1
STREAM_PORT = 6900

# defines the interval in sec where progress will be reported to stdout
REPORTING_INTERVAL = 10 

out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP

if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT)


################################################################################
## API

def _fs_create_package():
  fs_package = {
    'timestamp' : str(datetime.datetime.now().isoformat()),
    'name' : 'TBD',
    'size' : 'TBD'
  }    
  logging.debug('FS package created: %s' %fs_package)
  return (fs_package, sys.getsizeof(str(fs_package)))

def _send_package(out_socket, package):
    out_socket.sendto(str(package) + '\n', (STREAM_HOST, STREAM_PORT))

def walk():
  start_time = datetime.datetime.now()
  num_packages = 0
  bytes_packages = 0

  while True:    
    (package, package_size) = _fs_create_package()
    _send_fintran(out_socket, json.dumps(package))
    num_packages += 1
    bytes_packages += package_size
    end_time = datetime.datetime.now()
    diff_time = end_time - start_time

    if diff_time.seconds > REPORTING_INTERVAL):
      tp_bytes = bytes_packages/1024/1024
      logging.info('%s\t%d\t%0.3f'
        %(
          str(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')),
          num_packages, 
          bytes_packages/1024/1024
        )
      )
      start_time = datetime.datetime.now()
      num_packages = 0
      bytes_packages = 0

################################################################################
## main script

if __name__ == '__main__':
  walk()