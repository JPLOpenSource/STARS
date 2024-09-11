#!/bin/env python3
# -----------------------------------------------------------------------
# fprimecoder.py
#
# Implements the C++ switch statement for fprime output for the Stars.
# The hierarchical state-machine is flattened into just the leaf states.
# This code is responsible for creating the flattened state-machine and
# performing polymorphism or inheritance on all the transitions.
#
# -----------------------------------------------------------------------

import qmlib
import flattenstatemachine as flatt
from fprime_backend.fprimetemplates import FprimeTemplate
from fprime_backend.fprimeUnitTestTemplates import FprimeUnitTestTemplate
from fprime_backend.fprimeImplTemplates import FprimeImplTemplate
from typing import List, Dict, Tuple, Any, Optional, IO
from qmlib import ElementTreeType
from pydantic import BaseModel
import json
import os

# Pydantic classes that specify the configSm.json
class State(BaseModel):
    stateName: str
    stateMachineInstance: List[str]

class FprimeConfig(BaseModel):
    nameSpace: str
    component: str
    componentPath: str
    autoHeaderFile: str
    componentBase: str
    state_machines: List[State]


# Initialize global variables
codeTemplate = FprimeTemplate()
unitTestTemplate = FprimeUnitTestTemplate()
codeImplTemplate = FprimeImplTemplate()

# -----------------------------------------------------------------------
# printSmHeader
#
# Print the state-machine header file
# -----------------------------------------------------------------------  
def printSmHeader(smname: str, qmRoot: ElementTreeType, namespace: str):
        
    hFile = open(smname+".hpp", "w")
    eventList = []
    trans = qmRoot.iter('tran')
    for tran in trans:
        event = tran.get('trig').upper() + "_SIG"
        if event not in eventList:
            eventList.append(event)
        
    stateList = []
    states = qmRoot.iter('state')
    for state in states:
        stateList.append(state.get('name'))            

    funcList = get_function_signatures(qmRoot, smname)

    hFile.write(codeTemplate.fileHeader(smname, stateList, eventList, namespace, funcList ))
        
        
# ---------------------------------------------------------------------------
# formatTarget
#
# From the input target function, return the C string for the target
# ---------------------------------------------------------------------------
def formatTarget(targ: str) -> str:
    return codeTemplate.target(targ)

    
# ---------------------------------------------------------------------------
# printFlatTransition
#
# This function is designed to recursively process a transition 
# chain within a state machine, particularly focusing on handling choices 
# (conditional branches) within transitions. It aims to convert the transition 
# logic into a series of 'if then else' statements in a flat, textual format. 
# ---------------------------------------------------------------------------
def printFlatTransition(smname: str, tran: ElementTreeType) -> List[str]:
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
    actionName, actionArgs = qmlib.parse_action(initialGuard)   #type: ignore
    sig = codeTemplate.ifGuard(smname, actionName, actionArgs)
    rstr.append(sig)

    rstr = rstr + printFlatTransition(smname, ifChoice)
    rstr.append("}")

    # Do the elseChoice
    if elseChoice is not None:
        rstr.append("else {")
        rstr = rstr + printFlatTransition(smname, elseChoice)
        rstr.append("}")

    return rstr


# -------------------------------------------------------------------------
# dfs_find_target_state
#
# This routine recursively parses the tree and builds a list of all the
# transitions.  Each transition consists of a guard and target tuple.
#
# -------------------------------------------------------------------------
def dfs_find_target_state(node: ElementTreeType, targetStates: List[Tuple[ElementTreeType, Any, Any]], guardList: List[str], actionList: List[str]):

    guard = node.find('guard')
    if guard is not None:
        guardName = guard.get('brief')
        if guardName not in guardList:
            guardList.append(guardName)

    action = node.find('action')
    if action is not None:
        actionName = action.get('brief')
        if actionName not in actionList:
            actionList.append(actionName)

    choices = node.findall('choice')

    if len(choices) == 0:
        targetState = node.get('target')
        guard = ";".join(guardList)
        action = ";".join(actionList)
        targetStates.append((targetState, guard, action))

    else:
        for choice in choices:
            dfs_find_target_state(choice, targetStates, guardList.copy(), actionList.copy())


# ---------------------------------------------------------------------------
# printStateTransition
#
# Print a transition from a state
# ---------------------------------------------------------------------------                   
def printStateTransition(state: ElementTreeType, smname: str, tran: ElementTreeType, cFile: IO, transFile: IO):
        
    targetStates: List[Tuple[ElementTreeType, Any, Any]] = []
    guardList: List[str] = []
    actionList: List[str] = []

    signal = tran.get('trig').upper() + "_SIG"
    transition = qmlib.format_C(printFlatTransition(smname, tran), 24)
    cFile.write(codeTemplate.stateTransition(signal, transition, smname))

    dfs_find_target_state(tran, targetStates, guardList, actionList)

    for target in targetStates:
        guard = target[1]
        action = target[2]
        if guard == "":
            guard = None
        if action == "":
            action = None
        if target[0] is None:
            targetState = state.get("name")
        else:
            targetState = target[0]
        transFile.write(f'InitialState = {state.get("name")}, Event = {tran.get("trig")}, guard = {guard}, action = {action}, TargetState = {targetState}\n')

       
# -----------------------------------------------------------------------
# printSmCode
#
# Print the state-machine C file
# -----------------------------------------------------------------------  
def printSmCode(smname: str, qmRoot: ElementTreeType, namespace: str):

    cFile= open(smname+".cpp", "w")
    transFile = open(smname+".trans", "w")
           
    initialTran = qmRoot.find('initial')
    initialCode = qmlib.format_C(printFlatTransition(smname, initialTran), 4)
    cFile.write(codeTemplate.stateMachineInit(smname, initialCode, namespace))

    states = qmRoot.iter("state")
    for state in states:
        cFile.write(codeTemplate.stateMachineState(state.get('name')))
        trans = state.findall('tran')
        for tran in trans:
            printStateTransition(state, smname, tran, cFile, transFile)

        cFile.write(codeTemplate.stateMachineBreak())
    
    cFile.write(codeTemplate.stateMachineFinalBreak())
    

# -----------------------------------------------------------------------
# printUnitCode
#
# Print unit test files
# -----------------------------------------------------------------------  
def printUnitCode(smname: str, implHdr: str, component: str, namespace: str, qmRoot: ElementTreeType):
    # Open the generated files
    mainFile= open("main.cpp", "w")
    sendEventHFile = open("sendEvent.h", "w")
    sendEventCFile = open("sendEvent.cpp", "w")
    
    mainFile.write(unitTestTemplate.mainFile(implHdr, component, namespace))
    sendEventHFile.write(unitTestTemplate.sendEventHeaderFile(smname, namespace))
    
    
    trans = qmRoot.iter("tran")
    triggerList = []
    for tran in trans:
        trig = tran.get("trig").upper() + "_SIG"
        if trig not in triggerList:
            triggerList.append(trig)
        
    sendEventCFile.write(unitTestTemplate.sendEventFile(smname, component, namespace, implHdr, triggerList))
    
    # Generate the test Driver if testDrv.txt file exists
    try:
        testDrvFile = open("../testDrv.txt", "r")
        print ("Generating testDrv.h")
        print ("Generating testDrv.cpp")
        testDrvHFile = open("testDrv.h", "w")
        testDrvCFile = open("testDrv.cpp", "w")
        testDrvHFile.write(unitTestTemplate.testDrvHeader())
        testDrvCFile.write(unitTestTemplate.testDrvStart(smname, component))
        
        for line in testDrvFile:
            testDrvCFile.write(unitTestTemplate.testDrv(line, smname, namespace))
        testDrvCFile.write("}")
        testDrvHFile.close()
        testDrvCFile.close()
    except FileNotFoundError:
        pass
    
    mainFile.close()
    sendEventHFile.close()
    sendEventCFile.close()
    

# -----------------------------------------------------------------------
# get_function_defs
#
# Return a tuple of lists of guard and action definitions
# -----------------------------------------------------------------------  
class ImplFunc:
    signature = ""
    name = ""

    def __init__(self, signature, name):
        self.signature = signature
        self.name = name

def get_function_defs(root: ElementTreeType, smname: str, namespace: str, component: str) -> Tuple[List[ImplFunc], List[ImplFunc]]:


    guardFunctions = qmlib.get_guard_functions(root)
    stateFunctions = qmlib.get_state_functions(root)
    transFunctions = qmlib.get_trans_functions(root)    
    
    actionFunctions = stateFunctions + transFunctions

    funcList = get_function_signatures(root, smname)

    guardList: List[ImplFunc]= []
    sigList: List[str] = []
    for guard in guardFunctions:
        actionName, actionArgs = qmlib.parse_action(guard)
        sig = codeTemplate.guardDef(smname, actionName, component, actionArgs, namespace)
        if sig not in sigList:
            sigList.append(sig)
            guardList.append(ImplFunc(sig, qmlib.get_name(guard)))
        
    stateList: List[ImplFunc] = []
    sigList = []
    for state in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(state)
        sig = codeTemplate.actionDef(smname, actionName, component, actionArgs, namespace)
        if sig not in sigList:
            sigList.append(sig)
            stateList.append(ImplFunc(sig, qmlib.get_name(state)))

    return (guardList, stateList)

# -----------------------------------------------------------------------
# get_function_signatures
#
# Return a list of all the function signatures in the model
# -----------------------------------------------------------------------  
def get_function_signatures(root: ElementTreeType, smname: str) -> List[str]:

    guardFunctions = qmlib.get_guard_functions(root)
    stateFunctions = qmlib.get_state_functions(root)
    transFunctions = qmlib.get_trans_functions(root)    

    actionFunctions = stateFunctions + transFunctions

    funcList = []

    for func in guardFunctions:
        actionName, actionArgs = qmlib.parse_action(func)
        sig = codeTemplate.guardSignature(smname, actionName, actionArgs)
        if sig not in funcList:
            funcList.append(sig)

    for func in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(func)
        sig = codeTemplate.actionSignature(smname, actionName, actionArgs)
        if sig not in funcList:
            funcList.append(sig)

    return funcList


# -----------------------------------------------------------------------
# printComponentCode
#
# Print Component stub files
# -----------------------------------------------------------------------  
def printComponentCode(qmRoot: ElementTreeType, smname: str, namespace: str, component: str):

    # Open the generated files
    compImplFile = open(component+".cpp", "w")
    compHdrFile = open(component+".hpp", "w")

    funcList = get_function_signatures(qmRoot, smname)

    compHdrFile.write(codeImplTemplate.componentHdrFile(smname, namespace, component, funcList))

    (guardList, actionList) = get_function_defs(qmRoot, smname, namespace, component)

    compImplFile.write(codeImplTemplate.componentFile(smname, namespace, component, guardList, actionList))

    compImplFile.close()
    compHdrFile.close()

    return 


# -----------------------------------------------------------------------
# printEnumFpp
#
# Print state enumeration fpp
# -----------------------------------------------------------------------  
def printEnumFpp(smname: str, qmRoot: ElementTreeType, namespace: str):
        
    # Open the generated files

    fileName = smname + ".fppi"
    file = open(fileName, "w")
    print(f'Generating {fileName}')
    
    states = qmRoot.iter("state")
    stateList = []
    for state in states:
        stateList.append(state.get('name'))
  
    # Write the C implementation file    
    file.write(codeImplTemplate.stateEnumFpp(smname, namespace, stateList))
    

    file.close()
    
    return 

# -----------------------------------------------------------------------
# generateCode
#
# This function generates the following code:
#
# - Component code (for unit testing)
# - main.cpp (for unit testing)
# - sendEvent (for unit testing)
# - State-machine code
# - Enum Ai.xml (needed for older versions of Fprime)
#
# For a user the only important product is the State-machine code, 
# everything else is only important for the tool developer.
# ----------------------------------------------------------------------- 
def generateCode(qmRoot: ElementTreeType, noImpl: bool, namespace: str):
    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate

    qmRoot, smname = qmlib.get_state_machine(qmRoot)

    print(f'Generating Fprime C++ backend for state machine {smname}')

    flatchart : ElementTreeType = flatt.flatten_state_machine(qmRoot)
    
    if noImpl == False:
        component = "SignalGen"
        implHdr = "SignalGen.hpp"
        # Generate the component files for unit testing only
        print ("Generating " + component + ".cpp")
        print ("Generating " + component + ".hpp")
        printComponentCode(flatchart, smname, namespace, component)      
    
        # Generate the unit test files
        print ("Generating main.cpp")
        print ("Generating sendEvent.h")
        print ("Generating sendEvent.cpp")
        printUnitCode(smname, implHdr, component, namespace, flatchart)
    
    # Generate the state-machine header file
    print ("Generating " + smname + ".cpp")
    print ("Generating " + smname + ".trans")
    printSmHeader(smname, flatchart, namespace)
    
    # Generate the state-machine implementation file
    print ("Generating " + smname + ".hpp")
    printSmCode(smname, flatchart, namespace)

    # Generate the states enumeration fpp
    printEnumFpp(smname, flatchart, namespace)
