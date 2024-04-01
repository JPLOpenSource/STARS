#!/bin/env python3
# -----------------------------------------------------------------------
# ccoder.py
#
# Implements the C switch statement output for the Stars.
# The hierarchical state-machine is flattened into just the leaf states.
# This code is responsible for creating the flattened state-machine and
# performing polymorphism or inheritance on all the transitions.
#
# -----------------------------------------------------------------------


from Cheetah.Template import Template # type: ignore
import qmlib
import sys
import flattenstatemachine as flatt
from c_backend.ctemplates import CTemplate
from c_backend.cUnitTestTemplates import CUnitTestTemplate
from c_backend.cImplTemplates import CImplTemplate
from typing import List, Dict, Tuple, Any, Optional, IO
from qmlib import ElementTreeType
from lxml import etree


# Initialize global variables
codeTemplate = CTemplate()
unitTestTemplate = CUnitTestTemplate()
codeImplTemplate = CImplTemplate()

# -----------------------------------------------------------------------
# printSmHeader
#
# Print the state-machine header file
# -----------------------------------------------------------------------  
def printSmHeader(smname: str, root: ElementTreeType):

    hFile = open(smname + ".h", "w")

    eventList = []
    trans = root.iter('tran')
    for tran in trans:
        event = tran.get('trig').upper() + "_SIG"
        if event not in eventList:
            eventList.append(event)
        
    stateList = []
    states = root.iter('state')
    for state in states:
        stateList.append(state.get('name'))
            
    hFile.write(codeTemplate.fileHeader(smname, stateList, eventList))
        
        
# ---------------------------------------------------------------------------
# formatTarget
#
# From the input target function, return the C string for the target
# ---------------------------------------------------------------------------
def formatTarget(targ: str) -> str:
    return codeTemplate.target(targ)
    
# ---------------------------------------------------------------------------
# printTransition
#
# This function is designed to recursively process a transition 
# chain within a state machine, particularly focusing on handling choices 
# (conditional branches) within transitions. It aims to convert the transition 
# logic into a series of 'if then else' statements in a flat, textual format.
# ---------------------------------------------------------------------------
def printTransition(smname: str, tran: ElementTreeType) -> List[str]:
    rstr = []
    
    # Action
    action = qmlib.pick_action(tran)
    if action:
        functionList = qmlib.n_parse_function_args(action)
        for func in functionList:
            actionName, actionArgs = qmlib.parse_action(func)
            sig = codeTemplate.action(smname, actionName, actionArgs)
            rstr.append(sig)
    
    # Target
    targetState = tran.get('target')
    if targetState:
        rstr.append(formatTarget(targetState))

    # Choices  
    choices = tran.findall('choice')
    if len(choices) == 0:
        return rstr
    
    ifChoice = None
    elseChoice = None

    for choice in choices:
        guard = choice.find('guard')
        if guard is not None:
            if ifChoice is None:
                ifChoice = choice
        else:
            elseChoice = choice

    # Do the ifchoice    
    initialGuard = qmlib.pick_guard(ifChoice)
    actionName, actionArgs = qmlib.parse_action(initialGuard)  #type: ignore
    sig = codeTemplate.ifGuard(smname, actionName, actionArgs)
    rstr.append(sig)

    rstr = rstr + printTransition(smname, ifChoice)
    rstr.append("}")

    # Do the elseChoice
    if elseChoice is not None:
        rstr.append("else {")
        rstr = rstr + printTransition(smname, elseChoice)
        rstr.append("}")

    return rstr

  

# ---------------------------------------------------------------------------
# printStateTransition
#
# Print a transition from a state
# ---------------------------------------------------------------------------                   
def printStateTransition(smname: str, tran: ElementTreeType, cFile: IO):
        
    signal = tran.get('trig').upper() + "_SIG"
    transition = qmlib.format_C(printTransition(smname, tran), 24)
    cFile.write(codeTemplate.stateTransition(signal, transition))
    
# -----------------------------------------------------------------------
# printSmCode
#
# Print the state-machine C file
# -----------------------------------------------------------------------  
def printSmCode(smname: str, root: ElementTreeType):
           
    cFile = open(smname + ".c", "w")

    initialTran = root.find('initial')
    initialCode = qmlib.format_C(printTransition(smname, initialTran), 4)
    cFile.write(codeTemplate.stateMachineInit(smname, initialCode))
    
    states = root.iter("state")
    for state in states:
        cFile.write(codeTemplate.stateMachineState(state.get('name')))
        trans = state.findall('tran')
        for tran in trans:
            printStateTransition(smname, tran, cFile)
            
        cFile.write(codeTemplate.stateMachineBreak())
    
    cFile.write(codeTemplate.stateMachineFinalBreak())


# -----------------------------------------------------------------------
# printUnitCode
#
# Print unit test files
# -----------------------------------------------------------------------  
def printUnitCode(smname: str, root: ElementTreeType):

    # Open the generated files
    mainFile = open("main.c", "w")
    sendEventHFile = open("sendEvent.h", "w")
    sendEventCFile = open("sendEvent.c", "w")

    
    mainFile.write(unitTestTemplate.mainFile(smname))
    sendEventHFile.write(unitTestTemplate.sendEventHeaderFile(smname))
    
    trans = root.iter("tran")
    triggerList = []
    for tran in trans:
        trig = tran.get("trig").upper() + "_SIG"
        if trig not in triggerList:
            triggerList.append(trig)
        
    sendEventCFile.write(unitTestTemplate.sendEventFile(smname, triggerList))
    
    # Generate the test Driver if testDrv.txt file exists
    try:
        testDrvFile = open("../testDrv.txt", "r")
        print ("Generating testDrv.h")
        print ("Generating testDrv.c")
        testDrvHFile = open("testDrv.h", "w")
        testDrvCFile = open("testDrv.c", "w")
        testDrvHFile.write(unitTestTemplate.testDrvHeader(smname))
        testDrvCFile.write(unitTestTemplate.testDrvStart(smname))
        
        for line in testDrvFile:
            testDrvCFile.write(unitTestTemplate.testDrv(line))
        testDrvCFile.write("}")
        testDrvHFile.close()
        testDrvCFile.close()
    except FileNotFoundError:
        pass
    
    mainFile.close()
    sendEventHFile.close()
    sendEventCFile.close()


    
# -----------------------------------------------------------------------
# printImplCode
#
# Print Implementation files
# -----------------------------------------------------------------------  
class ImplFunc:
    signature = ""
    name = ""
    
    def __init__(self, signature, name):
        self.signature = signature
        self.name = name

def printImplCode(smname: str, root: ElementTreeType):
        
    # Open the generated files
    cImplFile = open(smname + "Impl.c", "w")
    hImplFile = open(smname + "Impl.h", "w")
        
        
    guardFunctions = qmlib.get_guard_functions(root)
    stateFunctions = qmlib.get_state_functions(root)
    transFunctions = qmlib.get_trans_functions(root)
    
    actionFunctions = stateFunctions + transFunctions
    
    guardList = []
    sigList = []
    for guard in guardFunctions:
        actionName, actionArgs = qmlib.parse_action(guard)
        sig = codeTemplate.guardSignature(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            guardList.append(ImplFunc(sig, qmlib.get_name(guard)))
   
   
    stateList = []
    sigList = []
    for action in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(action)
        sig = codeTemplate.actionSignature(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            stateList.append(ImplFunc(sig, qmlib.get_name(action)))
       
    # Write the header implementation file
    hImplFile.write(codeImplTemplate.implFileHeader(smname, guardList, stateList))
    
    # Write the C implementation file    
    cImplFile.write(codeImplTemplate.implFile(smname, guardList, stateList))

    cImplFile.close()
    hImplFile.close()
    
    return 

                   
# -----------------------------------------------------------------------
# generateCode
#
# This function generates the following code:
#
# - main.cpp (for unit testing)
# - Implementation code (for unit testing)
# - sendEvent (for unit testing)
# - State-machine code
#
# For a user the only important product is the State-machine code, 
# everything else is only important for the tool developer.

# ----------------------------------------------------------------------- 
def generateCode(smname: str, statechart: ElementTreeType, noImpl: bool):
    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate

    #qmlib.print_tree(statechart)
        
    print ("Generating flat C code for {0}".format(smname))
    

    flatchart : ElementTreeType = flatt.flatten_state_machine(statechart)
    
    if noImpl == False:
        # Generate the Impl files
        print ("Generating " + smname + "Impl.c")
        print ("Generating " + smname + "Impl.h")
        printImplCode(smname, flatchart)
    
        # Generate the unit test files
        print ("Generating main.c")
        print ("Generating sendEvent.h")
        print ("Generating sendEvent.c")

        printUnitCode(smname, flatchart)
    
    # Generate the header file
    print ("Generating " + smname + ".c")
    printSmHeader(smname, flatchart)
    
    # Generate the C file
    print ("Generating " + smname + ".h")
    printSmCode(smname, flatchart)
