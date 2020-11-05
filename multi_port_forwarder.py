#!/usr/bin/env python
#
# Author: Joseph Astier
# Date: 2020 October
#
# Multiple Port Forwarder.  This script will manage forwarding multiple
# ports, by repeatedly calling the Single Port Forwarder.  Each call to the
# Single Port Forwarder requires three arguments:
#
# -d <destination>       hostname or IP address 
#
# -p <port>              positive integer 
#
# <action>               'start', 'stop', or 'status' 
#

import threading
import os

# Add your port forwarding jobs here.  Number of Jobs is arbitrary, as is
# the order in which the three arguments appear.
jobs = (
    ('-d lectura.cs.arizona.edu', '-p 8002', 'start'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'status'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'stop'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'status'),
)


# Single Port Forwarder script
spf = './single_port_forwarder.py'


# Run one job
def jobRunner(arg1, arg2, arg3):
    cmd = spf + ' ' + arg1 + ' ' + arg2 + ' ' + arg3
    print(cmd)
    os.system(cmd)


# Start a thread for each job
thread_list = []
for job in jobs:
    thread = threading.Thread(target=jobRunner, args=job)
    thread_list.append(thread)
    thread.start()

