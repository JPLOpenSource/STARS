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
        escaped_name = escape_fpp_keyword(name)
        if arg and fullSpecifier:
            result.append(f"{escaped_name}: {arg}")
        else:
            result.append(escaped_name)

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
# escape_fpp_keyword
#
# Escape FPP reserved keywords to avoid syntax errors.
# -----------------------------------------------------------------------
def escape_fpp_keyword(name: str) -> str:
    """
    Escape FPP reserved keywords by appending '_state' suffix.
    FPP reserved keywords are case-sensitive and include: on, state, initial, 
    choice, if, else, do, enter, exit, entry, signal, action, guard, etc.
    """
    fpp_keywords = {
        'on', 'state', 'initial', 'choice', 'if', 'else', 
        'do', 'enter', 'exit', 'entry', 'signal', 'action', 'guard'
    }
    
    if name in fpp_keywords:
        return f"{name}_state"
    return name

# -----------------------------------------------------------------------
# get_qualified_target
#
# Get the qualified target name for a transition.
# Returns just the stateName if target is at same level or up the hierarchy,
# otherwise returns qualified path (e.g., Parent.Child) when going down.
# -----------------------------------------------------------------------
def get_qualified_target(source_node: Node, target_id, xmiModel: XmiModel) -> str:
    target_node = xmiModel.idMap[target_id]
    target_name = target_node.stateName
    
    # Build list of ancestors from source to root
    source_ancestors = []
    node = source_node
    while node is not None:
        source_ancestors.append(node)
        node = node.parent
    
    # Build list of ancestors from target to root
    target_ancestors = []
    node = target_node
    while node is not None:
        target_ancestors.append(node)
        node = node.parent
    
    # Find common ancestor
    common_ancestor = None
    for s_anc in source_ancestors:
        if s_anc in target_ancestors:
            common_ancestor = s_anc
            break
    
    # Build qualified path from common ancestor down to target
    path = []
    node = target_node
    while node != common_ancestor and node is not None:
        if hasattr(node, 'stateName'):
            path.insert(0, escape_fpp_keyword(node.stateName))
        node = node.parent
    
    # If path has more than one element, we need qualified notation
    if len(path) > 1:
        return ".".join(path)
    else:
        return escape_fpp_keyword(target_name)

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
        qualified_target = get_qualified_target(node, child.target, xmiModel)
        doExpr = f" do {{ {format_funcs(child.action, False)} }}" if child.action else ""
        fppFile.write(f"{indent}initial{doExpr} enter {qualified_target}\n")

    # Process STATE children first (in sorted alphabetical order) to avoid forward references
    for child in sorted(states, key=lambda s: s.stateName):
        stateName = escape_fpp_keyword(child.stateName)
        enterExpr = f" entry do {{ {format_funcs(child.entry, False)} }}" if child.entry else ""
        exitExpr = f" exit do {{ {format_funcs(child.exit, False)} }}" if child.exit else ""
        fppFile.write(f"{indent}state {stateName} {{\n")
        if enterExpr:
            fppFile.write(f"{indent}{enterExpr}\n")
        if exitExpr:
            fppFile.write(f"{indent}{exitExpr}\n")
        processNode(child, xmiModel, fppFile, level+1)
        fppFile.write(f"{indent}}}\n\n")

    # Process TRANSITION children after states (in sorted order by event name for consistency)
    for child in sorted(transitions, key=lambda t: t.event if t.event else ""):
        guardExpr = f" if {format_funcs(child.guard, False)}" if child.guard else ""
        if child.kind is None:
            qualified_target = get_qualified_target(node, child.target, xmiModel)
            enterExpr = f" enter {qualified_target}"
        else:
            enterExpr = ""
        doExpr = f" do {{ {format_funcs(child.action, False)} }}" if child.action else ""
        fppFile.write(f"{indent}on {child.event}{guardExpr}{doExpr}{enterExpr}\n")

    # Process JUNCTION children last (maintain order, typically referenced by transitions)
    for child in junctions:
        ifTarget = get_qualified_target(node, child.ifTarget, xmiModel)
        elseTarget = get_qualified_target(node, child.elseTarget, xmiModel)
        doIfExpr = f" do {{ {format_funcs(child.ifAction, False)} }}" if child.ifAction else ""
        doElseExpr = f" do {{ {format_funcs(child.elseAction, False)} }}" if child.elseAction else ""
        guardExpr = format_funcs(child.guard, False) if child.guard else child.guard
        junctionName = escape_fpp_keyword(child.stateName)
        fppFile.write(f"{indent}choice {junctionName} {{\n")
        fppFile.write(f"{indent}  if {guardExpr}{doIfExpr} enter {ifTarget} else{doElseExpr} enter {elseTarget}\n")
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
            guardSet.add(format_funcs(child.guard, True))
            signalSet.add((child.event + getActionDataType(child.action)))
        if child.name == "JUNCTION":
            actionSet.add(format_funcs(child.ifAction, True))
            actionSet.add(format_funcs(child.elseAction, True))
            guardSet.add(format_funcs(child.guard, True))
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
        escaped_action = escape_fpp_keyword(action.split(':')[0].strip()) + (f": {action.split(':', 1)[1].strip()}" if ':' in action else "")
        fppFile.write(f"  action {escaped_action}\n")
    fppFile.write("\n")

    for guard in sorted(guards):
        escaped_guard = escape_fpp_keyword(guard.split(':')[0].strip()) + (f": {guard.split(':', 1)[1].strip()}" if ':' in guard else "")
        fppFile.write(f"  guard {escaped_guard}\n")
    fppFile.write("\n")

    for signal in sorted(signals):
        escaped_signal = escape_fpp_keyword(signal.split(':')[0].strip()) + (f": {signal.split(':', 1)[1].strip()}" if ':' in signal else "")
        fppFile.write(f"  signal {escaped_signal}\n")
    fppFile.write("\n")
        
    processNode(currentNode, xmiModel, fppFile, 1)
    fppFile.write(f"}}\n")

    fppFile.close()



