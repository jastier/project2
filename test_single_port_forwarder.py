#!/usr/bin/env python

# Debug tester for Joseph's single port forwarding python script.

import os

# used for reporting results
passStr = ' OK '
failStr = 'FAIL'

# path to software under test
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
    target + ' -d localhost -p 80',
    target + ' -d localhost -p 80 --start',
    target + ' -d localhost -p 80 --status',
    target + ' -d localhost -p 80 --stop',
    target + ' -d localhost -p 80 --start --status --stop',
    './exitFAIL.py',
    target,
    target + ' -d localhost',
    target + ' -p blah',
    target + ' -p 80',
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

