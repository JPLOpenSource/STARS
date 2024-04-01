#!/bin/env python3
# -----------------------------------------------------------------------
# qfcoder.py
# 
# Implements the C Quantum Framework (QF) output of the Stars.
# The QF preserves the hierarchy of the state-machine.
# This output is the most common state-machine implementation at JPL and 
# is used in multiple JPL spacecraft flight software.
#
# -----------------------------------------------------------------------
# mypy: ignore-errors

from lxml import etree
import sys
import flattenstatemachine as flatt
from Cheetah.Template import Template
import qmlib
from qf_backend.qftemplates import QFTemplate
from qf_backend.qfUnitTestTemplates import QFUnitTestTemplate
from qf_backend.qfImplTemplates import QFImplTemplate

    
# ---------------------------------------------------------------------------
# formatTarget
#
# From the input target function, return the C string for the target
# ---------------------------------------------------------------------------
def formatTarget(sm, target):
    return codeTemplate.target(sm, target)

    
# ---------------------------------------------------------------------------
# printStateDef
#
# Print a state function definition with Entry, Exit and Initial Transition
# ---------------------------------------------------------------------------         
def printStateDef(sm, state):
    
    stateName = state.get('name')
    
    # Check for state Entry function
    entry = state.find('entry')
    if entry is not None:
        functionList = qmlib.n_parse_function_args(entry.get('brief'))
        stateEntryFunction = ""
        for func in functionList:
            actionName, actionArgs = qmlib.parse_action(func)
            stateEntryFunction = stateEntryFunction + codeTemplate.action(sm, actionName, actionArgs)
    else:
        stateEntryFunction = None
    
    # Check for state Exit function
    exit = state.find('exit')
    if exit is not None:
        functionList = qmlib.n_parse_function_args(exit.get('brief'))
        stateExitFunction = ""
        for func in functionList:
            actionName, actionArgs = qmlib.parse_action(func)
            stateExitFunction = stateExitFunction + codeTemplate.action(sm, actionName, actionArgs)
    else:
        stateExitFunction = None
        

    initialTran = state.find('initial')
    if initialTran is not None:
        initialCode = qmlib.format_C(printTransition(sm, initialTran), 4)
    else:
        initialCode = None

    cFile.write(codeTemplate.stateMachineState(sm, stateName, initialCode, stateEntryFunction, stateExitFunction))
    

# ---------------------------------------------------------------------------
# printTransition
#
# Recursively process the transition chain going down through all the
# choices.  Return a string of 'if then else' statements
# ---------------------------------------------------------------------------
def printTransition(smname, tran):
    rstr = []
    
    # Action
    action = qmlib.pick_action(tran)
    if action:
        functionList = qmlib.n_parse_function_args(action)
        stateExitFunction = ""
        for func in functionList:
            actionName, actionArgs = qmlib.parse_action(func)
            rstr.append(codeTemplate.action(smname, actionName, actionArgs))
    
    # Target
    targetState = flatt.get_tran_target(tran)
    if targetState:
        rstr.append(formatTarget(smname, targetState))
      
    # Choices  
    choices = tran.findall('choice')
    if len(choices) == 0:
        return rstr
        
    foundGuard = False
    ifChoice = None
    elseChoice = None
    for choice in choices:
        guard = choice.find('guard')
        if guard is not None:
            assert(foundGuard == False)
            foundGuard = True
            ifChoice = choice
        else:
            elseChoice = choice     
    assert(foundGuard == True)
        
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
# Print a state transition
# ---------------------------------------------------------------------------         
def printStateTransition(sm, tran):
      
    signal = tran.get('trig').upper() + "_SIG"
    transition = qmlib.format_C(printTransition(sm, tran), 4)
    cFile.write(codeTemplate.stateTransition(signal, transition))
    
# ---------------------------------------------------------------------------
# printStateParent
#
# Print the state return parent
# ---------------------------------------------------------------------------         
def printStateParent(sm, parent):
        
    if parent.get('name') is not None:
        parent = sm + "_" + parent.get('name')
    else:
        parent = None
 
    cFile.write(codeTemplate.stateParent(parent))
    

# -----------------------------------------------------------------------
# printSmHeader
#
# Print the state-machine header file
# -----------------------------------------------------------------------    
def printSmHeader(smname, root):
 
    stateList = []    
    states = root.iter("state")
    for state in states:
        stateList.append(state.get('name'))
        
    hFile.write(codeTemplate.fileHeader(stateList, smname))
              
# -----------------------------------------------------------------------
# printSmCode
#
# Print the state-machine code
# -----------------------------------------------------------------------    
def printSmCode(smname, root):

    initialTran = root.find('initial')
 
    initialCode = qmlib.format_C(printTransition(smname, initialTran), 4)
    cFile.write(codeTemplate.stateMachineInit(smname, initialCode))

       
    states = root.iter("state")
    for state in states:
        printStateDef(smname, state)
       
        transitions = state.findall('tran')
        for trans in transitions:
            printStateTransition(smname, trans)
            
        printStateParent(smname, state.getparent())
        
# -----------------------------------------------------------------------
# printSignals
#
# Print the StatechartSignals.h
# -----------------------------------------------------------------------    
def printSignals(smname, root):

    trans = root.iter("tran")
    triggerList = []
    for tran in trans:
        trig = tran.get("trig").upper() + "_SIG"
        if trig not in triggerList:
            triggerList.append(trig)
        
    signalFile.write(codeTemplate.signals(triggerList))


# -----------------------------------------------------------------------
# printImplCode
#
# Print Implementation files
# -----------------------------------------------------------------------  
def printImplCode(smname, root):
        
    # Open the generated files
    cFile= open(smname+"Impl.c", "w")
    hFile = open(smname+"Impl.h", "w")

    class ImplFunc:
        signature = ""
        name = ""
        
        def __init__(self, signature, name):
            self.signature = signature
            self.name = name
            
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
    for state in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(state)
        sig = codeTemplate.actionSignature(smname, actionName, actionArgs)
        if sig not in sigList:
            sigList.append(sig)
            stateList.append(ImplFunc(sig, qmlib.get_name(state)))
            
    # Write the header implementation file    
    hFile.write(codeImplTemplate.implFileHeader(smname, guardList, stateList))
    
    # Write the C implementation file    
    cFile.write(codeImplTemplate.implFile(smname, guardList, stateList))
    

    cFile.close()
    hFile.close()
    return 
   
# -----------------------------------------------------------------------
# printUnitCode
#
# Print unit test files
# -----------------------------------------------------------------------  
def printUnitCode(smname, root):
    # Open the generated files
    mainFile= open("main.c", "w")
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
# changeStateNames
#
# Recursively change state names to include the names of the parent states
# -----------------------------------------------------------------------
def changeStateNames(root, parentName):
    stateNames = []
    states = root.findall('state')
    for state in states:
        if parentName is not None:
            newName = parentName + '_' + state.get('name')
        else:
            newName = state.get('name')
        changeStateNames(state, newName)
        state.set('name', newName)
            
# -----------------------------------------------------------------------
# generateCcode
#
# Print the state-machine C file
# ----------------------------------------------------------------------- 
def generateCode(smname, statechart, noImpl, noSignals):
    global backend
    global cFile
    global hFile
    global signalFile
    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate
    
    # Change the state names in the xml to reflect the state hierarchy
    changeStateNames(statechart, None)
    
    
    backend = "C Quantum Framework"
    print ("Generating C Quantum Framework code for {0}".format(smname))
    
    # Use this code template class
    codeTemplate = QFTemplate()
    unitTestTemplate = QFUnitTestTemplate()
    codeImplTemplate = QFImplTemplate()
    
    # Open the generated files
    cFile= open(smname+".c", "w")
    hFile = open(smname+".h", "w")
    
    if noImpl == False:
        # Generate the Impl files
        print ("Generating " + smname + "Impl.c")
        print ("Generating " + smname + "Impl.h")
        printImplCode(smname, statechart)
    
        # Generate the unit test files
        print ("Generating main.c")
        print ("Generating sendEvent.h")
        print ("Generating sendEvent.c")
        printUnitCode(smname, statechart)

       
    if noSignals == False:
        # Open the generated files
        cFile= open(smname+".c", "w")
        hFile = open(smname+".h", "w")
        signalFile = open("StatechartSignals.h", "w")
        print ("Generating StatechartSignals.h")
        printSignals(smname, statechart)

    # Generate the header file
    print ("Generating " + smname + ".c")
    printSmHeader(smname, statechart)
    
    # Generate the C file
    print ("Generating " + smname + ".h")
    printSmCode(smname, statechart)
    



