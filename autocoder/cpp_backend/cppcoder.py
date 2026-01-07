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
from typing import List, Dict, Tuple, Any, Optional, IO, TextIO
from qmlib import ElementTreeType
from anytree import Node, PreOrderIter
import re
from xmiModelApi import XmiModel

# Initialize the global variables
codeTemplate = CppTemplate()
unitTestTemplate = CppUnitTestTemplate()
codeImplTemplate = CppImplTemplate()


# -----------------------------------------------------------------------
# printSmHeader
#
# Print the state-machine header file
# -----------------------------------------------------------------------  
def printSmHeader(xmiModel: XmiModel):
    stateMachine = xmiModel.tree.stateMachine

    hFile = open(f"{stateMachine}.h", "w")

    states = list()
    (actions, guards, signals) = getStateMachineMethods(xmiModel)

    #trans = root.iter('tran')

    #print(f"signals {signals}")

    isSuperstate = False

    for child in PreOrderIter(xmiModel.tree):
        if child.name == "STATE":
            for grandchild in PreOrderIter(child):
                # if the node is a superstate, do not add it to the state list
                if (grandchild.name == "STATE"):
                    if (child.stateName != grandchild.stateName):
                        isSuperstate = True
                        break
            if (not isSuperstate):
                states.append(child.stateName)

            isSuperstate = False
    
    signals = {signal.upper() + "_SIG" for signal in signals}
        
    actions = sorted(actions)
    guards = sorted(guards)
    signals = sorted(signals)
    #states = sorted(states)
        
    #guardFunctions = qmlib.get_guard_functions(root)
    #stateFunctions = qmlib.get_state_functions(root)
    #transFunctions = qmlib.get_trans_functions(root)

    #getInitTransitions(xmiModel)
    
    #actionFunctions = stateFunctions + transFunctions
      
    #funcList = []
    #sigList = []
    #for guard in guards:
        #print(f"guard: {guard}")
        #actionName, actionArgs = qmlib.parse_action(func)
       # sig = codeTemplate.guardSignature(stateMachine, action, actionArgs)
        #if sig not in sigList:
            #sigList.append(sig)
            #funcList.append(sig)
     
    #sigList = []
    #for action in actions:
        #print(f"acton: {action}")
        #actionName, actionArgs = qmlib.parse_action(func)
        #sig = codeTemplate.actionSignature(smname, actionName, actionArgs)
        #if sig not in sigList:
            #sigList.append(sig)
            #funcList.append(sig) 
    
    hFile.write(codeTemplate.fileHeader(stateMachine, states, signals, actions))

def getActionNames(input_string: str, fullSpecifier: bool):
    if input_string is None:
        return None

    # Use regex to find all procedural names before the '(' and ignore everything after
    procedural_names = re.findall(r'\b\w+(?=\()', input_string)
    # Join the names with commas
    output_string = ', '.join(procedural_names)

    if fullSpecifier:
        output_string = output_string + getActionDataType(input_string)

    return output_string

def getActionDataType(inputString: str):
    if inputString is None:
        return ""

    outputString = None

    # Get this index of the opening and closing parenthesis for function parameter list
    start = inputString.index('(') + 1
    end = inputString.index(')')

    # If there is any character between the parenthesis, treat it as a FPP datatype
    if (start != end):
        outputString = (": " + inputString[slice(start,end)])
    else:
        outputString = ""
    
    return outputString

def getStateMachineMethods(xmiModel: XmiModel):

    actionSet = set()
    guardSet = set()
    signalSet = set()

    for child in PreOrderIter(xmiModel.tree):
        #print(child.name)
        if child.name == "STATE":
            #actionSet.add(getActionNames(child.entry, True))
            actionSet.add(child.entry)
            actionSet.add(child.exit)
        if child.name == "TRANSITION":
            actionSet.add(child.action)
            guardSet.add(getActionNames(child.guard, False))
            if (child.event != None):
                #print(f"{child.name} - {child} - {child.event}")
                signalSet.add((child.event))
        if child.name == "JUNCTION":
            actionSet.add(child.ifAction)
            actionSet.add(child.elseAction)
            guardSet.add(child.guard)
        if child.name == "INITIAL":
            actionSet.add(child.action)

    # Remove empty strings
    actionSet = {item for item in actionSet if item}
    guardSet = {item for item in guardSet if item}
    signalSet = {item for item in signalSet if item}

    #for item in guardSet:
        #print("item: " + str(item))

    flatActions = {a.strip() for action in actionSet for a in action.split(',')}


    return (flatActions, guardSet, signalSet)

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

    #print(f"transition {rstr}")

    return rstr
  
# ---------------------------------------------------------------------------
# printStateTransition
#
# Print a transition from a state
# ---------------------------------------------------------------------------                   
def printStateTransition(smname: str, tran: Node, cFile: IO):
        
    signal = tran.get('trig').upper() + "_SIG"
    transition = qmlib.format_C(printTransition(smname, tran), 24)
    cFile.write(codeTemplate.stateTransition(signal, transition))

def getStates(xmiModel: XmiModel):
    states = list()

    isSuperstate = False

    for child in PreOrderIter(xmiModel.tree):
        if child.name == "STATE":
            for grandchild in PreOrderIter(child):
                # if the node is a superstate, do not add it to the state list
                if (grandchild.name == "STATE"):
                    if (child.stateName != grandchild.stateName):
                        isSuperstate = True
                        break
            if (not isSuperstate):
                states.append(child.stateName)

            isSuperstate = False
    
    return states

def resolveTransition(xmiModel: XmiModel, node: Node, states: List):
    if xmiModel.idMap[node.target].stateName in states:
        return xmiModel.idMap[node.target].stateName
    else:
        for child in xmiModel.idMap[node.target].children:
            if child.name == "INITIAL":
                return xmiModel.idMap[child.target].stateName


       
# -----------------------------------------------------------------------
# printSmCode
#
# Print the state-machine C file
# ----------------------------------------------------------------------- 
def printSmCode(node: Node, xmiModel: XmiModel, cFile: TextIO, level: int = 4):
    stateMachine = xmiModel.tree.stateMachine

    states = getStates(xmiModel)
           
    #initialTran = root.find('initial')

    defaultIndent = "  "

    indent = defaultIndent * level

    for state in states:
        cFile.write(codeTemplate.stateMachineState(state))

        for child in PreOrderIter(xmiModel.tree):
            if child.name == "TRANSITION":
                #print(xmiModel.idMap[child.source])
                if (xmiModel.idMap[child.source].stateName == state):
                    #print(f"State match with {state}")
                    guardExpr = f" if {getActionNames(child.guard, False)}" if child.guard else ""
                    transition = f"\n{indent}this->state = {resolveTransition(xmiModel, child, states)};" if child.kind is None else ""
                    action = f"\n{indent}{getActionNames(child.action, False)}();" if child.action else ""

                    if (action != "" or transition != ""):
                        cFile.write(f"{defaultIndent}case {child.event.upper() + "_SIG: "}{guardExpr}{action}{transition}\n{indent}break;\n")
        
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
def generateCode(xmiModel: XmiModel, noImpl: bool):
    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate

    stateMachine = xmiModel.tree.stateMachine

    currentNode = xmiModel.tree

    #qmRoot, smname = qmlib.get_state_machine(qmRoot)
        
    print (f"Generating flat C++ code for {stateMachine}")

    cFile = open(f"{stateMachine}.cpp", "w")

    xmiModel.getInitTransitions()

    xmiModel.getJunctions()

    (actions, guards, signals) = getStateMachineMethods(xmiModel)

    xmiModel.moveTransitions()

    #xmiModel.print()

    #initialCode = qmlib.format_C(printTransition(stateMachine, currentNode), 4)
    #cFile.write(codeTemplate.stateMachineInit(stateMachine, initialCode))
    
    #flatchart : ElementTreeType = flatt.flatten_state_machine(currentNode)

    
    if noImpl == False:
        # Generate the Impl files
        print (f"Generating {stateMachine}Impl.cpp")
        #printImplCode(smname, flatchart)
    
        # Generate the unit test files
        print ("Generating main.cpp")
        print ("Generating sendEvent.h")
        print ("Generating sendEvent.cpp")
        #printUnitCode(smname, flatchart)
    
    # Generate the header file
    print (f"Generating {stateMachine}.cpp")
    printSmHeader(xmiModel)
    
    # Generate the C file
    print (f"Generating {stateMachine}.h")

    initialCode = str()
    target = str()

    for child in currentNode.children:
        #print(f"{child.name}")

        if child.name == "INITIAL":
            #print(child.target)
            target = xmiModel.idMap[child.target].stateName
    
    for child in currentNode.children:
        if (child.name == "STATE"):
            #print(child.stateName)

            if (child.stateName == target):
                #print("node found")
                if child.entry:
                    initialCode = "  " + child.entry + ";"

            initialCode = initialCode + "\n  this->state = " + target + ";"

            break

    xmiModel.flattenModel()

    #xmiModel.print()

    #initialCode = qmlib.format_C(printTransition(stateMachine, Node), 4)
    cFile.write(codeTemplate.stateMachineInit(stateMachine, initialCode, ""))

    printSmCode(currentNode, xmiModel, cFile)
