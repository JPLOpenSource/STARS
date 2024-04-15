#!/usr/bin/env python3

# -----------------------------------------------------------------------
# Filename: fault.py
#
# A python script to run the autocoder and check that it catches
# semantic errors.
#
# ./fault.py <test description> <model>
#
# example:
# > ./fault.py "Missing initial transition" Fault.qm
#
# -----------------------------------------------------------------------


import subprocess
import sys
import os

root = os.getenv('ROOT')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printPass():
    print (model + " unit test --> " + bcolors.OKGREEN + "PASS" + bcolors.ENDC)

def printFail():
    print (model + " unit test --> " + bcolors.FAIL + "FAIL" + bcolors.ENDC)
    

# -----------------------------------------------------------------------
# main
#
# -----------------------------------------------------------------------

model = "???"
sm = "???"

if (len(sys.argv) < 3):
    printFail()
    print ("    Reason: {0}".format("Missing model and description arguments to fault.py"))
    sys.exit()

model = sys.argv[1]
sm = sys.argv[2]
    
try:
    # Run the executable and store stdout in a file
    tmpFileName = '/tmp/results'
    resFile = open(tmpFileName, 'w')
    subprocess.call([root + "/autocoder/Stars.py", "-backend", "c", "-model", sys.argv[2]], stdout=resFile)
    resFile.close()
    
    # Compare the output results with the goldy
    resFile = open(tmpFileName, 'r')
    goldyFile = open('goldy.txt', 'r')
    results = resFile.read()
    goldy = goldyFile.read()
    
    # If the results are the same as goldy then pass the test
    if results == goldy:
        printPass()
    else:
        printFail()
        print ("   Reason: {0}".format("Output does not match goldy.txt"))

except:
    printFail()
    print ("   Reason: {0}".format(sys.exc_info()))


