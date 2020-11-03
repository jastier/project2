#!/usr/bin/env python

import argparse
import os

parser = argparse.ArgumentParser()

# Destination, this can be a hostname or an IPV4/IPV6 Internet address
parser.add_argument(
    '-d', type=str, required=True, 
    help='Destination name or IP address'
)

# Port to be forwarded
parser.add_argument(
    '-p', type=int, required=True, help='Port number to forward'
)

# Start forwarding this port
parser.add_argument(
    '--start', action='store_true', help='Start forwarding this port'
)

# Stop forwarding this port
parser.add_argument(
    '--stop', action='store_true', help='Stop forwarding this port'
)

# Query the status of this port
parser.add_argument(
    '--status', action='store_true', help='Query the port status'
)

args = parser.parse_args()

# Forward the port
if(args.start):

    preamble = 'ssh -o ConnectTimeout=7 -NfL '
  
    try:
        port = str(args.p)
        cmd = preamble + port + ':localhost:' + port + ' ' + args.d
        print('Executing command')
        print(cmd)
        os.system(cmd)
        

    except NameError:
        print('NameError exception')

    except: 
        print('some other exception')

# Query the status of the port
if(args.status):
    print('Status')
  


# Unbind the port...maybe
if(args.stop):
     print('Stop')

