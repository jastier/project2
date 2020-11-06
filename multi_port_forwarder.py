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
# -p <port>              positive integer 
# <action>               'start' or 'stop' or 'status' 
#
# A collection of these three arguments define a Job that this script can run.
# eg ('-d lectura.cs.arizona.edu', '-p 8002', 'status'),


import os

# Add your port forwarding jobs here
jobs = (
    ('-d lectura.cs.arizona.edu', '-p 8002', 'status'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'start'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'status'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'stop'),
    ('-d lectura.cs.arizona.edu', '-p 8002', 'status'),
)


# Run each job.  
job_id = 0
print('Port Forwarder jobs to run: ' + str(len(jobs)))
for job in jobs:
    job_id += 1
    print("Starting job " + str(job_id) + '...')
    cmd = './single_port_forwarder.py'
    for arg in job:
        cmd += ' ' + arg
    print(cmd)
    for line in os.popen(cmd).read().splitlines():
        line = line.rstrip('\n')
        if(len(line) > 0):
            print(line)
    print("Job " + str(job_id) + ' completed.')
