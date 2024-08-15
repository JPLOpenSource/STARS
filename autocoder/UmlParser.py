#!/usr/bin/env python
# --------------------------------------------------------------------------------------------------------------
# UmlParser.py
# Module Description:
# This module encapsulates a comprehensive toolkit for parsing PlantUML text that specifies hierachical
# state machines and converting them into QM models.  QM models are the XMI models used in the Quantum 
# Modeling state machine tool.  This module utilizes the `pyparsing` library.  The module defines a custom 
# UML syntax parser to interpret various UML elements like states, transitions, actions, and events. 
#
# ----------------------------------------------------------------------------------------------------------------

import pyparsing as pyparse
from pyparsing import Forward, Optional, delimitedList
from copy import deepcopy
import xmiModelApi
import xmiToQm
import os
import sys
from xmiModelApi import xmiModel
from qmlib import ElementTreeType
from pyparsing import ParserElement, ParseException
from typing import Dict, List

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


global_stateId = 1


# -------------------------------------------------------------------------------------------------------------------
# Function: handleError
#
# Description:
#   When an parsing error has been detected, this routine will print out the error message in color and
#   exit the program
# -------------------------------------------------------------------------------------------------------------------
def handleError(msg):
    print(bcolors.FAIL)
    print("Error processing PlantUML text:")
    print(bcolors.WARNING)
    print(msg)
    print(bcolors.ENDC)
    sys.exit(0)

# -------------------------------------------------------------------------------------------------------------------
# Function: createUmlSyntax
#
# Description: 
#   Creates a parser for a subset of UML syntax using pyparsing. The parser interprets elements like states,
#   transitions, actions, events, and guards within UML diagrams, particularly focusing on state machines. It
#   supports a textual representation of UML diagrams, allowing the parsing of elements marked with specific
#   syntax like @startuml, @enduml, states, transitions, actions, events, guards, entry/exit actions, internal
#   actions, and choice pseudostates.
#
# Returns:
#   ParserElement: A pyparsing ParserElement object, which can be used to parse and interpret UML diagrams
#   based on the defined syntax.
#
# Recognized Elements:
#   - @startuml/@enduml: Indicate the start and end of a UML diagram.
#   - States: Defined with alphanumeric characters and underscores.
#   - Transitions: Represented with arrows (-->, ->) and connect states.
#   - Actions: Specified after a colon and separated by semicolons for multiples.
#   - Events: Triggers for transitions, using alphanumeric characters and underscores.
#   - Guards: Conditions within square brackets, associated with transitions.
#   - Entry/Exit actions: Specified with 'Entry:' or 'Exit:' prefixes before actions.
#   - Internal actions: Actions within a state, prefixed with 'Internal:'.
#   - Choice pseudostates: Denoted with '<<choice>>' following a state name.
#
# --------------------------------------------------------------------------------------------------------------------
def createUmlSyntax() -> ParserElement:
    nameChars = pyparse.alphanums + "_"
    actionChars = pyparse.alphanums + "_" + "(" + ")"
    startUml = pyparse.Suppress(pyparse.Word("@startuml"))
    endUml = pyparse.Suppress(pyparse.Word("@enduml"))
    junction = pyparse.Suppress(pyparse.Word("[*]"))
    arrow = pyparse.Suppress(pyparse.Suppress(pyparse.Word("-->") | pyparse.Word('->')))
    colon = pyparse.Suppress(pyparse.Word(":"))
    function = pyparse.Combine(pyparse.Word(actionChars))
    guard = pyparse.Suppress(pyparse.Word('[')) + function.setResultsName('GUARD') + pyparse.Suppress(pyparse.Word(']'))
    prefix = pyparse.Literal('Entry:') | pyparse.Literal('Exit:')
    state = pyparse.Word(nameChars)
    event = pyparse.Word(nameChars)
    delim = pyparse.Suppress("/")
    actionList = delimitedList(function, delim=';').setResultsName('ACTION')
    action = delim + actionList

    initTrans = pyparse.Group(
        junction + 
        arrow + 
        state.setResultsName('STATE_NAME') +
        Optional(colon + action)
    ).setResultsName('INIT', True)

    internal = pyparse.Group(
        state.setResultsName('STATE_NAME') +
        colon +
        pyparse.Literal('Internal:') +
        Optional(event.setResultsName('EVENT')) +  
        Optional(guard) + 
        action
    ).setResultsName('INTERNAL', True)

    
    transBody = pyparse.Group(
        colon + 
        Optional(event.set_results_name('EVENT')) + 
        Optional(guard) + 
        Optional(action)
    ).setResultsName('BODY')

    transition = pyparse.Group(\
                     state.setResultsName('SOURCE') + \
                     arrow + \
                     state.setResultsName('TARGET') + \
                     Optional(transBody)
    ).setResultsName('TRANSITION', True)


    stateDef = pyparse.Group(\
                   state.setResultsName('STATE_NAME') + \
                   (colon + prefix.setResultsName('PREFIX') + actionList)
    ).setResultsName('STATE', True)

    compState = Forward()

    choiceState = pyparse.Group(\
                        pyparse.Word('state') + \
                        state.setResultsName('STATE_NAME') + \
                        pyparse.Literal('<<choice>>') \
    ).setResultsName('CHOICE', True)

    compState <<= pyparse.Group(
        pyparse.Word('state') +
        state +
        pyparse.nestedExpr('{', '}', content=initTrans | transition | internal | stateDef | choiceState | compState)
    ).setResultsName('COMP_STATE', True)

    totalSyntax = startUml + (initTrans | transition | internal | stateDef | choiceState | compState)[0,...] + endUml

    return totalSyntax

# ----------------------------------------------------------------------------------------------------
# Function: nodups
#
# Description: 
#   Removes duplicate elements from a list, maintaining the order of elements as they first appear.
#
# Parameters:
#   list (list): The list from which duplicates are to be removed.
#
# Returns:
#   list: A new list containing the elements from the input list but without any duplicates.
# ----------------------------------------------------------------------------------------------------
def nodups(list: List[str]) -> List[str]:
    thisList =[]
    for x in list:
        if x not in thisList:
            thisList.append(x)
            
    return thisList


# -------------------------------------------------------------------------------------------
# Function: createStateIdMap
#
# Description: 
#   Takes a list, generates a unique ID for each unique item, and maps each item to its ID.
#   It updates a global variable to the next available ID after assigning IDs.
#
# Parameters:
#   parseList (list): List from which unique items are extracted and assigned IDs.
#
# Returns:
#   dict: A dictionary mapping each unique item in parseList to a unique ID.
#
# Global variables:
#   global_stateId (int): Updated to the next available ID after the function executes.
# -------------------------------------------------------------------------------------------
def createStateIdMap(parseList: ParserElement) -> Dict[str, int]:
    global global_stateId

    stateList = []
    stateIdMap = {}
    createStateList(parseList, stateList)
    stateList = nodups(stateList)
    stateId = 1
    for state in stateList:
        stateIdMap[state] = stateId
        stateId = stateId + 1

    global_stateId = stateId
    return stateIdMap



# --------------------------------------------------------------------------------------------------------------
# Function: createStateList
#
# Description: 
#   Recursively traverses a structure of components and choices in parseList to extract states,
#   appending them to stateList. It ensures that stateList contains unique state names by removing
#   duplicates.
#
# Parameters:
#   parseList (object): Contains COMP_STATE and CHOICE attributes which are iterated over to extract states.
#   stateList (list): List to which the extracted state names are appended.
#
# Returns:
#   None: This function does not return a value but modifies stateList in place.
#
# Note:
#   This function is recursive and modifies stateList directly by appending new states and removing duplicates.
# --------------------------------------------------------------------------------------------------------------
def createStateList(parseList: ParserElement, stateList: List[str]):

    for comp in parseList.COMP_STATE:
        stateList.append(comp[1])
        createStateList(comp[2], stateList)

    for choice in parseList.CHOICE:
        stateList.append(choice.STATE_NAME)

    stateList = nodups(stateList)

    return

# --------------------------------------------------------------------------------------------------------------
# Function: createStateDefMap
#
# Description: 
#   Constructs a nested dictionary mapping state names to their corresponding entry and exit functions.
#   It iteratively traverses the structure in parseList, identifying entry and exit actions for states
#   and updating the map accordingly.
#
# Parameters:
#   parseList (object): Contains COMP_STATE attributes used to extract state names and actions.
#   thisMap (dict): The map that is updated with state names as keys and dictionaries as values,
#                   where each dictionary contains 'entry' and 'exit' keys mapping to their respective functions.
#
# Returns:
#   None: This function does not return a value but modifies thisMap in place.
#
# Note:
#   The function is recursive and modifies thisMap directly, adding new states and their associated entry
#   and exit functions.
# -------------------------------------------------------------------------------------------------------------
def createStateDefMap(parseList: ParserElement, thisMap:  Dict[str, Dict[str, str]]):
    '''
    Returns nested map.
    {STATE_NAME: {'entry': entryFunc, 'exit': exitFunc}}
    '''
    for comp in parseList.COMP_STATE:
        stateName = comp[1]
        entryFunc = None
        exitFunc = None
        thisMap[stateName] = {'entry': None, 'exit': None, 'internal': None}
        for state in comp[2].STATE:
            if state.PREFIX == 'Entry:':
                entryFunc = ";".join(state.ACTION)
            elif state.PREFIX == "Exit:":
                exitFunc = ";".join(state.ACTION)
            if state.STATE_NAME != stateName:
                handleError(f"In the composition state {stateName}, state {state.STATE_NAME} is unexpected.")

        for intern in comp[2].INTERNAL:
            if intern.STATE_NAME != stateName:
                handleError(f"In the composition state {state.STATE_NAME}, state {intern.STATE_NAME} is unexpected.")

        thisMap[stateName]['entry'] = entryFunc
        thisMap[stateName]['exit'] = exitFunc
        createStateDefMap(comp[2], thisMap)

    return

# ----------------------------------------------------------------------------------------------------------------
# Function: createXmi
#
# Description: 
#   Iteratively builds an XMI (XML Metadata Interchange) model by adding states, transitions, and pseudostates
#   based on the parsed list. It assigns IDs, entry, and exit actions to states, and details transitions with
#   event, guard, and action. The function updates a global state ID.
#
# Parameters:
#   parseList (object): Contains COMP_STATE, INIT, CHOICE, and TRANSITION attributes to build the XMI structure.
#   model (object): The XMI model object to which elements are added.
#   root (object): The root node in the XMI model.
#   stateIdMap (dict): A mapping of state names to their corresponding IDs.
#   stateFunctions (dict): A mapping of state names to their entry and exit functions.
#
# Global Variables:
#   global_stateId (int): Used for assigning unique IDs, updated throughout the function.
#
# Returns:
#   None: This function does not return a value but builds the XMI model by modifying the 'model' object.
# ----------------------------------------------------------------------------------------------------------------
def createXmi(parseList: ParserElement, model: xmiModel, root: xmiModel, stateIdMap: Dict[str, int], stateFunctions: Dict[str, Dict[str, str]]):
    global global_stateId

    # Add states to the XMI
    for comp in parseList.COMP_STATE:
        state = comp[1]
        id = stateIdMap[state]
        entry = stateFunctions[state]['entry']
        exit = stateFunctions[state]['exit']
        newNode = model.addState(state, root, entry, exit, id)
        createXmi(comp[2], model, newNode, stateIdMap, stateFunctions)

    # Add initial transition to the XMI
    for init in parseList.INIT:
        action = None
        if len(init.ACTION) != 0:
            action = ";".join(init.ACTION)
        model.addPsuedostate(global_stateId, root)
        model.addTransition(global_stateId,  # source 
                            stateIdMap[init.STATE_NAME], # target
                            None, # event
                            None, # guard
                            action, # action
                            None, # kind
                            root)
        global_stateId = global_stateId + 1        

    for choice in parseList.CHOICE:
        model.addPsuedostate(stateIdMap[choice.STATE_NAME], root)

    for internal in parseList.INTERNAL:
        if "GUARD" not in internal:
            guard = None
        else:
            guard = internal.GUARD
        action = ";".join(internal.ACTION)
        model.addTransition(stateIdMap[internal.STATE_NAME], 
                                stateIdMap[internal.STATE_NAME],
                                internal.EVENT,
                                guard,
                                action,
                                "internal",
                                root)


    # Add transitions to the XMI
    for trans in parseList.TRANSITION:
        
        if "EVENT" not in trans.BODY:
            event = None
        else:
            event = trans.BODY.EVENT

        if "GUARD" not in trans.BODY:
            guard = None
        else:
            guard = trans.BODY.GUARD

        if "ACTION" not in trans.BODY:
            action = None
        else:
            action = ";".join(trans.BODY.ACTION)

        model.addTransition(stateIdMap[trans.SOURCE], 
                                stateIdMap[trans.TARGET],
                                event, # event 
                                guard, # guard
                                action, # action
                                None, # kind
                                root)

# ----------------------------------------------------------------------------------------------------------------
# Function: getXmiModel
#
# Description: 
#   Parses a UML (Unified Modeling Language) file to create an XMI (XML Metadata Interchange) model.
#   The function sets up parsing rules, processes the UML file, generates state IDs, defines state functions, 
#   and constructs the XMI model.
# ----------------------------------------------------------------------------------------------------------------
def getXmiModel(umlFileName: str):
    global XMI_ID, XMI_TYPE
    print(f'Parsing file: {umlFileName}')
    
    comment = pyparse.Literal("'") + pyparse.restOfLine
    umlSyntax = createUmlSyntax().ignore(comment)

    umlFile = open(umlFileName, 'r')
        
    parseResults = umlSyntax.parseFile(umlFile)

    modelName = os.path.splitext(umlFileName)[0].split('/')[-1]
    
    xmiModel = xmiModelApi.xmiModel(modelName + "Package", modelName)
    
    stateIdMap = createStateIdMap(parseResults)

    stateFunctions = {}
    createStateDefMap(parseResults, stateFunctions)
   
    try:

        createXmi(parseResults, xmiModel, xmiModel.getRoot(), stateIdMap, stateFunctions)

    except KeyError as error:
        handleError(f"State {error.args[0]} has not been defined")

    return xmiModel
    




            
        

