#!/bin/bash -

################################################################################
# 
# This is the simplest direhose sink one could think of: using netcat
# (see also 'man nc'), this script listens on the default port 7654 for
# incoming UDP packages, echos them on stdout and also writes them to 
# into a file 'direhose_packages.log' in the same dir. Launch this script
# first and then launch the direhose script using source_type=network in the
# config file.
# 
# Usage: ./echo_sink.sh
#
#
nc -v -u -l 7654 | tee direhose_packages.log