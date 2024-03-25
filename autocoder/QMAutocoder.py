#!/usr/bin/env python3
# -----------------------------------------------------------------------
# QMAutocoder.py
#
# The State-machine Autocoder for the Quantum Leaps QM modeling tool
# This Autocoder outputs the following design pattern implementations:
#     - C switch statements
#     - C Quantum Framework
#     - C++ switch statements
#     - Fprime
#
# Usage: QMAutocoder.py [-h] [-noImpl] [-noSignals] [-namespace NAMESPACE] [-debug] {c,qf,c++,fprime} model
#
# State-machine Autocoder.
#
# Positional arguments:
#  {c,qf,c++,fprime}     back-end code to generate
#  model                 QM state-machine model file: <model>.qm#
#
# Optional arguments:
#  -h, --help            show this help message and exit
#  -noImpl               Don't generate the Impl files
#  -noSignals            Don't generate the Signals header file
#  -namespace NAMESPACE  Fprime namespace
#  -debug                prints out the models
# 
# Example:
#     QMAutocoder.py c -noImpl ping.qm
#     This will output the following files:
#        ping.h
#        ping.c
#
#     QMAutocoder.py fprime -noImpl -namespace PING ping.qm
#     This will output the following files:
#        ping.cpp
#        ping.h
#        ping.trans
#        pingStatesEnumAi.xml
#
#     QMAutocoder.py qf -noImpl ping.qm    
#     This will output the following files:
#       ping.h
#       ping.c
#       StatechartSignals.h
#
# 
#
# This file is responsible for reading the command line syntax, opening
# the model .qm file and invoking one of the output back-ends.
# -----------------------------------------------------------------------
import os
from lxml import etree
import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import argparse
import c_backend.ccoder as ccoder 
import qf_backend.qfcoder as qfcoder
import cpp_backend.cppcoder as cppcoder
import fprime_backend.fprimecoder as fprimecoder
import checkFaults
import CameoParser
import UmlParser

from typing import Any
ElementTreeType = Any


# -----------------------------------------------------------------------
# main
#
# -----------------------------------------------------------------------

parser = argparse.ArgumentParser(description='State-machine Autocoder.')
parser.add_argument("backend", type=str, choices=['c', 'qf', 'c++', 'fprime'], help="back-end code to generate")
parser.add_argument("model", help="QM state-machine model file: <model>.qm")
parser.add_argument("-noImpl", help="Don't generate the Impl files", action="store_true")
parser.add_argument("-noSignals", help="Don't generate the Signals header file", action="store_true")
parser.add_argument("-namespace", help="Fprime namespace")
parser.add_argument("-debug", help="prints out the models", action = "store_true")


args = parser.parse_args()
    
    
inputFile = args.model

suff = os.path.basename(inputFile).split('.')[1]

if suff == 'qm':
    root: ElementTreeType = etree.parse(inputFile)
elif suff == 'xml':
    root = CameoParser.processCameo(inputFile, args.debug)
elif suff == 'plantuml':
    root = UmlParser.processUml(inputFile, args.debug)
else:
    print("Unknown suffix {0} on file {1}".format(suff, inputFile))
    sys.exit(0)

package: ElementTreeType = root.find('package')
className = package.find('class')
statechart: ElementTreeType = className.find('statechart')
# Process the states by adding an index attribute
smname: str = className.get('name')

# Perform state-machine semantics checking
checkFaults.checkStateMachine(smname, statechart)

if args.backend == "c++":
        cppcoder.generateCode(smname, statechart, args.noImpl)
    
if args.backend == "c":
        ccoder.generateCode(smname, statechart, args.noImpl)
    
if args.backend == "qf":
    qfcoder.generateCode(smname, statechart, args.noImpl, args.noSignals)
    
if args.backend == 'fprime':
    if (args.namespace is None):
        print("*** Error - missing namespace argument for the fprime backend")
        exit(0)
    else:
            fprimecoder.generateCode(smname, statechart, args.noImpl, args.namespace)
        
        
    

