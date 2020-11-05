#!/usr/bin/env python
#
# Author: Joseph Astier
# Date: 2020 October 
#
# Single Port Forwarder.  This script will manage forwarding one 
# port from this machine to a destination machine, by starting an ssh
# process that will maintain the port forwarding in the background.
# The command used to start the forwarding is later used to check for a
# running process.
#
# Required arguments:
#
# -d       Destination, either a hostname or IPV4/IPV6 address
#
# -p       Port to be forwarded to the destination machine
#
#
# actions (choose one):
#
# start    Begin forwarding the port by starting a background ssh process
#
# stop     Stop the port by killing the ssh process.  
#
# status   Report whether the port is currently in use.
#

import argparse
import os
import subprocess

parser = argparse.ArgumentParser()

# add args
parser.add_argument(
    '-d', type=str, required=True, 
    help='Host, either a hostname or IP address'
)
parser.add_argument(
    '-p', type=int, required=True, help='Port number to forward'
)

# add actions
START = 'start'    # Start forwarding this port
STOP = 'stop'      # Stop forwarding this port
STATUS = 'status'  # Return the port status
parser.add_argument('action', choices=(START, STOP, STATUS))


# Compose an ssh command that will start forward the port to the host
args = parser.parse_args()
port = str(args.p)
host = args.d
ssh_cmd = 'ssh -o ConnectTimeout=7 -NfL ' + port + ':localhost:' + port + ' ' + host


# Find the pid(s) for any processes running our ssh command.  If any exist,
# the port has already been forwarded.
pids = []
pid_cmd = 'ps -C ssh'
for line in os.popen(pid_cmd).read().splitlines():
    tokens = line.split()
    if(len(tokens) > 0):
        token = tokens[0]
        if(token.isdigit()):
            args_cmd = 'ps -p ' + token + ' -o args='
            args_output = os.popen(args_cmd).read().rstrip('\n')
            if(ssh_cmd == args_output):
                pids.append(token)


# Forward the port by starting a process with the ssh command
if(args.action == START):
    print('Forwarding ' + port + ' to ' + host + '...')
    if(len(pids) == 0):
        try:
            os.system(ssh_cmd)
            print('Port '+port+' is now forwarded to '+host)
        except: 
            print('Could not forward port ' + port + ' to ' + host)
    else:
        for pid in pids:
            print('Port '+port+' was already forwarded to '+host+' ['+pid+']')
  

# Stop forwarding the port(s) by killing their pids
elif(args.action == STOP):
    print('Unforwarding ' + port + ' from ' + host + '...')
    for pid in pids:
        cmd = 'kill ' + str(pid)
        try:
            os.system(cmd)
            print('Port '+port+' is no longer forwarded to '+host +' ['+pid+']')
        except: 
            print('Could not unforward port ' + port + ' from ' + host)
    if(len(pids) == 0):
        print('Port '+port+' was not forwarded to '+host)


# Query the status of the port by testing if it already has an ssh process
else:  # STATUS
    for pid in pids:
        print('Port '+port+' is forwarded to '+host+' ['+pid+']')
    if(len(pids) == 0):
        print('Port ' + port + ' is not forwarded to ' + host)
        
