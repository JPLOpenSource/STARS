#!/usr/bin/env python3

# -----------------------------------------------------------------------
# Filename: run.py
#
# A python script to run a state-machine model unit test
# This script assumes the test executable is built and resides 
# in the directory in which this script is invoked and is called
# 'test'
#
# ./run.py <model description>
#
# example:
# > ./run.py "Junction (c back-end)"
#
# -----------------------------------------------------------------------


import subprocess
import sys
import os
import argparse


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
    print(f'{model} model ({backend} back-end) unit test --> {bcolors.OKGREEN}PASS{bcolors.ENDC}')

def printFail():
    print(f'{model} model ({backend} back-end) unit test --> {bcolors.FAIL}FAIL{bcolors.ENDC}')
    

# -----------------------------------------------------------------------
# main
#
# -----------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Run and Check against the goldy.')
parser.add_argument("model", help="Name of the model")
parser.add_argument("goldy", help="Name of the goldy file to check against")
parser.add_argument("backend", help="The autocoder backend")

args = parser.parse_args()

model = args.model
goldy = args.goldy
backend = args.backend

try:
    # Run the executable and store stdout in a file
    tmpFileName = '/tmp/results'
    resFile = open(tmpFileName, 'w')
    subprocess.call(["./test"], stdout=resFile)
    resFile.close()
    
    # Compare the output results with the goldy
    resFile = open(tmpFileName, 'r')
    goldyFile = open("../" + args.goldy, 'r')
    results = resFile.read()
    goldy = goldyFile.read()
    
    # If the results are the same as goldy then pass the test
    if results == goldy:
        printPass()
    else:
        printFail()
        print ("   Reason: {0}".format("Output does not match ../" + args.goldy))

except:
    printFail()
    print ("   Reason: {0}".format(sys.exc_info()))


