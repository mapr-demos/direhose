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

RCV_BUFFER_SIZE = 4096 # UDP socket receive buffer size set to 4kB

def build_lmod_hist(dh_port):
  in_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP
  in_socket.bind(('localhost', dh_port))
  while True:
    data, addr = sock.recvfrom(RCV_BUFFER_SIZE)


################################################################################
## main script

if __name__ == '__main__':
  dh_port = 7654
  try:
    dh_port = args[0]
  except:
    pass
  build_lmod_hist(int(dh_port))
