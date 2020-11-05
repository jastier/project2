#!/usr/bin/env python

# run a single test case that forwards a port

import os

cmd = './single_port_forwarder.py -d lectura.cs.arizona.edu -p 8000 start'

os.system(cmd)

