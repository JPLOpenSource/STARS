#!/bin/env python3
# -----------------------------------------------------------------------
# fppcoder.py
#
# From an xmiModel, translate to a FPP state machine
# -----------------------------------------------------------------------
from anytree import Node, PreOrderIter
import re
from xmiModelApi import XmiModel
from typing import TextIO


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

# -----------------------------------------------------------------------
# processNode
#
# Process the XMI model into FPP
# -----------------------------------------------------------------------
def processNode(node: Node, 
                xmiModel: XmiModel, 
                fppFile: TextIO, 
                level:int = 0):

    indent = "  " * level

    for child in node.children:

        if child.name == "INITIAL":
            target = xmiModel.idMap[child.target].stateName
            doExpr = f" do {{ {getActionNames(child.action, False)} }}" if child.action else ""
            fppFile.write(f"{indent}initial{doExpr} enter {target}\n")

        if child.name == "JUNCTION":
            ifTarget = xmiModel.idMap[child.ifTarget].stateName
            elseTarget = xmiModel.idMap[child.elseTarget].stateName
            doIfExpr = f" do {{ {getActionNames(child.ifAction, False)} }}" if child.ifAction else ""
            doElseExpr = f" do {{ {getActionNames(child.elseAction, False)} }}" if child.elseAction else ""
            fppFile.write(f"{indent}choice {child.stateName} {{\n")
            fppFile.write(f"{indent}  if {child.guard}{doIfExpr} enter {ifTarget} else{doElseExpr} enter {elseTarget}\n")
            fppFile.write(f"{indent}}}\n")

        if child.name == "TRANSITION":
            guardExpr = f" if {getActionNames(child.guard, False)}" if child.guard else ""
            enterExpr = f" enter {xmiModel.idMap[child.target].stateName}" if child.kind is None else ""
            doExpr = f" do {{ {getActionNames(child.action, False)} }}" if child.action else ""
            fppFile.write(f"{indent}on {child.event}{guardExpr}{doExpr}{enterExpr}\n")

        if child.name == "STATE":
            stateName = child.stateName
            enterExpr = f" entry do {{ {getActionNames(child.entry, False)} }}" if child.entry else ""
            exitExpr = f" exit do {{ {getActionNames(child.exit, False)} }}" if child.exit else ""
            fppFile.write(f"{indent}state {stateName} {{\n")
            if enterExpr:
                fppFile.write(f"{indent}{enterExpr}\n")
            if exitExpr:
                fppFile.write(f"{indent}{exitExpr}\n")
            processNode(child, xmiModel, fppFile, level+1)
            fppFile.write(f"{indent}}}\n\n")
       
# -----------------------------------------------------------------------
# getInitTranstions
#
# Update the xmi model to add Initial Transitions from Transitions
# -----------------------------------------------------------------------  
def getInitTransitions(xmiModel: XmiModel):

    psuedoStateList = xmiModel.psuedoStateList
    transTargetSet = xmiModel.transTargets

    for trans in PreOrderIter(xmiModel.tree):
        if trans.name == "TRANSITION":
            # If the transition source is a psuedostate and no other transition goes into that psuedostate
            if (trans.source in psuedoStateList) and (trans.source not in transTargetSet):
                xmiModel.addInitial(trans)

# -----------------------------------------------------------------------
# getJunctions
#
# Update the xmi model to add Junctions
# -----------------------------------------------------------------------  
def getJunctions(xmiModel: XmiModel):

    for ps in PreOrderIter(xmiModel.tree):
        if ps.name == "PSUEDOSTATE":
            psId = ps.id
            transList = []
            for child in PreOrderIter(xmiModel.tree):
                # Get the transitions that exit this psuedo state
                if child.name == "TRANSITION":
                    if psId == child.source:
                        transList.append(child)
            if len(transList) == 2:
                xmiModel.addJunction(transList, ps)

# -----------------------------------------------------------------------
# moveTransitions
#
# Transitions that start from a state are to be moved under that state
# -----------------------------------------------------------------------  
def moveTransitions(xmiModel: XmiModel):
    for child in PreOrderIter(xmiModel.tree):
        if child.name == "TRANSITION": 
            # Look up where this transition is supposed to go
            state = xmiModel.idMap[child.source]
            # Move the transition under the source state
            xmiModel.moveTransition(child, state)

        if child.name == "JUNCTION":
            for sourceTransition in PreOrderIter(xmiModel.tree):
                if (sourceTransition.name == "TRANSITION") and (sourceTransition.target == child.id):
                    #state = xmiModel.idMap[parentState.source]
                    child.parent = sourceTransition.parent.parent
                    # Move the transition under the source state


def getStateMachineMethods(xmiModel: XmiModel):

    actionSet = set()
    guardSet = set()
    signalSet = set()

    for child in PreOrderIter(xmiModel.tree):
        #print(child.name)
        if child.name == "STATE":
            actionSet.add(getActionNames(child.entry, True))
            actionSet.add(getActionNames(child.exit, True))
        if child.name == "TRANSITION":
            actionSet.add(getActionNames(child.action, True))
            guardSet.add(getActionNames(child.guard, False))
            signalSet.add((child.event + getActionDataType(child.action)))
        if child.name == "JUNCTION":
            actionSet.add(getActionNames(child.ifAction, True))
            actionSet.add(getActionNames(child.elseAction, True))
            guardSet.add(child.guard)
        if child.name == "INITIAL":
            actionSet.add(getActionNames(child.action, True))

    # Remove empty strings
    actionSet = {item for item in actionSet if item}
    guardSet = {item for item in guardSet if item}
    signalSet = {item for item in signalSet if item}

    #for item in guardSet:
        #print("item: " + str(item))

    flatActions = {a.strip() for action in actionSet for a in action.split(',')}


    return (flatActions, guardSet, signalSet)

# -----------------------------------------------------------------------
# printFpp
#
# Print the FPP for state machine
# -----------------------------------------------------------------------  
def generateCode(xmiModel: XmiModel):

    #xmiModel.print()

    stateMachine = xmiModel.tree.stateMachine

    print ("Generating " + stateMachine + "_State_Machine.fpp")

    fppFile = open(stateMachine +"_State_Machine.fpp", "w")

    currentNode = xmiModel.tree

    getInitTransitions(xmiModel)

    getJunctions(xmiModel)

    (actions, guards, signals) = getStateMachineMethods(xmiModel)

    moveTransitions(xmiModel)

    xmiModel.print()

    fppFile.write(f"state machine {xmiModel.tree.stateMachine} {{\n\n")

    for action in sorted(actions):
        fppFile.write(f"  action {action}\n")
    fppFile.write("\n")

    for guard in sorted(guards):
        fppFile.write(f"  guard {guard}\n")
    fppFile.write("\n")

    for signal in sorted(signals):
        fppFile.write(f"  signal {signal}\n")
    fppFile.write("\n")
        
    processNode(currentNode, xmiModel, fppFile, 1)
    fppFile.write(f"}}\n")

    fppFile.close()



