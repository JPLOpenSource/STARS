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
from typing import Tuple
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

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
from xmiModelApi import XmiModel
from zipfile import ZipFile


from lxml.etree import _ElementTree
ElementTreeType = _ElementTree 

# -----------------------------------------------------------------------
# getQmRoot
#
# Parse the input model files and return the QM Root which is used
# for the code generation.
# -----------------------------------------------------------------------
def getQmRoot(modelFileName: str) -> Tuple[ElementTreeType, XmiModel] :

    suff = os.path.basename(modelFileName).split('.')[1]

    qmRoot: ElementTreeType
    xmiModel: XmiModel

    if suff == 'qm':
        qmRoot = etree.parse(modelFileName)
        # Translate QM to XMI
        xmiModel = QmParser.getXmiModel(qmRoot)
    elif suff == 'xml':
        # Translate Cameo to XMI
        cameoRoot: ElementTreeType = etree.parse(modelFileName)
        xmiModel = CameoParser.getXmiModel(cameoRoot)
        # Translate XMI to QM
        qmRoot = xmiToQm.translateXmiModelToQmFile(xmiModel, args.debug)
    elif suff == 'mdzip':
        # Cameo mdzip file
        za = ZipFile(modelFileName)
        buf = za.read('com.nomagic.magicdraw.uml_model.model')
        cameoRoot: ElementTreeType = etree.ElementTree(etree.fromstring(buf))
        xmiModel = CameoParser.getXmiModel(cameoRoot)
        qmRoot = xmiToQm.translateXmiModelToQmFile(xmiModel, args.debug)
    elif suff == 'plantuml':
        # Translate UML to XMI
        xmiModel = UmlParser.getXmiModel(modelFileName)
        # Translate XMI to QM
        qmRoot = xmiToQm.translateXmiModelToQmFile(xmiModel, args.debug)
    else:
        print("Unknown suffix {0} on file {1}".format(suff, modelFileName))
        sys.exit(0)

    return qmRoot, xmiModel


# -----------------------------------------------------------------------
# main
#
# -----------------------------------------------------------------------

the_description="""
Autocoder for state machines.

Input model based on file extenion:
  .qf       QF model file
  .xml      Cameo model file
  .mdzip    Cameo project file
  .plantuml  PlantUML model file
"""
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description=the_description)
parser.add_argument("-backend", type=str, choices=['c', 'qf', 'c++', 'fprime', 'test'], help="back-end code to generate")
parser.add_argument("-model", help="state-machine model file")
parser.add_argument("-noImpl", help="Don't generate the Impl files", action="store_true")
parser.add_argument("-noSignals", help="Don't generate the Signals header file", action="store_true")
parser.add_argument("-namespace", help="Fprime namespace")
parser.add_argument("-debug", help="prints out the models", action = "store_true")


args = parser.parse_args()

qmRoot: ElementTreeType
xmiModel: XmiModel
smname: str

qmRoot, xmiModel = getQmRoot(args.model)

# Check Correctness of the QM
checkFaults.checkStateMachine(qmRoot)

if args.backend == "c++":
    cppcoder.generateCode(qmRoot, args.noImpl)
    
if args.backend == "c":
    ccoder.generateCode(qmRoot, args.noImpl)
    
if args.backend == "qf":
    qfcoder.generateCode(qmRoot, args.noImpl, args.noSignals)

if args.backend == "test":
    testcoder.generateCode(qmRoot)
    
if args.backend == 'fprime':
    if (args.namespace is None):
        print("*** Error - missing namespace argument for the fprime backend")
        exit(0)
    else:
            fppcoder.generateCode(xmiModel)
            fprimecoder.generateCode(qmRoot, args.noImpl, args.namespace)

            
        
    

