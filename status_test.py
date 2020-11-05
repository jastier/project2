#!/usr/bin/env python

# run a single test case that checks the status of a forwarded port

import os

cmd = './single_port_forwarder.py -d lectura.cs.arizona.edu -p 8000 status'

os.system(cmd)

