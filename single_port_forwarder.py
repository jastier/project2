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


# Compose an ssh command that will start forward the port to the host
args = parser.parse_args()
port = str(args.p)
host = args.d
ssh_cmd = 'ssh -o ConnectTimeout=7 -NfL ' + port + ':localhost:' + port + ' ' + host

#print('ssh_cmd:')
#print ssh_cmd

# Find the pid(s) for any processes running our ssh command.  If any exist,
# the port has already been forwarded.
pids = []
ps_cmd = 'ps -C \'' + ssh_cmd + '\' -o pid='
proc = subprocess.Popen(ps_cmd, stdout=subprocess.PIPE, shell=True)
retval = proc.wait()
c = ' '
output = ''
while(c != ''):  # read process output
    c = proc.stdout.read(1)
    output += c  
outputLines = output.splitlines() # ps returns pids one per line
for line in outputLines:  
    try:
        pids.append(int(line))
    except:
        continue
    

# Forward the port by starting a process with the ssh command
if(args.start):
    print('Forwarding ' + port + ' to ' + host + '...')
    if(len(pids) == 0):
        try:
            os.system(ssh_cmd)
            print('Port '+port+' is now forwarded to '+host)
        except: 
            print('Could not forward port ' + port + ' to ' + host)
    else:
        for pid in pids:
            print('Port '+port+' was already forwarded to '+host+' ['+str(pid)+']')
        print('Nothing to do.')
  

# Stop forwarding the port(s) by killing their pids
elif(args.stop):
    print('Unforwarding ' + port + ' from ' + host + '...')
    for pid in pids:
        cmd = 'kill ' + str(pid)
        try:
            os.system(cmd)
            print('Port '+port+' is no longer forwarded to '+host +' ['+str(pid)+']')
        except: 
            print('Could not unforward port ' + port + ' from ' + host)
    if(len(pids) == 0):
        print('Port '+port+' was not forwarded to '+host)
        print('Nothing to do.')


# Query the status of the port by testing if it already has an ssh process
elif(args.status):
    for pid in pids:
        print('Port '+port+' is forwarded to '+host+' ['+str(pid)+']')
    if(len(pids) == 0):
        print('Port ' + port + ' is not forwarded to ' + host)
        
