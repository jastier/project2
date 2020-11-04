#!/usr/bin/env python
#
# Author: Joseph Astier
# Date: 2020 October 
#
# Single-action port forwarder.  This script will manage forwarding
# one port from this machine to a destination machine, by starting an
# ssh process that will maintain the port forwarding in the background.
# The command used to start the forwarding is later used to check for a
# running process, or to stop it.
#
# Required arguments:
#
# -d         Destination, either a hostname or IPV4/IPV6 address
#
# -p         Port to be forwarded to the destination machine
#
#
# Optional actions (pick one):
#
# --start    Begin forwarding the port by starting a background ssh process
#
# --stop     Stop the port by killing the ssh process.  
#
# --status   Report whether the port is currently in use.
#

import argparse
import os
import subprocess

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


# Compose the ssh command from args
args = parser.parse_args()
port = str(args.p)
host = args.d
ssh_cmd = 'ssh -o ConnectTimeout=7 -NfL ' + port + ':localhost:' + port + ' ' + host


# Find the pid(s) for this command, there may be n >= 0 of these 
ps_cmd = 'ps -C \'' + ssh_cmd + '\' -o pid='
proc = subprocess.Popen(ps_cmd, stdout=subprocess.PIPE, shell=True)
retval = proc.wait()
c = ' '
output = ''
while(c != ''):
    c = proc.stdout.read(1)
    output += c  

# find numeric pids of each line
outputLines = output.splitlines()
pids = []
for line in outputLines:
    try:
        pids.append(int(line))
    except:
        continue
    

# Forward the port by running the ssh command
if(args.start):
    if(len(pids) > 0):
        print(port + ' is already forwarded to ' + host)
    else:
        try:
            if(os.system(ssh_cmd) == 0):
                print('Port ' + port + ' is forwarded to ' + host)
            else:
                print('Port ' + port + ' could not be forwarded to ' + host)
        except: 
            print('There was a problem forwarding port ' + port + ' to ' + host)
  

# Stop forwarding the port(s) by killing their processes
elif(args.stop):
    for pid in pids:
        print('pid = ' + str(pid))
        cmd = 'kill ' + str(pid)
        try:
            if(os.system(cmd) == 0):
                print('Port ' + port + ' unforwarded from ' + host)
            else:
                print('Port ' + port + ' forwarding to ' + host + ' not stopped')
        except: 
            print('There was a problem unforwarding port ' + port + ' to ' + host)
    


# Query the status of the port by testing if a forwarding process exists
elif(args.status):
    state = (' is not', ' is')[len(pids) > 0]
    print('Port ' + port + state + ' forwarded to ' + host)
        


