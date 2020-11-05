#!/usr/bin/env python
#
# Author: Joseph Astier
# Date: 2020 October
#
# Debugging script for the Single-action port forwarder.  Each test case is
# run as a system call.   Feel free to add new cases.
#

import os

# used for reporting results
passStr = ' OK '
failStr = 'FAIL'

# path to test article
target = './single_port_forwarder.py'

# Perform the test with a system call.  A zero return value is a pass.
def doTest(t):
    print('TEST:  '+t)
    print('OUTPUT:')
    retval = (failStr, passStr)[(os.system(t)== 0)]
    print('RESULT: ' + retval + '\n')
    return (retval, t)
  

# Tests to perform.  They should probably have names
tests = (
    './exitOK.py',
    target + ' -d localhost -p 10000',
    target + ' -d localhost -p 10000 --start',
    target + ' -d localhost -p 10000 --status',
    target + ' -d localhost -p 10000 --stop',
    target + ' -d localhost -p 10000 --start --status --stop',
    './exitFAIL.py',
    target,
    target + ' -d localhost',
    target + ' -p blah',
    target + ' -p 10000',
)

# run the tests.  This output can be rather verbose.
results = map(doTest, tests)
tested = len(results)
passed = sum(map(lambda (a,b): (0,1)[a==passStr], results))
failed = tested-passed

# report the results in a concise way
print('Testing Summary: ')
for g in results:
    print(g[0] + ' ' + g[1])
print('Tested: ' + str(tested))
print('Passed: ' + str(passed))
print('Failed: ' + str(failed))
if(failed == 0):
    print('All tests passed.')

