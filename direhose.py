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
import getopt

################################################################################
## config

DEBUG = False

# defines host and port to stream the data out via UDP
STREAM_HOST = '127.0.0.1'
STREAM_PORT = 7654

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

def walk(start_dir):
  for root, dirs, files in os.walk(start_dir):
    print('%s' %root)
    for f in files:
      print(' %s' %f)
      # (package, package_size) = _fs_create_package()
      # _send_fintran(out_socket, json.dumps(package))

def usage():
  print('Usage: python direhose.py [start directory]\n')


################################################################################
## main script

if __name__ == '__main__':
  start_dir = '.'  
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    
    for opt, arg in opts:
      if opt in ('-h', '--help'):
        usage()
        sys.exit()
    try:
      start_dir = args[0]
    except:
      pass
  
    walk(start_dir)
  except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)