#!/bin/env python3
# -----------------------------------------------------------------------
# checkFaults.py
# 
# Check for correct state-machine semantics
#
# -----------------------------------------------------------------------
# mypy: ignore-errors

import sys
import flattenstatemachine as flatt
import collections
import qmlib
from Cheetah.Template import Template
from qmlib import ElementTreeType


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# -----------------------------------------------------------------------
# MissingInit
# 
# An Exception class for missing initial transitions
#
# -----------------------------------------------------------------------
class MissingInit(Exception):
    message = """ Missing initial transition:  
    Add an initial transition to one of these states:  $stateList"""
    
    def __init__(self, states):
        self.states = states
        
    def __str__(self):
        template = Template(self.message)
        template.stateList = self.states
        return str(template)
       
        

# -----------------------------------------------------------------------
# MultipleInit
# 
# An Exception class for multiple initial transitions at the same level
#
# -----------------------------------------------------------------------
class MultipleInit(Exception):
    message = """ Multiple initial transitions:  
    Only 1 initial transition allowed on the same state-machine level.
    Remove one of the initial transitions to these states: $stateList"""
    
    def __init__(self, states):
        self.states = states
        
    def __str__(self):
        template = Template(self.message)
        template.stateList = self.states
        return str(template)
    
# -----------------------------------------------------------------------
# StateNames
# 
# An Exception class for state names that are not unique
#
# -----------------------------------------------------------------------
class StateNames(Exception):
    message = """ State names not unique:  
    Of these states: $stateList,
    Rename these states to be unique: $duplicates """
    
    def __init__(self, states, duplicates):
        self.states = states
        self.duplicates = duplicates
        
    def __str__(self):
        template = Template(self.message)
        template.stateList = self.states
        template.duplicates = self.duplicates
        return str(template)
    
# -----------------------------------------------------------------------
# GuardError
# 
# An Exception class for junctions with no guards
#
# -----------------------------------------------------------------------
class GuardError(Exception):
    message = """ Bad guard specification:  
    Transition $trigger, from state $state: Junction has no guard """ 
    
    def __init__(self, state, trigger):
        self.state = state
        self.trigger = trigger
        
    def __str__(self):
        template = Template(self.message)
        template.state = self.state
        template.trigger = self.trigger
        return str(template)
    
# -----------------------------------------------------------------------
# JunctionError
# 
# An Exception class for junctions with too many outgoing transitions
#
# -----------------------------------------------------------------------
class JunctionError(Exception):
    message = """ Junction transition error:  
    Transition $trigger, from state $state: Only 2 outgoing transitions from a junction is allowed""" 
    
    def __init__(self, state, trigger):
        self.state = state
        self.trigger = trigger
        
    def __str__(self):
        template = Template(self.message)
        template.state = self.state
        template.trigger = self.trigger
        return str(template)
    
# -----------------------------------------------------------------------
# JunctionGuardError
# 
# An Exception class for junctions with too many guards
#
# -----------------------------------------------------------------------
class JunctionGuardError(Exception):
    message = """ Junction Guard error:  
    Transition $trigger, from state $state: multiple guards detected, only 1 guard allowed from a junction""" 
    
    def __init__(self, state, trigger):
        self.state = state
        self.trigger = trigger
        
    def __str__(self):
        template = Template(self.message)
        template.state = self.state
        template.trigger = self.trigger
        return str(template)
    
# -----------------------------------------------------------------------
# EntryExitArg
# 
# An Exception class for entry and exit actions that have arguments
#
# -----------------------------------------------------------------------
class EntryExitArg(Exception):
    message = """ Entry/Exit action badly specified:  
    Entry/Exit function '$action' in state $state: Needs to be specified as: '<function_name>()' with no arguments""" 
    
    def __init__(self, state, action):
        self.state = state
        self.action = action
        
    def __str__(self):
        template = Template(self.message)
        template.state = self.state
        template.action = self.action
        return str(template)
    
# -----------------------------------------------------------------------
# ActionArg
# 
# An Exception class for actions with bad argument specifications
#
# -----------------------------------------------------------------------
class ActionArg(Exception):
    message = """ Action badly specified:  
    Action function '$action' from event $event: Needs to be specified as: '<function_name>([e])' """ 
    
    def __init__(self, event, action):
        self.event = event
        self.action = action
        
    def __str__(self):
        template = Template(self.message)
        template.event = self.event
        template.action = self.action
        return str(template)

# -----------------------------------------------------------------------
# BadEvent
# 
# An Exception class for transitions with badly specified Event
#
# -----------------------------------------------------------------------
class BadEvent(Exception):
    message = """ Transition has no Event:  
    The transition with action $action, has no Event """ 
    
    def __init__(self, trans):
        self.trans = trans
        
    def __str__(self):
        template = Template(self.message)
        actions = self.trans.iter('action')
        for action in actions:
            template.action = action.get('brief')
        return str(template)
    
# -----------------------------------------------------------------------
# initialTransition
# 
# Check for initial transition
#
# -----------------------------------------------------------------------
def initialTransition(qmRoot: ElementTreeType):
    states = qmRoot.findall('state')
    statesList = [state.get('name') for state in states]
        
    if len(states) == 0:
        return
    
    init = qmRoot.findall('initial')
    if len(init) == 0:
        raise MissingInit(statesList)
    
    if len(init) > 1:
        raise MultipleInit(statesList)
        
    for state in states:
        initialTransition(state)


# -----------------------------------------------------------------------
# dupList
# 
# Given a list, return a list of duplicate elements in the list.
#
# -----------------------------------------------------------------------
def dupList(a):
    return [item for item, count in collections.Counter(a).items() if count > 1]

        
# -----------------------------------------------------------------------
# stateNames
# 
# Check for unique state names
#
# -----------------------------------------------------------------------
def stateNames(qmRoot: ElementTreeType):
    states = qmRoot.iter("state")
        
    nameList = [state.get('name').upper() for state in states]
            
    dups = dupList(nameList)
    if len(dups) != 0:
        raise StateNames(nameList, dups)   
    
# --------------------------------------------------------------------------------------
# checkTransition
#
# Check for well specified transitions and guards
# --------------------------------------------------------------------------------------                   
def checkTransition(state, tran):
    
    # Target
    targetState = flatt.get_tran_target(tran)
    if targetState:
        return
    else:
        choices = tran.findall('choice')
        
        # Check for unguarded internal transitions - no junctions and no targets
        if len(choices) == 0:
            return
        
        # Transition through the junctions
        if len(choices) == 1:
            guard = choices[0].find('guard')
            if guard is None:
                raise GuardError(state.get('name'), tran.get('trig'))
            checkTransition(state, choices[0])

        elif len(choices) == 2:
            foundGuard = False
            for choice in choices:
                guard = choice.find('guard')
                if guard is not None:
                    if foundGuard == True:
                        raise JunctionGuardError(state.get('name'), tran.get('trig'))
                    foundGuard = True
                    ifChoice = choice
                else:
                    elseChoice = choice
            if not foundGuard:
                raise GuardError(state.get('name'), tran.get('trig'))
            
            checkTransition(state, ifChoice)
            checkTransition(state, elseChoice)
        else:
            raise JunctionError(state.get('name'), tran.get('trig'))

            
    return
                     
    
    
# -----------------------------------------------------------------------
# junctionGuards
# 
# Check that junctions have one and only one guard.
#
# -----------------------------------------------------------------------
def junctionGuards(qmRoot: ElementTreeType):
    states = qmRoot.iter("state")
    for state in states:
        trans = state.findall('tran')
        for tran in trans:
            checkTransition(state, tran)
        
# -----------------------------------------------------------------------
# checkEntryExitAction
# 
# Given the function string, check the arguments for entry or exit action 
# and raise expceptions
#
# -----------------------------------------------------------------------
def checkEntryExitAction(action, state):  
        if action is not None: 
            functions = action.split(';') 
            for function in functions:
                try:
                    s = function.index('(') + 1
                    e = function.index(')')
                except (ValueError):
                    raise EntryExitArg(state.get('name'), function)
    
                args = function[slice(s,e)]

                strippedArgs = args.strip(' ')
                if (strippedArgs != '') and (not strippedArgs.isnumeric()):
                    raise EntryExitArg(state.get('name'), function)

                
# -----------------------------------------------------------------------
# checkAction
# 
# Given the function string, check the arguments for transition action 
# and raise expceptions
#
# -----------------------------------------------------------------------
def checkAction(action, tran):  
        if action is not None: 
            functions = action.strip(';').split(';')
            for function in functions:
                try:
                    s = function.index('(') + 1
                    e = function.index(')')
                except (ValueError):
                    raise ActionArg(tran, function)
    
                args = function[slice(s,e)]
                strippedArgs = args.strip(' ')
                if (strippedArgs != '') and (not strippedArgs.isnumeric()) and (strippedArgs != 'e'):
                    raise ActionArg(tran, function)
            
# -----------------------------------------------------------------------
# entryExitArgs
# 
# Check that entry and exit actions are correctly specified
#
# -----------------------------------------------------------------------
def entryExitArgs(qmRoot: ElementTreeType):
    states = qmRoot.iter("state")
    for state in states:
        checkEntryExitAction(flatt.pick_entry(state), state)
        checkEntryExitAction(flatt.pick_exit(state), state)
        
# -----------------------------------------------------------------------
# actionArgs
# 
# Check that transition actions are correctly specified
#
# -----------------------------------------------------------------------
def actionArgs(qmRoot: ElementTreeType):
    trans = qmRoot.iter('tran')
    for tran in trans:
        actions = tran.iter('action')
        for action in actions:
            checkAction(action.get('brief'), tran.get('trig'))
    
# -----------------------------------------------------------------------
# checkEvents
# 
# Check that a transition has an event
#
# -----------------------------------------------------------------------
def checkEvents(qmRoot: ElementTreeType):
    trans = qmRoot.iter('tran')
    for tran in trans:
        if tran.get('trig').isspace() or not tran.get('trig'):
            raise BadEvent(tran)

# -----------------------------------------------------------------------
# checkStateMachine
# 
# Check the state-machine for valid semantics
#
# -----------------------------------------------------------------------
def checkStateMachine(qmRoot: ElementTreeType):
    qmRoot, smname = qmlib.get_state_machine(qmRoot)
    errorMessage = "\n*** Error parsing the state-machine: '{0}' ".format(smname)
    try:
        initialTransition(qmRoot)
        stateNames(qmRoot)
        junctionGuards(qmRoot)
        entryExitArgs(qmRoot)
        actionArgs(qmRoot)
        checkEvents(qmRoot)
        print("State-machine semantics look good")
    except (MissingInit, MultipleInit, StateNames, GuardError, JunctionError, EntryExitArg, JunctionGuardError, ActionArg, BadEvent) as Argument:
        print(bcolors.FAIL)
        print(errorMessage)
        print(bcolors.WARNING)
        print(Argument)
        print(bcolors.ENDC)
        sys.exit(0)
 
