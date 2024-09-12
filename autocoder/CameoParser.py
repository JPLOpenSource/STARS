#!/usr/bin/env python3
# -----------------------------------------------------------------------
# CameoParser.py
#
# 
# -----------------------------------------------------------------------
# mypy: ignore-errors

from anytree import Node
from copy import deepcopy
import xmiModelApi
from typing import Tuple, Dict


from lxml.etree import _ElementTree
ElementTreeType = _ElementTree 
from xmiModelApi import XmiModel



# -------------------------------------------------------------------------
# createEventSignalMap
#
# Create a mapping of event id's to signal names and return the map
#
# --------------------------------------------------------------------------
def createEventSignalMap(xmlFileNodeModel: ElementTreeType, 
                         xmlFileNodeStateMachine: ElementTreeType):
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
def parseStateTree(xmlFileNode: ElementTreeType, 
                   xmiModelNode: Node):
    
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
def populateXmiModel(xmlRoot: ElementTreeType, xmiModel: XmiModel):

    global XMI_TYPE
    global XMI_ID
    global eventToNameMap

    smRoot: ElementTreeType = getXmlStateMachine(xmlRoot)

    eventToNameMap = createEventSignalMap(xmlRoot, smRoot)

    parseStateTree(smRoot, xmiModel.getRoot())


#-----------------------------------------------------------------------
# getXmlFileNode
#
# Return the namespace and model element from the input xml file
# -----------------------------------------------------------------------
def getXmlFileNode(cameoRoot: ElementTreeType) -> Tuple[Dict[str, str], ElementTreeType]:

    root = cameoRoot.getroot()
    nsmap = root.nsmap
    doc = root.find('xmi:Documentation', nsmap)
    version = doc.find('xmi:exporterVersion', nsmap)
    print("MagicDraw version = {0}".format(version.text))

    # Get the Model
    xmlRoot = root.find('uml:Model', nsmap)

    XMI_TYPE = "{"+nsmap['xmi']+"}type"

    return(nsmap, xmlRoot)

# -----------------------------------------------------------------------------
# getXmlStateMachine
#
# Given the xml File element, find and return the uml:StateMachine xml element
# ------------------------------------------------------------------------------
def getXmlStateMachine(xmlRoot: ElementTreeType) -> ElementTreeType:

    # Get the StateMachine node from the xml File.
    pe = xmlRoot.findall("packagedElement")
    for e in pe:
        if e.get(XMI_TYPE) == "uml:StateMachine":
            return e 

# -----------------------------------------------------------------------
# fixComplexIDs
#
# -----------------------------------------------------------------------
def fixComplexIDs(cameoRoot: ElementTreeType):

    idMap = {}
    simpleId = 0
    for element in cameoRoot.iter():
            if element.tag == "subvertex":
                umlType = element.get(XMI_TYPE)
                id = element.get(XMI_ID)
                if umlType in ["uml:State", "uml:Pseudostate"]:
                    idMap[id] = simpleId
                    simpleId += 1

    # Second pass: Update the XML tree with new IDs
    for element in cameoRoot.iter():
        if element.tag == "subvertex":
            umlType = element.get(XMI_TYPE)
            id = element.get(XMI_ID)
            if umlType in ["uml:State", "uml:Pseudostate"]:
                element.set(XMI_ID, str(idMap[id]))
        if element.tag == "transition":
            source = element.get('source')
            target = element.get('target')
            # Only set source and target if they exist in idMap to avoid KeyErrors
            if source in idMap:
                element.set('source', str(idMap[source]))
            if target in idMap:
                element.set('target', str(idMap[target]))

# -----------------------------------------------------------------------
# getXmiModel
#
# Process the input CAMEO xmi and return an xmiModel
# -----------------------------------------------------------------------
def getXmiModel(cameoRoot: ElementTreeType) -> XmiModel:
    
    global XMI_ID, XMI_TYPE, xmiModel

    (nsmap, xmlRoot) = getXmlFileNode(cameoRoot)

    XMI_ID = "{"+nsmap['xmi']+"}id"
    XMI_TYPE = "{"+nsmap['xmi']+"}type"

    # The Cameo file has some very long ID's
    # Change the ID's to simple unique integers
    fixComplexIDs(cameoRoot)

    #
    # Instantiate the xmi model
    #
    packageName = xmlRoot.get('name')
    smRoot = getXmlStateMachine(xmlRoot)
    xmiModel = xmiModelApi.XmiModel(packageName, smRoot.get('name'))

    # 
    # Populate the xmi model
    # 
    populateXmiModel(xmlRoot, xmiModel)

    return xmiModel
        

