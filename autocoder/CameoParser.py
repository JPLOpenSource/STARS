#!/usr/bin/env python3
# -----------------------------------------------------------------------
# CameoParser.py
#
# 
# -----------------------------------------------------------------------
# mypy: ignore-errors

from lxml import etree
from anytree import Node, RenderTree
import anytree
import sys
from copy import deepcopy
import xmiModelApi
import xmiToQm

# -------------------------------------------------------------------------
# createEventSignalMap
#
# Create a mapping of event id's to signal names and return the map
#
# --------------------------------------------------------------------------
def createEventSignalMap(xmlFileNodeModel, xmlFileNodeStateMachine):
    global XMI_ID

    eventToSignalMap = {}
    signalToNameMap = {}

    pe = xmlFileNodeModel.findall("packagedElement")
    for e in pe:
        if e.get(XMI_TYPE) == "uml:SignalEvent":
            eventToSignalMap[e.get(XMI_ID)] = e.get('signal')
        if e.get(XMI_TYPE) == "uml:Signal":
            signalToNameMap[e.get(XMI_ID)] =  e.get('name')

    nc = xmlFileNodeStateMachine.findall("nestedClassifier")
    for e in nc:
        if e.get(XMI_TYPE) == "uml:Signal":
            signalToNameMap[e.get(XMI_ID)] =  e.get('name')

    thisMap = {}
    for eventId in eventToSignalMap:
            signalId = eventToSignalMap[eventId]
            if signalId is not None:
                thisMap[eventId] = signalToNameMap[signalId]

    return thisMap

# -------------------------------------------------------------------------
# parseStateTree
#
# Recursively parse the xmi file root and populate the xmiModel
# --------------------------------------------------------------------------
def parseStateTree(xmlFileNode, xmiModelNode):
    global XMI_TYPE
    global XMI_ID
    global eventToNameMap

     # Get the Region
    region = xmlFileNode.find('region')
    if region is None:
        return

    # Get all the states
    vertexes = region.findall('subvertex')
    for v in vertexes:
        if v.get(XMI_TYPE) == "uml:State":
            state = v
            stateName = state.get('name')

            entry = state.find('entry')
            if entry is None:
                stateEntry = None
            else:
                stateEntry = entry.get('name')

            exit = state.find('exit')
            if exit is None:
                stateExit = None
            else:
                stateExit = exit.get('name')

            stateId = state.get(XMI_ID)
                
            thisNode = xmiModel.addState(stateName, xmiModelNode, stateEntry, stateExit, stateId)
            parseStateTree(state, thisNode)

        if v.get(XMI_TYPE) == "uml:Pseudostate":
            state = v
            stateId = state.get(XMI_ID)
            thisNode = xmiModel.addPsuedostate(stateId, xmiModelNode)

    transitions = region.findall('transition')
    for trans in transitions:
        sourceId = trans.get('source')
        targetId = trans.get('target')
        kind = trans.get('kind')

        # Get the Transition event
        trigger = trans.find('trigger')
        if trigger is not None and trigger.get('event') is not None:
            eventName = eventToNameMap[trigger.get('event')]
        else:
            eventName = None

        # Get the Transition guard
        ownedRule = trans.find('ownedRule')
        guardName = None
        if ownedRule is not None:
            guard = ownedRule.find('.//body')
            if guard is not None:
                guardName = guard.text

        # Get the Transition action
        effect = trans.find('effect')
        actionName = None
        if effect is not None:
            actionName = effect.get('name')

        kindName = None
        if kind is not None:
            kindName = kind
            
        thisNode = xmiModel.addTransition(sourceId, targetId, eventName, guardName, actionName, kindName, xmiModelNode)

    return   

# -------------------------------------------------------------------------
# populateXmiModel
#
# Recursively parse the input xml File nodes root and populate the xmiModel
# --------------------------------------------------------------------------
def populateXmiModel(xmlFileNode, xmiModel):
    global XMI_TYPE
    global XMI_ID
    global eventToNameMap

    stateMachine = getXmlStateMachine(xmlFileNode)

    eventToNameMap = createEventSignalMap(xmlFileNode, stateMachine)

    parseStateTree(stateMachine, xmiModel.getRoot())


#-----------------------------------------------------------------------
# getXmlFileNode
#
# Return the namespace and model element from the input xml file
# -----------------------------------------------------------------------
def getXmlFileNode(xmlfile):
    tree = etree.parse(xmlfile)
    root = tree.getroot()
    nsmap = root.nsmap
    doc = root.find('xmi:Documentation', nsmap)
    version = doc.find('xmi:exporterVersion', nsmap)
    print("MagicDraw version = {0}".format(version.text))

    # Get the Model
    model = root.find('uml:Model', nsmap)

    XMI_TYPE = "{"+nsmap['xmi']+"}type"

    return(nsmap, model)

# -----------------------------------------------------------------------------
# getXmlStateMachine
#
# Given the xml File element, find and return the uml:StateMachine xml element
# ------------------------------------------------------------------------------
def getXmlStateMachine(xmlFileNode):
    # Get the StateMachine node from the xml File.
    pe = xmlFileNode.findall("packagedElement")
    for e in pe:
        if e.get(XMI_TYPE) == "uml:StateMachine":
            return e 

# -----------------------------------------------------------------------
# getXmiModel
#
# Process the input CAMEO xmi and return an xmiModel
# -----------------------------------------------------------------------
def getXmiModel(xmlfile: str):
    global XMI_ID, XMI_TYPE, xmiModel
    print(f'Parsing file: {xmlfile}')
        
    (nsmap, xmlFileNode) = getXmlFileNode(xmlfile)

    XMI_ID = "{"+nsmap['xmi']+"}id"
    XMI_TYPE = "{"+nsmap['xmi']+"}type"

    #
    # Instantiate the xmi model
    #
    packageName = xmlFileNode.get('name')
    stateMachine = getXmlStateMachine(xmlFileNode)
    xmiModel = xmiModelApi.xmiModel(packageName, stateMachine.get('name'))

    # 
    # Populate the xmi model
    # 
    populateXmiModel(xmlFileNode, xmiModel)

    return xmiModel





            
        

