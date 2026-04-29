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


def format_funcs(s: str, fullSpecifier: bool) -> str:
    if s is None:
        return None
    parts = [p.strip() for p in s.split(';') if p.strip()]
    result = []

    for part in parts:
        m = re.match(r'(\w+)\s*\(\s*(.*?)\s*\)', part)
        if not m:
            continue

        name, arg = m.groups()
        if arg and fullSpecifier:
            result.append(f"{name}: {arg}")
        else:
            result.append(name)

    return ", ".join(result)

def dedupe_events(values: set[str]) -> set[str]:
    best = {}

    for v in values:
        if ':' in v:
            name, arg = v.split(':', 1)
            best[name.strip()] = f"{name.strip()}: {arg.strip()}"
        else:
            name = v.strip()
            # only keep bare name if we haven't seen a version with arg
            best.setdefault(name, name)

    return set(best.values())

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

    # Separate children by type for consistent ordering
    initials = [child for child in node.children if child.name == "INITIAL"]
    junctions = [child for child in node.children if child.name == "JUNCTION"]
    transitions = [child for child in node.children if child.name == "TRANSITION"]
    states = [child for child in node.children if child.name == "STATE"]

    # Process INITIAL children (typically only one, maintain order)
    for child in initials:
        target = xmiModel.idMap[child.target].stateName
        doExpr = f" do {{ {format_funcs(child.action, False)} }}" if child.action else ""
        fppFile.write(f"{indent}initial{doExpr} enter {target}\n")

    # Process TRANSITION children in sorted order by event name for consistency
    for child in sorted(transitions, key=lambda t: t.event if t.event else ""):
        guardExpr = f" if {format_funcs(child.guard, False)}" if child.guard else ""
        enterExpr = f" enter {xmiModel.idMap[child.target].stateName}" if child.kind is None else ""
        doExpr = f" do {{ {format_funcs(child.action, False)} }}" if child.action else ""
        fppFile.write(f"{indent}on {child.event}{guardExpr}{doExpr}{enterExpr}\n")

    # Process STATE children in sorted (alphabetical) order for consistency
    for child in sorted(states, key=lambda s: s.stateName):
        stateName = child.stateName
        enterExpr = f" entry do {{ {format_funcs(child.entry, False)} }}" if child.entry else ""
        exitExpr = f" exit do {{ {format_funcs(child.exit, False)} }}" if child.exit else ""
        fppFile.write(f"{indent}state {stateName} {{\n")
        if enterExpr:
            fppFile.write(f"{indent}{enterExpr}\n")
        if exitExpr:
            fppFile.write(f"{indent}{exitExpr}\n")
        processNode(child, xmiModel, fppFile, level+1)
        fppFile.write(f"{indent}}}\n\n")

    # Process JUNCTION children last (maintain order, typically referenced by transitions)
    for child in junctions:
        ifTarget = xmiModel.idMap[child.ifTarget].stateName
        elseTarget = xmiModel.idMap[child.elseTarget].stateName
        doIfExpr = f" do {{ {format_funcs(child.ifAction, False)} }}" if child.ifAction else ""
        doElseExpr = f" do {{ {format_funcs(child.elseAction, False)} }}" if child.elseAction else ""
        fppFile.write(f"{indent}choice {child.stateName} {{\n")
        fppFile.write(f"{indent}  if {child.guard}{doIfExpr} enter {ifTarget} else{doElseExpr} enter {elseTarget}\n")
        fppFile.write(f"{indent}}}\n")
       
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
            actionSet.add(format_funcs(child.entry, True))
            actionSet.add(format_funcs(child.exit, True))
        if child.name == "TRANSITION":
            actionSet.add(format_funcs(child.action, True))
            guardSet.add(format_funcs(child.guard, False))
            signalSet.add((child.event + getActionDataType(child.action)))
        if child.name == "JUNCTION":
            actionSet.add(format_funcs(child.ifAction, True))
            actionSet.add(format_funcs(child.elseAction, True))
            guardSet.add(child.guard)
        if child.name == "INITIAL":
            actionSet.add(format_funcs(child.action, True))

    # Remove empty strings
    actionSet = {item for item in actionSet if item}
    guardSet = {item for item in guardSet if item}
    signalSet = {item for item in signalSet if item}

    flatActions = {a.strip() for action in actionSet for a in action.split(',')}


    return (flatActions, guardSet, dedupe_events(signalSet))

# -----------------------------------------------------------------------
# printFpp
#
# Print the FPP for state machine
# -----------------------------------------------------------------------  
def generateCode(xmiModel: XmiModel):

    stateMachine = xmiModel.tree.stateMachine

    print ("Generating " + stateMachine + "_State_Machine.fppi")

    fppFile = open(stateMachine +"_State_Machine.fppi", "w")

    currentNode = xmiModel.tree
 
    getInitTransitions(xmiModel)

    getJunctions(xmiModel)

    (actions, guards, signals) = getStateMachineMethods(xmiModel)

    moveTransitions(xmiModel)
    
    # Renumber junctions for consistent output across input formats
    junctions = [node for node in PreOrderIter(xmiModel.tree) if node.name == "JUNCTION"]
    for idx, junction in enumerate(sorted(junctions, key=lambda j: (j.parent.stateName if hasattr(j.parent, 'stateName') else "", j.guard or ""))):
        junction.stateName = f"J{idx}"

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



