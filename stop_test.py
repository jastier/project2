#!/usr/bin/env python

# run a single test case that stops a port from being forwarded

import os

cmd = './single_port_forwarder.py -d lectura.cs.arizona.edu -p 8000 --stop'

os.system(cmd)

