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

# name of the config file, read on start-up and overwriting defaults
DEFAULT_CONFIG_FILE = './direhose.conf'

# default starting directory for the walk
DEFAULT_START_DIR = '.'

# default source type (send to stdout)
DEFAULT_SOURCE_TYPE = 'local'

# default source mode (send metadata only)
DEFAULT_SOURCE_MODE = 'metadata'

# defaults for host and port to stream the data out via network
DEFAULT_STREAM_HOST = '127.0.0.1'
DEFAULT_STREAM_PORT = 7654

direhose_config = {
  'start_dir' : DEFAULT_START_DIR,
  'source_type' : DEFAULT_SOURCE_TYPE,
  'source_mode' : DEFAULT_SOURCE_MODE,
  'network_host' : DEFAULT_STREAM_HOST,
  'network_port' : DEFAULT_STREAM_PORT
}

out_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # use UDP

if DEBUG:
  FORMAT = '%(asctime)-0s %(levelname)s %(message)s [at line %(lineno)d]'
  logging.basicConfig(level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%dT%I:%M:%S')
else:
  FORMAT = '%(message)s'
  logging.basicConfig(level=logging.INFO, format=FORMAT)


################################################################################
## API

def _create_package(f):
  package = {
    'package_ts' : str(datetime.datetime.now().isoformat()),
    'name' : '-',
    'size' : '-',
    'last_modification' : '-'
  }    
  try:
    package['name'] = os.path.abspath(f)
    package['size'] = os.path.getsize(f)
    package['last_modification'] = os.path.getmtime(f)
  except:
    pass
  logging.debug('Package created: %s' %package)
  return package

def _send_meta(package):
  f = package['name']
  logging.debug('Preparing to send metadata of %s ...' %f)
  try:
    if direhose_config['source_type'] == 'local':
      print(json.dumps(package))
      logging.debug('Metadata sent to stdout.')
    else:
      out_socket.sendto(
        str(json.dumps(package)) + '\n',
        (direhose_config['network_host'], int(direhose_config['network_port']))
      )
      logging.debug('Metadata sent to %s:%s' %(direhose_config['network_host'], direhose_config['network_port']))      
  except Exception, e:
    logging.error('%s' %e)
    
def _send_data(package):
  f = package['name']
  logging.debug('Preparing to send content of %s ...' %f)
  try:
    if direhose_config['source_type'] == 'local':
      print('xxx')
      logging.debug('Metadata sent to stdout.')
    else:
      out_socket.sendto(
        'xxx' + '\n',
        (direhose_config['network_host'], int(direhose_config['network_port']))
      )
      logging.debug('Metadata sent to %s:%s' %(direhose_config['network_host'], direhose_config['network_port']))      
  except Exception, e:
    logging.error('%s' %e)

def _send_package(package):
  if direhose_config['source_mode'] == 'metadata':
    _send_meta(package)
  elif direhose_config['source_mode'] == 'data':
    _send_data(package)
  elif direhose_config['source_mode'] == 'all':
    _send_meta(package)
    _send_data(package)
  else:
    pass
    
def walk():
  start_dir = direhose_config['start_dir']
  for root, dirs, files in os.walk(start_dir):
    _send_package(_create_package(root))
    for f in files:
      _send_package(_create_package(os.path.join(root, f)))

def apply_config(config_file): 
  cf = os.path.abspath(config_file)
  if os.path.exists(cf):
    logging.debug('Using config file %s, parsing settings ...' %cf)
    lines = tuple(open(cf, 'r'))
    for line in lines:
      l = str(line).strip()
      if l and not l.startswith('#'): # non-empty or non-comment line
        (setting_key, setting_value) = l.split('=')
        direhose_config[setting_key] = setting_value
        logging.debug('For %s using %s' %(setting_key, direhose_config[setting_key]))
  else:
    logging.debug('No config file found, using defaults')

def usage():
  print('Usage: python direhose.py [configuration file]\n')
  print('Note that the "configuration file" parameter is optional.')
  print('If none is provided, I will use %s' %DEFAULT_CONFIG_FILE)


################################################################################
## main script

if __name__ == '__main__':
  config_file = DEFAULT_CONFIG_FILE 
  try:
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    for opt, arg in opts:
      if opt in ('-h', '--help'):
        usage()
        sys.exit()
    try:
      config_file = args[0]
    except:
      pass
    apply_config(config_file)
    walk()
  except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)