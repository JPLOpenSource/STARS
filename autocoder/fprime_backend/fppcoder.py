#!/bin/env python3
# -----------------------------------------------------------------------
# fppcoder.py
#
# From an xmiModel, translate to a FPP state machine
# -----------------------------------------------------------------------
from anytree import Node, PreOrderIter
import re

def getActionNames(input_string):
    # Use regex to find all procedural names before the '(' and ignore everything after
    procedural_names = re.findall(r'\b\w+(?=\()', input_string)
    # Join the names with commas
    output_string = ', '.join(procedural_names)
    return output_string


def processNode(node, model, fppFile, level = 0):
    indent = "  " * level

    for child in node.children:

        if child.name == "INITIAL":
            target = model.idMap[child.target].stateName
            doExpr = f" do {{ {getActionNames(child.action)} }}" if child.action else ""
            fppFile.write(f"{indent}initial{doExpr} enter {target}\n")

        if child.name == "JUNCTION":
            ifTarget = model.idMap[child.ifTarget].stateName
            elseTarget = model.idMap[child.elseTarget].stateName
            doIfExpr = f" do {{ {getActionNames(child.ifAction)} }}" if child.ifAction else ""
            doElseExpr = f" do {{ {getActionNames(child.elseAction)} }}" if child.elseAction else ""
            fppFile.write(f"{indent}junction {child.stateName} {{\n")
            fppFile.write(f"{indent}  if {getActionNames(child.guard)}{doIfExpr} enter {ifTarget} \\\n")
            fppFile.write(f"{indent}  else{doElseExpr} enter {elseTarget}\n")
            fppFile.write(f"{indent}}}\n")

        if child.name == "TRANSITION":
            guardExpr = f" if {getActionNames(child.guard)}" if child.guard else ""
            enterExpr = f" enter {model.idMap[child.target].stateName}" if child.kind is None else ""
            doExpr = f" do {{ {getActionNames(child.action)} }}" if child.action else ""
            fppFile.write(f"{indent}on {child.event}{guardExpr}{doExpr}{enterExpr}\n")

        if child.name == "STATE":
            stateName = child.stateName
            enterExpr = f" entry do {{ {getActionNames(child.entry)} }}" if child.entry else ""
            exitExpr = f" exit do {{ {getActionNames(child.exit)} }}" if child.exit else ""
            fppFile.write(f"{indent}state {stateName} {{\n")
            if enterExpr:
                fppFile.write(f"{indent}{enterExpr}\n")
            if exitExpr:
                fppFile.write(f"{indent}{exitExpr}\n")
            processNode(child, model, fppFile, level+1)
            fppFile.write(f"{indent}}}\n")
       
# -----------------------------------------------------------------------
# getInitTranstions
#
# Update the xmi model to add Initial Transitions from Transitions
# -----------------------------------------------------------------------  
def getInitTransitions(model):
    psuedoStateList = model.psuedoStateList
    transTargetSet = model.transTargets

    for trans in PreOrderIter(model.tree):
        if trans.name == "TRANSITION":
            # If the transition source is a psuedostate and no other transition goes into that psuedostate
            if (trans.source in psuedoStateList) and (trans.source not in transTargetSet):
                model.addInitial(trans)

# -----------------------------------------------------------------------
# getJunctions
#
# Update the xmi model to add Junctions
# -----------------------------------------------------------------------  
def getJunctions(model):

    for ps in PreOrderIter(model.tree):
        if ps.name == "PSUEDOSTATE":
            psId = ps.id
            transList = []
            for child in PreOrderIter(model.tree):
                # Get the transitions that exit this psuedo state
                if child.name == "TRANSITION":
                    if psId == child.source:
                        transList.append(child)
            assert len(transList) == 2, f"{len(transList)} transitions found, expected 2"
            model.addJunction(transList, ps)

# -----------------------------------------------------------------------
# moveTransitions
#
# Transitions that start from a state are to be moved under that state
# -----------------------------------------------------------------------  
def moveTransitions(model):
    for trans in PreOrderIter(model.tree):
        if trans.name == "TRANSITION":
            # Look up where this transition is supposed to go
            state = model.idMap[trans.source]
            # Move the transition under the source state
            model.moveTransition(trans, state)


# -----------------------------------------------------------------------
# printFpp
#
# Print the FPP for state machine
# -----------------------------------------------------------------------  
def generateCode(xmiModel):
    stateMachine = xmiModel.tree.stateMachine
    
    print ("Generating " + stateMachine + ".fpp")

    fppFile = open(stateMachine +".fpp", "w")

    currentNode = xmiModel.tree

    getInitTransitions(xmiModel)

    getJunctions(xmiModel)

    moveTransitions(xmiModel)

    fppFile.write(f"state machine {xmiModel.tree.stateMachine} {{\n")
    processNode(currentNode, xmiModel, fppFile, 1)
    fppFile.write(f"}}\n")

    fppFile.close()



