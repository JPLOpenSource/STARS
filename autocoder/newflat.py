#!/bin/env python

from xmiModelApi import XmiModel
from lxml.etree import _ElementTree
ElementTreeType = _ElementTree 
from anytree import Node
from typing import Dict, List
import copy
import sys

# -----------------------------------------------------------------------------
# get_child_trans
#
# Get a list of child transitions under this state
# -----------------------------------------------------------------------------   
def get_child_trans(state: Node) -> List[Node]:
    return [child for child in state.children if child.name == "TRANSITION"]

# -----------------------------------------------------------------------------
# get_child_states
#
# Get a list of child states under this state
# -----------------------------------------------------------------------------   
def get_child_states(state: Node) -> List[Node]:
    return [child for child in state.children if child.name == "STATE"]

# -----------------------------------------------------------------------------
# get_child_junctions
#
# Get a list of child states under this state
# -----------------------------------------------------------------------------   
def get_child_junctions(state: Node) -> List[Node]:
    return [child for child in state.children if child.name == "JUNCTION"]

# -----------------------------------------------------------------------------
# is_leaf
#
# Is this state a leaf state
# -----------------------------------------------------------------------------   
def is_leaf(state: Node) -> bool:
    if len(get_child_states(state)) == 0:
        return True
    else:
        return False

# -----------------------------------------------------------------------------
# get_state_ancestors
#
# -----------------------------------------------------------------------------   
def get_state_ancestors(soj: Node) -> List[Node]:
    # Get the list of ancestors (including the node itself)
    if soj.name == "STATE":
        ancestors_including_self = list(soj.ancestors) + [soj]
        # Filter to include only those with the name "STATE"
        state_ancestors = [n for n in ancestors_including_self if n.name == "STATE"]
    else:
        state_ancestors = []

    return state_ancestors

# -----------------------------------------------------------------------------
# print_state_list
#
# -----------------------------------------------------------------------------   
def print_state_list(msg: str, stateList: List[Node]):
    print(f"{msg} = ", end = " ")
    for state in stateList:
        print(f"{state.stateName}", end = " ")
    print()


# -----------------------------------------------------------------------------
# common_prefix
#
# -----------------------------------------------------------------------------   
def common_prefix(list1: List[Node], list2: List[Node]) -> List[Node]:
    prefix = []
    for elem1, elem2 in zip(list1, list2):
        if elem1 == elem2:
            prefix.append(elem1)
        else:
            break
    return prefix

# -----------------------------------------------------------------------------
# get_exit_actions
#
# -----------------------------------------------------------------------------   
def get_exit_actions(stateList: List[Node]) -> List[str]:
    thisList = []
    for state in stateList[::-1]:
        if state.exit is not None:
            thisList.append(state.exit)
    return thisList

# -----------------------------------------------------------------------------
# get_entry_actions
#
# -----------------------------------------------------------------------------   
def get_entry_actions(stateList: List[Node]) -> List[str]:
    thisList = []
    for state in stateList:
        if state.entry is not None:
            thisList.append(state.entry)
    return thisList


# -----------------------------------------------------------------------------
# construct_fst
#
# -----------------------------------------------------------------------------   
def construct_fst(xmiModel: XmiModel, soj: Node, t: Node) -> Node:

    t_p = copy.deepcopy(t)

    if t_p.kind != "internal":
        L1 = get_state_ancestors(soj)
        targetId = t.target
        targetState = xmiModel.idMap[targetId]
        L2 = get_state_ancestors(targetState)
        P = common_prefix(L1, L2)

        if (len(P) != 0) and ((P == L1) or (P == L2)):
            # This is a self transition, remove the last element of the list 
            # so that we exit and enter the self transition state
            P.pop()

        prefix_length = len(P)
        L1 = L1[prefix_length:]
        # Pop the last element off the entry list
        L2 = L2[prefix_length:][:-1]        

        exitActions = get_exit_actions(L1)
        entryActions = get_entry_actions(L2)

        transActions = t_p.action.split(';') if t_p.action else []

        allActions = exitActions + transActions + entryActions
        actionString = ';'.join([action for action in allActions if action is not None])
        t_p.action = actionString

    return t_p

# -----------------------------------------------------------------------------
# visit_state
#
# -----------------------------------------------------------------------------   
def visit_state(xmiModel: XmiModel, state: Node, stm: Dict[str, Node]):
    stm_p = copy.deepcopy(stm)
    for sd in get_child_states(state):

        for sts in get_child_trans(sd):
            s = sts.event
            # Update stm so that it maps s to (g,t). 
            stm[s] = sts

        if is_leaf(sd):

            # For each signal s in stm
            for s in stm.keys():
                t_p = construct_fst(xmiModel, sd, stm[s])
                stm[s] = t_p

            xmiModel.fstm[sd] = stm
        else:
            visit_state(xmiModel, sd, stm)

        stm = copy.deepcopy(stm_p)

# -----------------------------------------------------------------------------
# flatten_state_machine
#
# -----------------------------------------------------------------------------   
def flatten_state_machine(xmiModel: XmiModel) -> ElementTreeType:
    print("Flattening state machine")
    stm = {}
    visit_state(xmiModel, xmiModel.tree, stm)