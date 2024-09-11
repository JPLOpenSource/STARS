#!/bin/env python3
# -----------------------------------------------------------------------
# c++coder.py
#
# Implements the C switch statement output for the Stars.
# The hierarchical state-machine is flattened into just the leaf states.
# This code is responsible for creating the flattened state-machine and
# performing polymorphism or inheritance on all the transitions.
#
# -----------------------------------------------------------------------

import qmlib
import flattenstatemachine as flatt
from cpp_backend.cpptemplates import CppTemplate
from cpp_backend.cppUnitTestTemplates import CppUnitTestTemplate
from cpp_backend.cppImplTemplates import CppImplTemplate
from typing import List, Dict, Tuple, Any, Optional, IO
from qmlib import ElementTreeType

# Initialize the global variables
codeTemplate = CppTemplate()
unitTestTemplate = CppUnitTestTemplate()
codeImplTemplate = CppImplTemplate()


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
        
    guardFunctions = qmlib.get_guard_functions(root)
    stateFunctions = qmlib.get_state_functions(root)
    transFunctions = qmlib.get_trans_functions(root)  
    
    actionFunctions = stateFunctions + transFunctions
      
    funcList = []
    sigList = []
    for func in guardFunctions:
        actionName, actionArgs = qmlib.parse_action(func)
        sig = codeTemplate.guardSignature(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            funcList.append(sig)
     
    sigList = []
    for func in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(func)
        sig = codeTemplate.actionSignature(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            funcList.append(sig) 
    
    hFile.write(codeTemplate.fileHeader(smname, stateList, eventList, funcList))
        
        
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
# Recursively process the transition chain going down through all the
# choices.  Return a string of 'if then else' statements
# ---------------------------------------------------------------------------
def printTransition(smname: str, tran: ElementTreeType):
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
    if initialGuard is not None:
        actionName, actionArgs = qmlib.parse_action(initialGuard)
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

    cFile = open(smname + ".cpp", "w")
           
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
    mainFile= open("main.cpp", "w")
    sendEventHFile = open("sendEvent.h", "w")
    sendEventCFile = open("sendEvent.cpp", "w")
    
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
        print ("Generating testDrv.cpp")
        testDrvHFile = open("testDrv.h", "w")
        testDrvCFile = open("testDrv.cpp", "w")
        testDrvHFile.write(unitTestTemplate.testDrvHeader())
        testDrvCFile.write(unitTestTemplate.testDrvStart(smname))
        
        for line in testDrvFile:
            testDrvCFile.write(unitTestTemplate.testDrv(line, smname))
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
    cImplFile= open(smname+"Impl.cpp", "w")
        
    guardFunctions = qmlib.get_guard_functions(root)
    stateFunctions = qmlib.get_state_functions(root)
    transFunctions = qmlib.get_trans_functions(root)    
    
    actionFunctions = stateFunctions + transFunctions
    
    guardList = []
    sigList = []
    for guard in guardFunctions:
        actionName, actionArgs = qmlib.parse_action(guard)
        sig = codeTemplate.guardDef(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            guardList.append(ImplFunc(sig, qmlib.get_name(guard)))
        
    stateList = []
    sigList = []
    for action in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(action)
        sig = codeTemplate.actionDef(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            stateList.append(ImplFunc(sig, qmlib.get_name(action)))       
            
    # Write the C implementation file    
    cImplFile.write(codeImplTemplate.implFile(smname, guardList, stateList))
    

    cImplFile.close()
    
    return 
                   
# -----------------------------------------------------------------------
# generateCcode
#
# Print the state-machine C file
# ----------------------------------------------------------------------- 
def generateCode(qmRoot: ElementTreeType, noImpl: bool):
    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate

    qmRoot, smname = qmlib.get_state_machine(qmRoot)
        
    print ("Generating flat C++ code for {0}".format(smname))
    
    flatchart : ElementTreeType = flatt.flatten_state_machine(qmRoot)

    
    if noImpl == False:
        # Generate the Impl files
        print ("Generating " + smname + "Impl.cpp")
        printImplCode(smname, flatchart)
    
        # Generate the unit test files
        print ("Generating main.cpp")
        print ("Generating sendEvent.h")
        print ("Generating sendEvent.cpp")
        printUnitCode(smname, flatchart)
    
    # Generate the header file
    print ("Generating " + smname + ".cpp")
    printSmHeader(smname, flatchart)
    
    # Generate the C file
    print ("Generating " + smname + ".h")
    printSmCode(smname, flatchart)
