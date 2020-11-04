#!/usr/bin/env python
#
# Author: Joseph Astier
# Date: 2020 October 
#
# Single action port forwarder.  This script will manage forwarding
# one port from this machine to a destination machine, by starting an
# ssh process that will maintain the port forwarding in the background.
#
# Required arguments:
#
# -d         Destination, either a hostname or IPV4/IPV6 address
#
# -p         Port to be forwarded to the destination machine
#
#
# Optional actions (user chooses only 1, any others are ignred):
#
# --start    Begin forwarding the port by starting a background ssh process
#
# --stop     Stop the port by killing the ssh process.  
#
# --status   Report whether the port is currently in use.
#

import argparse
import os

parser = argparse.ArgumentParser()

# add args
parser.add_argument(
    '-d', type=str, required=True, 
    help='Destination hostname or IP address'
)
parser.add_argument(
    '-p', type=int, required=True, help='Port number to forward'
)

# add actions
parser.add_argument(
    '--start', action='store_true', help='Start forwarding this port'
)
parser.add_argument(
    '--stop', action='store_true', help='Stop forwarding this port'
)
parser.add_argument(
    '--status', action='store_true', help='Query the port status'
)

args = parser.parse_args()
print(args)


# Forward the port using ssh to manage it in the background
if(args.start):

    p = str(args.p)
    cmd = 'ssh -o ConnectTimeout=7 -NfL ' + p + ':localhost:' + p + ' '+args.d
  
    try:
        print('Executing command')
        print(cmd)
        os.system(cmd)
        

    except NameError:
        print('NameError exception')

    except: 
        print('some other exception')
  
# Stop forwarding the port by killing the ssh process managing this 
# port, if one exists.  
else if(args.stop):
     print('Stop')

# Query the status of the port by checking if there is an ssh process
# with destination and port number already running.  
# TODO:  Detect if a port has been bound by any process, not just ours.
else if(args.status):
    print('Status')


