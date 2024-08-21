#!/usr/bin/env python3
# -----------------------------------------------------------------------
# Stars.py
#
# The State-machine Autocoder for generating state-machine code
# from MagicDraw Cameo or the Quantum Leaps QM modeling tool or PlantUML.
# This Autocoder outputs one of the following back ends:
#     - C switch statements
#     - C Quantum Framework
#     - C++ switch statements
#     - Fprime
#
# usage: Stars.py [-h] [-backend {c,qf,c++,fprime}] [-model MODEL] [-noImpl] [-noSignals] [-namespace NAMESPACE] [-debug] [-smbase]
#
# State-machine Autocoder.
#
# optional arguments:
#   -h, --help            show this help message and exit
#   -backend {c,qf,c++,fprime}
#                         back-end code to generate
#   -model MODEL          QM state-machine model file: <model>.qm
#   -noImpl               Don't generate the Impl files
#   -noSignals            Don't generate the Signals header file
#   -namespace NAMESPACE  Fprime namespace
#   -debug                prints out the models
#   -smbase               Generates the component state-machine base class
# 
# Example:  To generate state-machine code
#     ./Stars.py -backend c -noImpl -model Blinky.qm
#     This will output the following files:
#        Blinky.h
#        Blinky.c
#
#     ./Stars.py -backend fprime -noImpl -namespace Components -model Blinky.qm
#     This will output the following files:
#        Blinky.cpp
#        Blinky.h
#        Blinky.fppi
#        Blinky.trans
#
#     ./Stars.py -backend qf -noImpl -model Blinky.qm    
#     This will output the following files:
#       Blinky.h
#       Blinky.c
#       StatechartSignals.h
#
# Example:  To generate fprime component state-machine base class artifacts
# Assuming a configSm.json file:
#
# {
#     "nameSpace": "Components",
#     "component": "SignalGen",
#     "componentPath": ".",
#     "autoHeaderFile": "SignalGenComponentAc.hpp",
#     "componentBase": "SignalGenComponentBase",
#     "state_machines": [
#         {
#             "stateName": "Blinky",
#             "stateMachineInstance": ["blinky1", "blinky2"]
#         },
#         {
#             "stateName": "Toggle",
#             "stateMachineInstance": ["toggle"]
#         }
#     ]
# }
#
# And a CMakeLists.txt file
#
#      ./Stars.py -smbase
#      This will output the following files:
#       SignalGenSmBase.hpp
#       SignalGenSmBase.cpp
#       SMEvents.fpp
#       state-machine.fppi
#       Update to CMakeLists.txt
#
#
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
import test_backend.testcoder as testcoder
import fprime_backend.fppcoder as fppcoder
import checkFaults
import CameoParser
import QmParser
import UmlParser
import xmiToQm
import qmlib


from typing import Any
ElementTreeType = Any


# -----------------------------------------------------------------------
# main
#
# -----------------------------------------------------------------------

parser = argparse.ArgumentParser(description='State-machine Autocoder.')
parser.add_argument("-backend", type=str, choices=['c', 'qf', 'c++', 'fprime', 'test'], help="back-end code to generate")
parser.add_argument("-model", help="QM state-machine model file: <model>.qm")
parser.add_argument("-noImpl", help="Don't generate the Impl files", action="store_true")
parser.add_argument("-noSignals", help="Don't generate the Signals header file", action="store_true")
parser.add_argument("-namespace", help="Fprime namespace")
parser.add_argument("-debug", help="prints out the models", action = "store_true")


args = parser.parse_args()

# Do the state machine autocoder
inputFile = args.model

suff = os.path.basename(inputFile).split('.')[1]

if suff == 'qm':
    root: ElementTreeType = etree.parse(inputFile)
elif suff == 'xml':
    xmiModel = CameoParser.getXmiModel(inputFile)
    root = xmiToQm.translateXmiModelToQmFile(xmiModel, args.debug)
elif suff == 'plantuml':
    xmiModel = UmlParser.getXmiModel(inputFile)
    root =  xmiToQm.translateXmiModelToQmFile(xmiModel, args.debug)
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

# Only do the QM to XMI translation after the semanics have been checked.
if suff == 'qm':
    xmiModel = QmParser.getXmiModel(inputFile)

if args.backend == "c++":
    cppcoder.generateCode(smname, statechart, args.noImpl)
    
if args.backend == "c":
    ccoder.generateCode(smname, statechart, args.noImpl)
    
if args.backend == "qf":
    qfcoder.generateCode(smname, statechart, args.noImpl, args.noSignals)

if args.backend == "test":
    testcoder.generateCode(smname, statechart)
    
if args.backend == 'fprime':
    if (args.namespace is None):
        print("*** Error - missing namespace argument for the fprime backend")
        exit(0)
    else:
            # if suff == "plantuml" or suff == "xml":
            fppcoder.generateCode(xmiModel)
            fprimecoder.generateCode(smname, statechart, args.noImpl, args.namespace)

            
        
    

