#!/usr/bin/env python3
# -----------------------------------------------------------------------
# QmParser.py
#
# 
# -----------------------------------------------------------------------
# mypy: ignore-errors

from lxml import etree
from copy import deepcopy
import xmiModelApi
import flattenstatemachine as flatt
import qmlib
from anytree import Node
import sys
import xml.etree.ElementTree as ET


class UniqueNumberGenerator:
    def __init__(self):
        self.generator = self.unique_number_generator()  # Create a generator instance

    def unique_number_generator(self):
        counter = 0
        while True:
            yield counter
            counter += 1

    def get_unique_number(self):
        return next(self.generator)  # Return the next unique number

# -------------------------------------------------------------------------
# parseTrans
#
# Recursively parse a qm model and populate the xmiModel
# --------------------------------------------------------------------------
def parseTrans(qmModel, xmiModel, xmiNode, number_gen):
    source = xmiNode.id
    target = int(qmModel.get('target')) if qmModel.get('target') else None
    kind = qmModel.get('kind')  
    guard = qmlib.pick_guard(qmModel)
    action = flatt.pick_action(qmModel)
    event = qmModel.get('trig')

    if target is None:
        choices = qmModel.findall("choice")
        if len(choices) == 2:
            psId = number_gen.get_unique_number()
            psNode = xmiModel.addPsuedostate(psId)
            xmiModel.addTransition(source, psId, event, guard, action, kind)
            for choice in choices:
                parseTrans(choice, xmiModel, psNode, number_gen)
        else:
            xmiModel.addTransition(source, target, event, guard, action, kind)
            # targetArg = choices[0].get('target')
            # if targetArg is not None:
            #     target = int(targetArg)
            #     guard = qmlib.pick_guard(choices[0])
            #     action = qmlib.pick_action(choices[0])
            #     xmiModel.addTransition(source, target, event, guard, action, kind)
            # else:
            #     psId = number_gen.get_unique_number()
            #     psNode = xmiModel.addPsuedostate(psId)
            #     xmiModel.addTransition(source, psId, event, guard, action, kind)
            #     parseTrans(choices[0], xmiModel, psNode, number_gen)
    else:
        xmiModel.addTransition(source, target, event, guard, action, kind, xmiNode.parent)

# -------------------------------------------------------------------------
# parseStateTree
#
# Recursively parse the qm model and populate the xmiModel
# --------------------------------------------------------------------------
def parseStateTree(qmModel, xmiModel, xmiNode, number_gen):

    for init in qmModel.findall("initial"):
        psNode = xmiModel.addPsuedostate(number_gen.get_unique_number(), xmiNode)
        parseTrans(init, xmiModel, psNode, number_gen)

    for tran in qmModel.findall("tran"):
        parseTrans(tran, xmiModel, xmiNode, number_gen)

    for state in qmModel.findall("state"):
        stateName = state.get('name')
        entry = flatt.pick_entry(state)
        exit = flatt.pick_exit(state)
        state_id = int(state.get('id'))
        thisNode = xmiModel.addState(stateName, xmiNode, entry, exit, state_id)
        parseStateTree(state, xmiModel, thisNode, number_gen)
    
# -------------------------------------------------------------------------
# populateXmiModel
#
# Recursively parse the qm model and populate the xmiModel
# --------------------------------------------------------------------------
def populateXmiModel(qmModel, xmiModel, number_gen):
    # Add a unique ID to every state
    states = qmModel.iter("state")
    for state in states:
        state.set("id", str(number_gen.get_unique_number()))

    # Replace the relative target attributes with ID's
    for node in qmModel.iter():
        target = node.get("target")
        if target is not None:
            targetId = flatt.state_from_target(node).get("id")
            node.set("target", str(targetId))

    # Search for internal transitions.  Internal transitions do not have a 
    # target and do not have an option child.  Mark the transition as internal
    for tran in qmModel.iter("tran"):
        if tran.get('target') is None:
            # Look for choice nodes
            choices = list(tran.iter("choice"))
            if len(choices) == 0:
                tran.set("kind", "internal")

    parseStateTree(qmModel, xmiModel, xmiModel.tree, number_gen)

#-----------------------------------------------------------------------
# getXmlFileNode
#
# Return the etree model
# -----------------------------------------------------------------------
def getXmlFileNode(xmlfile):
    tree = etree.parse(xmlfile)
    root = tree.getroot()
    package = root.find('package')
    className = package.find('class')
    modelName = className.get('name')
    statemachine = className.find('statechart')
    return modelName, statemachine

        
# -----------------------------------------------------------------------
# fixQMThing
#
# The QM modeling tool does not support guards on transitions.
# These are specified in the xml file as a transition to a single
# choice.
#
# This routine makes a fix where it looks for transitions with a single
# choice and then adds the children directly under the transition,
# essentilly moving everything up.
# -----------------------------------------------------------------------
def fixQMThing(qmModel):
    for tran in qmModel.iter("tran"):
        choices = tran.findall("choice")
        if len(choices) == 1:

            choice_children = list(choices[0])

            for child in choice_children:
                tran.append(child)

            # Remove the <choice> node after moving its children 
            # But first check if the choice had a target attribute
            target = choices[0].get('target')
            if target is not None:
                tran.set('target', target)
            tran.remove(choices[0])

            # Look for all the targets and move them up as well.
            for child in list(tran.iter()):
                target = child.get('target')
                if target is not None:
                    child.set('target', target[3:])

    return qmModel


# -----------------------------------------------------------------------
# getXmiModel
#
# Process the input QM and return an xmiModel
# -----------------------------------------------------------------------
def getXmiModel(xmlfile: str):
    print(f'Parsing file: {xmlfile}')
    number_gen = UniqueNumberGenerator()
        
    modelName, qmModel = getXmlFileNode(xmlfile)

    qmModel = fixQMThing(qmModel)

    xml_string = ET.tostring(qmModel, encoding='unicode')
    print(xml_string)

    xmiModel = xmiModelApi.xmiModel(modelName + "Package", modelName)
   
    populateXmiModel(qmModel, xmiModel, number_gen)


    return xmiModel





            
        

