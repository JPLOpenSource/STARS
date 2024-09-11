#!/bin/env python

from copy import deepcopy
from lxml import etree
from qmlib import ElementTreeType
from typing import List, Tuple, Optional, Any
import qmlib
import sys



# ----------------------------------------------------------------------------
# leaf_states_inherit
#
# Iterate through all the transitions in the model and mark the local
# and self transitions with tags.
#
# Then go through all the leaf states and add transitions from their parents.
# ----------------------------------------------------------------------------
def leaf_states_inherit(root: ElementTreeType):

    # Go through all the transitions and mark those that are local and self
    trans = root.iter('tran')
    for tran in trans:
        # Mark the transition with local flag
        tran.set('local', str(is_local_transition(tran)))
        
        # Mark the transitions with self flag
        mark_self_transition(tran)
        
    inherit_parent(root) 


# -----------------------------------------------------------------------
# inherit_parent
#
# For a given state, recursively inherit the transitions from its parent
# -----------------------------------------------------------------------
def inherit_parent(root: ElementTreeType):
    parent = root.getparent()
    if parent.tag == 'state':
        parentTrans = parent.findall('tran')
        stateTrans = root.findall('tran')
        stateSigList = []
        for tran in stateTrans:
            stateSigList.append(tran.get('trig'))
        for parentTran in parentTrans:
            if parentTran.get('trig') not in stateSigList:
                # Add a new trigger node to root with one deeper layer
                inheritTran = deepcopy(parentTran)
                target = inheritTran.get('target')
                               
                if target is not None:
                    inheritTran.set('target', '../' + target)
                else:
                    inheritTran = flatten_tran_choices(inheritTran)
                root.append( inheritTran )

        
    states = root.findall('state')
    for state in states:
        inherit_parent(state)

# -----------------------------------------------------------------------
# flatten_tran_choices
#
# For a transition with choices, add the depth to all the targets
# -----------------------------------------------------------------------
def flatten_tran_choices(tran: ElementTreeType) -> ElementTreeType:
    # Recursively find all the choice tags
    choices = tran.findall('.//choice')
    for choice in choices:
        target = choice.get('target')
        if target is not None:
            choice.set('target', '../' + target)
    return tran



# -----------------------------------------------------------------------
# is_local_transition
#
# Before flattening the state machine, check for transitions that are 
# local.  
# Receives a transition element and returns True or False
#
# The signature for a local transition is: '../..' 
# The signature for a self transition is '..'
# The signature for a regular transition is '../../5'
# 
# This routine only checks for the local transition signature
# 
# -----------------------------------------------------------------------
def is_local_transition(tran: ElementTreeType) -> bool:
    target = tran.get('target')
    if target is not None:
        # Check for self transition
        if target == "..":
            return False
        elif target.split('/')[-1].isdigit():
            return False
        else: 
            return True
    else:
        return False


# -----------------------------------------------------------------------
# self_transition
#
# Returns True if the transition is a self transition
# -----------------------------------------------------------------------
def self_transition(tran: ElementTreeType) -> bool:
    # Go up the tree until you hit a state tag
    # Then get the transition target and follow it up,
    # If we reach the same state then it's a self transition.
    thisState = get_this_state(tran)
    if thisState is None:
        return False

    targetState = get_tran_target(tran)
    
    if thisState == targetState:
        return True
    else:
        return False


# -----------------------------------------------------------------------
# get_tran_target
#
# Input argument is a transition.
# Parse the QM transition and return the name of the target state 
# -----------------------------------------------------------------------
def get_tran_target(tran: ElementTreeType) -> Optional[str]:    
    target = tran.get('target')
    if target is None:
        return target
    else:
        root = tran
        for i in target.split('/'):
            if i == "..":
                root = root.getparent()
            else:
                state = get_state_from_index(root, int(i))                                   
                root = state
                
    return root.get('name')

# -----------------------------------------------------------------------
# get_this_state
#
# Go up the tree until you find a tag called 'state', then return the name
# -----------------------------------------------------------------------
def get_this_state(tran: ElementTreeType) -> Optional[str]:
    if tran is None:
        return None
    if tran.tag == 'state':
        return tran.get('name')
    else:
        return get_this_state(tran.getparent())


# -----------------------------------------------------------------------
# get_state_from_index
#
# Given a root and an index, return the state that matches the index
# -----------------------------------------------------------------------
        
def get_state_from_index(root: ElementTreeType, index: int) -> ElementTreeType:
    count = 0
    for child in root:
        if child.tag == 'state' or child.tag == 'tran':
            count = count + 1
            if index == count:
                assert child.tag == 'state'
                return child
    assert 0


# -----------------------------------------------------------------------
# mark_self_transition
#
# Recursively go down a transition and mark all transitions (including 
# choices with a self flag for transitions that are self transitions.
# 
# -----------------------------------------------------------------------   
def mark_self_transition(tran: ElementTreeType):
    targetState = get_tran_target(tran)
    if targetState is not None:
        if self_transition(tran):
            tran.set('self', 'True')
    else:
        choices = tran.findall('choice')
        for choice in choices:
            mark_self_transition(choice)

# -----------------------------------------------------------------------
# state_from_target
#
# From a given transition, return the target state
# -----------------------------------------------------------------------
def state_from_target(tran: ElementTreeType) -> ElementTreeType:
    target = tran.get('target')
    if target is None:
        return tran.getparent()
    else:
        root = tran
        for i in target.split('/'):
            if i == "..":
                root = root.getparent()
            else:
                root = get_state_from_index(root, int(i))
    return root

# -----------------------------------------------------------------------
# pick_action
#
# Input is QM xml tags
# Return the action function
# -----------------------------------------------------------------------
def pick_action(tag: ElementTreeType) -> Optional[str]:
    action = tag.find('action')
    if action is not None:
        brief = action.get('brief').strip(';')
        return brief

    else:
        return None

# -----------------------------------------------------------------------
# pick_entry
#
# Input is QM xml tags
# Return the entry function
# -----------------------------------------------------------------------
def pick_entry(tag: ElementTreeType) -> Optional[str]:
    action = tag.find('entry')
    if action is not None:
        brief = action.get('brief').strip(';')
        return brief
    else:
        return None

# -----------------------------------------------------------------------
# pick_exit
#
# Input is QM xml tags
# Return the exit function
# -----------------------------------------------------------------------
def pick_exit(tag: ElementTreeType) -> Optional[str]:
    action = tag.find('exit')
    if action is not None:
        brief = action.get('brief').strip(';')
        return brief
    else:
        return None
    
# -----------------------------------------------------------------------
# pick_init
#
# Input is QM xml tags
# Return the initial transition action function
# -----------------------------------------------------------------------
def pick_init(tag: ElementTreeType) -> Optional[str]:
    initial = tag.find('initial')
    if initial is not None:
        action = initial.find('action')
        if action is not None:
            brief = action.get('brief').strip(';')
            return brief
        else:
            return None
    else:
        return None


# -----------------------------------------------------------------------
# get_actions_for_cross_transition
#
# For transitions that go from one state to another state, return
# a list of entry and exit actions and the final target state name.
# This is for transitions other than self transitions.
# -----------------------------------------------------------------------
def get_actions_for_cross_transition(trans: ElementTreeType) -> Tuple[Any, List[str], List[str]]:
        # Traverse up the state hierarchy looking for exit actions
        # and creating an exitList of actions
        upList: List[str] = []
        downList: List[str] = []
        target = trans.get('target')
        (upList, downList) = get_up_down_list(target)
        exitList = []
        entryList = []
        root = trans
        for i in upList:
            next = root.getparent()
            if root.tag == 'state':
                exitFunc = pick_exit(root)
                if exitFunc is not None:
                    exitList.append(exitFunc)
            root = next
                     
        # Traverse down the state hierarchy looking for entry actions
        # and creating an entryList of actions   

        for i in downList:
            root = get_state_from_index(root, int(i))
            entryFunc = pick_entry(root)
            initFunc = pick_init(root)
            if entryFunc is not None:
                entryList.append(entryFunc)
            if initFunc is not None:
                entryList.append(initFunc)
             
        exitList = [i for i in exitList if i is not None]
        entryList = [i for i in entryList if i is not None]      
        return(root.get('name'), exitList, entryList)      
    
# -----------------------------------------------------------------------
# get_up_down_list
#
# From a target string, return 2 lists:
# upList and downList
# -----------------------------------------------------------------------
def get_up_down_list(target: str) -> Tuple[List[str], List[str]]:
    targetSplit = target.split('/')
    upList: List[str] = []
    downList: List[str] = []

    for x in targetSplit:
        if x == '..':
            upList.append(x)
        else:
            downList.append(x)

    return upList, downList


# -----------------------------------------------------------------------
# get_actions_for_self_transition
#
# For self transitions, return
# a list of entry and exit actions and the final target state name.
# This is for transitions other than cross transitions.
# -----------------------------------------------------------------------
def get_actions_for_self_transition(trans: ElementTreeType) -> Tuple[Any, List[str], List[str]]:
        # Traverse up the state hierarchy looking for exit actions
        # and creating an exitList of actions
        upList: List[str] = []
        downList: List[str] = []
        target = trans.get('target')
        (upList, downList) = get_up_down_list(target)
        exitList: List[str] = []
        entryList: List[str] = []
        root = trans
        for i in upList:
            next = root.getparent()
            if next.tag == 'state':
                exitFunc = pick_exit(next)
                if exitFunc is not None:
                    exitList.append(exitFunc)
            root = next
         
        entry = pick_entry(root)
        if entry is not None:
            entryList.append(entry)
        for i in downList:
            root = get_state_from_index(root, int(i))
            entryFunc = pick_entry(root)
            if entryFunc is not None:
                entryList.append(entryFunc)
 
        exitList = [i for i in exitList if i is not None]
        entryList = [i for i in entryList if i is not None]                    
        return(root.get('name'), exitList, entryList)     
  

# -----------------------------------------------------------------------
# proc_tran
#
# The proc_tran function is designed to process a single transition 
# within a state machine, particularly focusing on parsing and handling 
# actions associated with transitions. The function takes a transition 
# element (tran) as its input and returns a tuple consisting of the 
# target state's name and three lists containing exit actions, 
# transition actions, and entry actions, respectively.
# -----------------------------------------------------------------------
def proc_tran(tran: ElementTreeType) -> Tuple[Any, List[str], List[str], List[str]]:  
        
    actionList = []
    target = tran.get('target')
        
    if target is None:
        action = pick_action(tran)
        if action is not None:
            actionList.append(action)
        return (None, [], actionList, [])
    else:
        
        # Get the action on the transition
        action = pick_action(tran)
        if action is not None:
            actionList.append(action)
                        
        
        if tran.get('local') == 'True':
            (targetState, exitList, entryList) = get_actions_for_cross_transition(tran)
        elif tran.get('self') == 'True':
            (targetState, exitList, entryList) = get_actions_for_self_transition(tran)
        else:
            (targetState, exitList, entryList) = get_actions_for_cross_transition(tran)
 

    return (targetState, exitList, actionList, entryList)

# -----------------------------------------------------------------------
# is_leaf
#
# For a given state, return True if leaf state else return False
# -----------------------------------------------------------------------
def is_leaf(state: ElementTreeType) -> bool:
    states = state.findall('state')
    if len(states) == 0:
        return True
    else:
        return False


# -----------------------------------------------------------------------------------------------------------
# new_rec
#
# This function is designed to process a state machine transition, as represented by an XML element 
# The goal of this function is to recursively navigate through the state machine transitions, copying relevant 
# actions and guards from the transitions and choices to a parent element in the state machine, flattening
# the state-machine hierarchy as it goes.  The input tran is the original hierarchical transition and
# the parent is the flattened transition.  The function recursively descends down the hierarchy of the 
# transition, building up the tranAction list which is a list of transition action and entry and exit
# state machine functions. 
# ------------------------------------------------------------------------------------------------------------

def new_rec(tran: ElementTreeType, parent: ElementTreeType, transActionList: List[str]):

    if tran.get('target'):
        (targetState, exitList, actionList, entryList) = proc_tran(tran)
        transActionList += actionList + exitList + entryList
        state = state_from_target(tran)
        if is_leaf(state):
            parent.set('target', targetState)
            if len(transActionList) != 0:
                new_action = etree.SubElement(parent, "action")
                new_action.set('brief', ";".join(transActionList))
        else:
            initial_tran = state.find('initial')
            new_rec(initial_tran, parent, transActionList)
    else:
            action = tran.find('action')
            if action is not None:
                new_action = etree.SubElement(parent, "action")
                new_action.set('brief', action.get('brief'))
            choices = tran.findall('choice')
            for choice in choices:
                new_choice = etree.SubElement(parent, "choice")
                guard = choice.find('guard')
                if guard is not None:
                    new_guard = etree.SubElement(new_choice, "guard")
                    new_guard.set('brief', guard.get('brief'))
                new_rec(choice, new_choice, transActionList.copy())


# -----------------------------------------------------------------------------
# flatten_state_machine
#
# Returns a flattened state-machine model from the hierarchical state-machine
# statechart.
#
# This flattening process can significantly simplify the analysis and implementation
# of state machines by reducing the complexity associated with nested states and 
# inherited transitions. The resulting flat state machine is easier to visualize, 
# debug, and translate into implementation code.
# 
# -----------------------------------------------------------------------------   
def flatten_state_machine(qmRoot: ElementTreeType) -> ElementTreeType:

    leaf_states_inherit(qmRoot)

    flatchart: ElementTreeType = etree.Element("FlatStateChart")
    
    initialTran = qmRoot.find('initial')
    new_initialTran = etree.SubElement(flatchart, 'initial')

    transActionList: List[str] = []
    new_rec(initialTran, new_initialTran, transActionList)

    states = qmRoot.iter("state")
    for state in states:
        if is_leaf(state):
            new_state = etree.SubElement(flatchart, state.tag, attrib=state.attrib)
            trans = state.findall('tran')
            for tran in trans:
                new_trans = etree.SubElement(new_state, tran.tag)
                new_trans.set('trig', tran.get('trig'))
                actionList: List[str] = []
                new_rec(tran, new_trans, actionList)

    # To print out the flattened state-machine, uncomment this line
    # qmlib.print_tree(flatchart)
    return flatchart

