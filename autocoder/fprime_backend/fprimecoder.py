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
import newflat
from fprime_backend.fprimetemplates import FprimeTemplate
from fprime_backend.fprimeUnitTestTemplates import FprimeUnitTestTemplate
from fprime_backend.fprimeImplTemplates import FprimeImplTemplate
from typing import List, Dict, Tuple, Any, TextIO
from qmlib import ElementTreeType
from xmiModelApi import XmiModel
from anytree import Node, PreOrderIter
import sys

# Initialize global variables
codeTemplate = FprimeTemplate()
unitTestTemplate = FprimeUnitTestTemplate()
codeImplTemplate = FprimeImplTemplate()

# -----------------------------------------------------------------------
# printSmHeader
#
# Print the state-machine header file
# -----------------------------------------------------------------------  
def printSmHeader(smname: str, 
                  xmiModel: XmiModel, 
                  namespace: str):
        
    hFile = open(smname+".hpp", "w")

    signalList = qmlib.get_signals(xmiModel)

    stateList = qmlib.get_states(xmiModel)
    junctionList = qmlib.get_junctions(xmiModel)

    funcList = get_function_signatures(xmiModel, smname)

    hFile.write(codeTemplate.fileHeader(smname, 
                                        stateList + junctionList, 
                                        signalList, 
                                        namespace, 
                                        funcList))
        
        
# ---------------------------------------------------------------------------
# formatTarget
#
# From the input target function, return the C string for the target
# ---------------------------------------------------------------------------
def formatTarget(targ: str) -> str:
    return codeTemplate.target(targ)

    
# ---------------------------------------------------------------------------
# printInitial
#
# Convert an initial transition into code
# ---------------------------------------------------------------------------
def printInitial(xmiModel: XmiModel,
                        smname: str, 
                        tran: Node,
                        stateName: str) -> List[str]:
    rstr = []

    if tran is None:
        rstr.append(f"this->state = {stateName};")
  
    else:
        # Action
        action = tran.action
        if action:
            functionList = qmlib.n_parse_function_args(action)
            for func in functionList:
                actionName, actionArgs = qmlib.parse_action(func)
                sig = codeTemplate.action(smname, actionName, actionArgs)
                rstr.append(sig)

        # Target
        if tran.target is not None:
            targetState = xmiModel.idMap[tran.target]
            stateCall = codeTemplate.call_state(targetState.stateName)
            rstr.append(stateCall)

    return rstr

# ---------------------------------------------------------------------------
# printTransition
#
# Convert a transition into code
# ---------------------------------------------------------------------------
def printTransition(xmiModel: XmiModel,
                        smname: str, 
                        tran: Node,
                        stateName: str) -> List[str]:
    rstr = []

    if tran is None:
        rstr.append(f"this->state = {stateName};")
  
    else:
        actionCode = []
        if tran.action:
            functionList = qmlib.n_parse_function_args(tran.action)
            for func in functionList:
                actionName, actionArgs = qmlib.parse_action(func)
                actionCode.append(codeTemplate.action(smname, actionName, actionArgs))

        if tran.target is not None:
            targetState = xmiModel.idMap[tran.target]
            targetCode = codeTemplate.call_state(targetState.stateName)
        else:
            targetCode = ""

        if tran.guard:
            guardName, guardArgs = qmlib.parse_action(tran.guard)
            guardCode = codeTemplate.ifGuard(smname, guardName, guardArgs)
            rstr.append(guardCode)
            rstr.extend(actionCode)
            rstr.append(targetCode)
            rstr.append("}")
        else:
            rstr.extend(actionCode)
            rstr.append(targetCode)

    return rstr
      
# -----------------------------------------------------------------------
# printSmCode
#
# Print the state-machine C file
# -----------------------------------------------------------------------  

def printSmCode(smname: str, 
                xmiModel: XmiModel, 
                namespace: str):

    cFile= open(smname+".cpp", "w")

    initialTran = get_initial_node(xmiModel.tree)
    assert initialTran is not None, "initial transition expected but not found"

    initialCode = qmlib.format_C(printInitial(xmiModel, smname, initialTran, None), 4)
    cFile.write(codeTemplate.stateMachineInit(smname, initialCode, namespace))

    for leafState in xmiModel.fstm.keys():
        cFile.write(codeTemplate.stateMachineState(leafState.stateName))
        for signal in xmiModel.fstm[leafState].keys():
            trans =  xmiModel.fstm[leafState][signal]
            transCode = qmlib.format_C(printTransition(xmiModel, smname, trans, leafState.stateName), 20)

            cFile.write(codeTemplate.stateTransition(signal, transCode, smname))
        cFile.write(codeTemplate.stateMachineBreak())
    cFile.write(codeTemplate.stateMachineFinalBreak())


    # State enter functions
    for node in PreOrderIter(xmiModel.tree):

        if node.name == "STATE":

            if node.entry:
                function_list = [func.strip() for func in node.entry.split(';') if func]
                entryActions = [func.split('(')[0] for func in function_list]
            else:
                entryActions = []
            initialTran = get_initial_node(node)
            initialCode = qmlib.format_C(printInitial(xmiModel, smname, initialTran, node.stateName), 4)
            cFile.write(codeTemplate.stateEntryFunction(namespace, smname, node.stateName, entryActions, initialCode))

        if node.name == "JUNCTION":

            if node.ifAction:
                function_list = [func.strip() for func in node.ifAction.split(';') if func]
                ifActions = [func.split('(')[0] for func in function_list]
            else:
                ifActions = []
            
            targetState = xmiModel.idMap[node.ifTarget]
            ifTarget = codeTemplate.call_state(targetState.stateName)
            guard = node.guard.split('(')[0]

            if node.elseAction:
                function_list = [func.strip() for func in node.elseAction.split(';') if func]
                elseActions = [func.split('(')[0] for func in function_list]
            else:
                elseActions = []
            targetState = xmiModel.idMap[node.elseTarget]
            elseTarget = codeTemplate.call_state(targetState.stateName)

            cFile.write(codeTemplate.junctionEntryFunction(namespace,
                                                           smname, 
                                                           node.stateName, 
                                                           guard, 
                                                           ifTarget, 
                                                           elseTarget, 
                                                           ifActions, 
                                                           elseActions))


# -----------------------------------------------------------------------
# printUnitCode
#
# Print unit test files
# -----------------------------------------------------------------------  
def printUnitCode(smname: str, 
                  implHdr: str, 
                  component: str, 
                  namespace: str, 
                  xmiModel: XmiModel):

    # Open the generated files
    mainFile= open("main.cpp", "w")
    sendEventHFile = open("sendEvent.h", "w")
    sendEventCFile = open("sendEvent.cpp", "w")
    
    mainFile.write(unitTestTemplate.mainFile(implHdr, component, namespace))
    sendEventHFile.write(unitTestTemplate.sendEventHeaderFile(smname, namespace))
    
    triggerList = qmlib.get_signals(xmiModel)
            
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

def get_function_defs(xmiModel: XmiModel, 
                      smname: str, 
                      namespace: str, 
                      component: str) -> Tuple[List[ImplFunc], List[ImplFunc]]:

    guardFunctions = qmlib.get_guard_functions(xmiModel)
    stateFunctions = qmlib.get_state_functions(xmiModel)
    transFunctions = qmlib.get_trans_functions(xmiModel)    
    
    actionFunctions = stateFunctions + transFunctions

    guardList: List[ImplFunc]= []
    sigList: List[str] = []
    for guard in guardFunctions:
        actionName, actionArgs = qmlib.parse_action(guard)
        signature = codeTemplate.guardDef(smname, actionName, component, actionArgs, namespace)
        if signature not in sigList:
            sigList.append(signature)
            guardList.append(ImplFunc(signature, qmlib.get_name(guard)))
        
    stateList: List[ImplFunc] = []
    sigList = []
    for state in actionFunctions:
        actionName, actionArgs = qmlib.parse_action(state)
        signature = codeTemplate.actionDef(smname, actionName, component, actionArgs, namespace)
        if signature not in sigList:
            sigList.append(signature)
            stateList.append(ImplFunc(signature, qmlib.get_name(state)))

    return (guardList, stateList)

# -----------------------------------------------------------------------
# get_function_signatures
#
# Return a list of all the function signatures in the model
# -----------------------------------------------------------------------  

def get_function_signatures(xmiModel: XmiModel, 
                            smname: str) -> List[str]:

    guardFunctions = qmlib.get_guard_functions(xmiModel)
    stateFunctions = qmlib.get_state_functions(xmiModel)
    transFunctions = qmlib.get_trans_functions(xmiModel)
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

    return sorted(funcList)

# -----------------------------------------------------------------------
# get_initial_node
#
# Get the immediate initial node under this node
# -----------------------------------------------------------------------
def get_initial_node(node: Node) -> Node:
    initialNode = None  

    for child in node.children:
        if child.name == "INITIAL":
            initialNode = child
            break

    return initialNode

# -----------------------------------------------------------------------
# printComponentCode
#
# Print Component stub files
# -----------------------------------------------------------------------  

def printComponentCode(xmiModel: XmiModel, 
                       smname: str, 
                       namespace: str, 
                       component: str):

    # Open the generated files
    compImplFile = open(component+".cpp", "w")
    compHdrFile = open(component+".hpp", "w")
    
    funcList = get_function_signatures(xmiModel, smname)

    compHdrFile.write(codeImplTemplate.componentHdrFile(smname, namespace, component, funcList))

    (guardList, actionList) = get_function_defs(xmiModel, smname, namespace, component)

    compImplFile.write(codeImplTemplate.componentFile(smname, namespace, component, guardList, actionList))

    compImplFile.close()
    compHdrFile.close()

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

def generateCode(xmiModel: XmiModel, 
                 noImpl: bool, 
                 namespace: str):

    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate
    
    print("Generate Fprime code")

    if noImpl == False:
        component = "SignalGen"
        implHdr = "SignalGen.hpp"
        # Generate the component files for unit testing only
        print ("Generating " + component + ".cpp")
        print ("Generating " + component + ".hpp")
        smname = xmiModel.getStateMachineName()
        print(f'smname = {smname}')
        printComponentCode(xmiModel, smname, namespace, component)   

        # Generate the unit test files
        print ("Generating main.cpp")
        print ("Generating sendEvent.h")
        print ("Generating sendEvent.cpp")
        printUnitCode(smname, implHdr, component, namespace, xmiModel)

        # Generate the state-machine header file
        print ("Generating " + smname + ".hpp")
        print ("Generating " + smname + ".trans")
        printSmHeader(smname, xmiModel, namespace)

        # Generate the state-machine implementation file
        print ("Generating " + smname + ".hpp")
        printSmCode(smname, xmiModel, namespace)
