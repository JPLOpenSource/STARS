#!/bin/env python

from xmiModelApi import XmiModel
from lxml.etree import _ElementTree
ElementTreeType = _ElementTree 
from anytree import Node
from typing import Dict, List
import copy

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
# construct_fst
#
# 
# -----------------------------------------------------------------------------   
def construct_fst(t: Node) -> Node:
    if t.kind == "internal":
        return t

# -----------------------------------------------------------------------------
# visit_state
#
# -----------------------------------------------------------------------------   
def visit_state(xmiModel: XmiModel, state: Node, stm: Dict[str, Node]):
    stm_p = copy.deepcopy(stm)
    for sd in get_child_states(state):

        for sts in get_child_trans(sd):
            s = sts.event
            if sts.kind == "internal":
                t = sts
                print(f"Internal transition {s} with action {t.action}")
            else:
                t = sts
                print(f"Regular transition {s} with action {t.action} and target {t.target}")
            stm[s] = sts


        print(f'stm for state {sd.stateName} = {stm.keys()}')

        if is_leaf(sd):
            #t_p = construct_fst(t)
            xmiModel.fstm[sd] = stm
            print(f'State {sd.stateName} is Leaf')
        else:
            print(f'State {sd.stateName} is not Leaf')
            visit_state(xmiModel, sd, stm)

        stm = copy.deepcopy(stm_p)

        #visit_state(xmiModel, sd, stm)

# -----------------------------------------------------------------------------
# flatten_state_machine
#
# -----------------------------------------------------------------------------   
def flatten_state_machine(xmiModel: XmiModel) -> ElementTreeType:
    print("Flattening state machine")
    stm = {}
    visit_state(xmiModel, xmiModel.tree, stm)

    xmiModel.print()
