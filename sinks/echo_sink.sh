#!/bin/bash -

################################################################################
# 
# This is the simplest direhose sink one could think of: using netcat
# (see also 'man nc'), the script listens on the port provided (defaults to
# 7654 if none is supplied) to incoming UDP packages, echos them on stdout and
# also writes them to a file 'direhose_packages.log' in the same dir.
# Launch this script first and then launch the direhose script using
# source_type=network, and optionally a network_port=PORT_NUMBER, in the
# direhose config file.
# 
# Usage: ./echo_sink.sh [PORT_NUMBER]
#
#

if [[ -z "$1" ]]; then
  DIREHOSE_PORT=7654
else
  DIREHOSE_PORT=$1
fi

echo "Listening on port "$DIREHOSE_PORT" for packages from direhose ..."
nc -v -u -l $DIREHOSE_PORT | tee direhose_packages.log