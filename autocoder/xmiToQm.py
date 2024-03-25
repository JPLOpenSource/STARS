#!/usr/bin/env python
# -----------------------------------------------------------------------
# xmiToQm.py
#
# 
# -----------------------------------------------------------------------
# mypy: ignore-errors

from lxml import etree
from anytree import Node, RenderTree
import anytree
import sys
from copy import deepcopy
import argparse
import xmiModelApi
import qmModelApi
from qmlib import ElementTreeType

#-----------------------------------------------------------------------
# translateXmiModelToQmFile
#
# -----------------------------------------------------------------------
def translateXmiModelToQmFile(xmiModel, debug) -> ElementTreeType:
    global qmModel

    #
    # Instantiate the qm model
    #
    (package, stateMachine) = xmiModel.getPackageAndStatMachineNames()
    qmModel = qmModelApi.qmModel(package, stateMachine)

    newNode = qmModel.getRoot()

    convertXmiToQmModel(xmiModel, qmModel)
            

    if debug:
        print("=> After convertXmiToQmModel")
        qmModel.print()

    return writeToXml(qmModel, debug)

#-----------------------------------------------------------------------
# convertXmiToQmModel
#
# Convert the xmi model to the qm model
# -----------------------------------------------------------------------
def convertXmiToQmModel(xmiModel, qmModel):
    global psList, stateList, transTargetList, psMapTran

    psList = xmiModel.getPsuedoStateList()

    stateList = xmiModel.getStatesList()

    transList = xmiModel.getTransitionsList()
    
    transTargetList = []
    for trans in transList:
        transTargetList.append(trans.target)

    psMapTran = mapPsuedoTransitions(psList, transList)

    
    copyXmiQmNodes(xmiModel.getRoot(), qmModel.getRoot())
    
    qmModel.assignAbsolutePositions()
    qmModel.makeRelativeTargets()

    return



#-----------------------------------------------------------------------
# mapPsuedoTransitions
#
# Return a map that maps psuedo state ID's with outgoing transitions
# -----------------------------------------------------------------------
def mapPsuedoTransitions(psList, transList):

    thisMap = {}
    class Choice:
        target = 0
        guard = None
        action = None

        def __init__(self, target, guard, action):
            self.target = target
            self.guard = guard
            self.action = action


    for psId in psList:
        # Check the psuedostate id in the transition source list
        outTransList = []
        for trans in transList:
            if trans.source == psId:
                outTransList.append(Choice(trans.target, trans.guard, trans.action))
        thisMap[psId] = outTransList

    return thisMap

#-----------------------------------------------------------------------
# copyXmiQmNodes
#
# Copy information from the xmi model to the qm model
# -----------------------------------------------------------------------
def copyXmiQmNodes(xmiModelNode, qmModelNode):
    global psList, stateList, transTargetList, psMapTran

    # First do states, then transitions
    for xmiNode in xmiModelNode.children:
        if xmiNode.name == "STATE":
            newNode = qmModel.addState(xmiNode.entry, xmiNode.exit, xmiNode.id, xmiNode.stateName, qmModelNode)
            copyXmiQmNodes(xmiNode, newNode) 

    for xmiNode in xmiModelNode.children: 
        if xmiNode.name == "TRANSITION":
                        
            # If the transition source is a psuedostate and no other transition goes into that psuedostate
            if (xmiNode.source in psList) and (xmiNode.source not in transTargetList):
                
                if xmiNode.target in stateList:
                    target = xmiNode.target
                else:
                    target = None

                newNode = qmModel.addInit(target, xmiNode.action, xmiNode.guard, xmiNode.event, qmModelNode)

                copyChoice(xmiNode.target, newNode)

            elif (xmiNode.source in stateList):
                
                # There are 6 cases when a transition source is a state:
                
                # Case 1:  Transition target is a state and not an internal transition and not a guard transition
                if (xmiNode.target in stateList) and (xmiNode.kind != "internal") and (xmiNode.guard is None):
                    qmModel.addTransition(xmiNode.source, xmiNode.target, xmiNode.action, xmiNode.guard, xmiNode.event)
                                    
                # Case 2:  Transition target is a state and is an internal transitions and is a guard transition 
                elif (xmiNode.target in stateList) and (xmiNode.kind == "internal") and (xmiNode.guard is not None):
                    newNode = qmModel.addTransition(xmiNode.source, None, None, None, xmiNode.event)
                    qmModel.addChoice(None, xmiNode.action, xmiNode.guard, newNode)
                    
                # Case 3:  Transition target is a state and is not an internal transitions and is a guard transition 
                elif (xmiNode.target in stateList) and (xmiNode.kind != "internal") and (xmiNode.guard is not None):
                    newNode = qmModel.addTransition(xmiNode.source, None, None, None, xmiNode.event)
                    qmModel.addChoice(xmiNode.target, xmiNode.action, xmiNode.guard, newNode)
                    
                # Case 4:  Transition target is a state and is an internal transition and not a guard transition
                elif (xmiNode.target in stateList) and (xmiNode.kind == "internal") and (xmiNode.guard is None):
                    qmModel.addTransition(xmiNode.source, None, xmiNode.action, xmiNode.guard, xmiNode.event)
                
                # Case 5:  Transition target is a psuedo state and not a guard transition
                elif (xmiNode.target not in stateList) and (xmiNode.guard is None):
                    newNode = qmModel.addTransition(xmiNode.source, None, xmiNode.action, xmiNode.guard, xmiNode.event)
                    copyChoice(xmiNode.target, newNode)

                
                # Case 6:  Transition target is a psuedo state and is a guard transition
                elif (xmiNode.target not in stateList) and (xmiNode.guard is not None):
                    newNode = qmModel.addTransition(xmiNode.source, None, None, None, xmiNode.event)
                    choiceNode = qmModel.addChoice(None, xmiNode.action, xmiNode.guard, newNode)
                    copyChoice(xmiNode.target, choiceNode)
                    
                else:
                    assert 0, "The transition does not fit into 1 of 5 cases"
                    
            else:
                pass

#-----------------------------------------------------------------------
# copyChoice
#
# Create a Choice node in the qmModel from a target
# -----------------------------------------------------------------------
def copyChoice(xmiModelTarget, qmModelNode):
    global psList, stateList, transTargetList, psMapTran

    if xmiModelTarget in psList:
        for choice in psMapTran[xmiModelTarget]:
            if choice.target in stateList:
                choiceNode = qmModel.addChoice(choice.target, choice.action, choice.guard, qmModelNode)
            else:
                choiceNode = qmModel.addChoice(None, choice.action, choice.guard, qmModelNode)
            copyChoice(choice.target, choiceNode)       

#-----------------------------------------------------------------------
# writeToXml
#
# Write out the qm xml file
# -----------------------------------------------------------------------
def writeToXml(qmModel, debug) -> ElementTreeType:

    root = etree.Element('model')
    package = etree.SubElement(root, 'package', name=qmModel.getPackageName())
    classTag = etree.SubElement(package, 'class', name=qmModel.getStateMachineName())
    statechart = etree.SubElement(classTag, 'statechart')

    writeTreeToXml(qmModel.getRoot(), statechart)

    if debug:
        print(etree.tostring(root, pretty_print=True).decode())

    return etree.ElementTree(root)

#-----------------------------------------------------------------------
# writeTreeToXml
#
# -----------------------------------------------------------------------
def writeTreeToXml(qmModelNode, xmlTag):

    for node in qmModelNode.children:
        if node.name == "STATE":
            state = etree.SubElement(xmlTag, 'state', name=node.stateName)
            if node.entry is not None:
                entry = etree.SubElement(state, 'entry', brief=node.entry)
            if node.exit is not None:
                exit = etree.SubElement(state, 'exit', brief=node.exit)
            writeTreeToXml(node, state)
        if node.name == "INIT":
            init = etree.SubElement(xmlTag, 'initial')
            if node.target is not None:
                init.attrib['target'] = node.target
            if node.action is not None:
                action = etree.SubElement(init, 'action', brief=node.action)
            writeTreeToXml(node, init)
        if node.name == "TRANSITION":
            if node.event == None:
                node.event = ""
            tran = etree.SubElement(xmlTag, 'tran', trig=node.event)
            if node.target is not None:
                tran.attrib['target'] = node.target
            if node.action is not None:
                action = etree.SubElement(tran, 'action', brief=node.action)
            writeTreeToXml(node, tran)
        if node.name == "CHOICE":
            choice = etree.SubElement(xmlTag, 'choice')
            if node.target is not None:
                choice.attrib['target'] = node.target
            if node.guard is not None:
                guard = etree.SubElement(choice, 'guard', brief=node.guard)
            if node.action is not None:
                action = etree.SubElement(choice, 'action', brief=node.action)
            writeTreeToXml(node, choice)
