#!/usr/bin/env python
from Cheetah.Template import Template
import os

modelList = [
             "MissingInitialTransition",
             "MissingInitialTransition2",
             "MissingInitialTransition3",
             "MultipleInitialTransition",
             "DuplicateStateNames",
             "JunctionNoGuard",
             "JunctionNoGuard2",
             "Junction3Trans",
             "JunctionDoubleGuard",
             "EntryExitArgs",
             "EntryExitArgs2",
             "EntryExitArgs3",
             "EntryExitArgs4",
             "EntryExitArgs5"
            ]


for model in modelList:
    os.system("rm -rf " + model + "/.Fault")
    os.system("rm -rf " + model + "/.simple")
    os.system("rm -rf " + model + "/.MultipleInitialTransition")
    os.system("rm -rf " + model + "/.MissingInitialTransition")
    os.system("rm -rf " + model + "/.MissingInitialTransition2")
    os.system("rm -rf " + model + "/.MissingInitialTransition3")
    os.system("rm -rf " + model + "/.EntryExitArgs")
    os.system("rm -rf " + model + "/.EntryExitArgs4")
    os.system("rm -rf " + model + "/.EntryExitArgs5")
    
