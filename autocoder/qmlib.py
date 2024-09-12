#!/bin/env python
# -----------------------------------------------------------------------
# qmlib.py
# 
# Some common library functions used by the Stars
#
# -----------------------------------------------------------------------

from lxml import etree
import sys
from copy import deepcopy
from Cheetah.Template import Template  # type: ignore
from typing import List, Dict, Tuple, Optional
from lxml.etree import _ElementTree
ElementTreeType = _ElementTree 
from typing import Tuple


# -----------------------------------------------------------------------
# get_name
#
# Return the name of the action function
# -----------------------------------------------------------------------  
def get_name(action: str) -> str:
    return action.split('(')[0]

# -----------------------------------------------------------------------
# format_C
#
# Input cStatements is a list of C statement strings
# The startTab is the number of spaces to initially indent the returned string.
# Returns a single string of all the input items with 
# spacing tabs and line returns
# -----------------------------------------------------------------------
def format_C(cStatements: List[str], startTab: int) -> str:
    output = ""
    tab = startTab
    indent = 4
    for s in cStatements:
        if s.find('}') >= 0:
            tab = tab - indent
        output = output + ' '*tab + s + "\n"
        if s.find('{') >= 0:
            tab = tab + indent
            
    return output 

# -----------------------------------------------------------------------
# format_python
#
# Input cStatements is a list of C statement strings
# The startTab is the number of spaces to initially indent the returned string.
# Returns a single string of all the input items with 
# spacing tabs and line returns
# -----------------------------------------------------------------------
def format_python(cStatements: List[str], startTab: int) -> str:
    output = ""
    tab = startTab
    indent = 4
    for s in cStatements:
        if s.find('}') >= 0:
            tab = tab - indent
        output = output + ' '*tab + s.replace("{", "").replace("}", "") + "\n"
        if s.find('{') >= 0:
            tab = tab + indent
            
    return output 

# -----------------------------------------------------------------------
# pick_guard

# Input is QM xml tags
# Return the guard function
# -----------------------------------------------------------------------
def pick_guard(tag: ElementTreeType) -> Optional[str]:
    guard = tag.find('guard')
    if guard is not None:
        brief = guard.get('brief')
        return brief
    else:
        return None
    
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
# get_trans_functions(root)
#
# Traverse the xml tree and return with a list of all the transition
# action functions.
# -----------------------------------------------------------------------  
def get_trans_functions(root: ElementTreeType) -> List[str]:
    list: List[str] = []
    if root is None:
        return list;
    
    for child in root:
        if child.tag == 'choice' or child.tag == 'tran' or child.tag == 'initial':
            action = child.find('action')
            if action is not None:
                list.append(action.get('brief'))
            
        list = list + get_trans_functions(child)
        
    # Handle more than 1 function in an action
    newList: List[str] = []
    for i in list:
        newList = newList + [x.strip() for x in i.strip(';').split(';')]
        
    # Remove duplicates from the list
    return [i for n, i in enumerate(newList) if i not in newList[:n]]

# -----------------------------------------------------------------------
# get_state_functions(root)
#
# Traverse the xml tree and return with a list of all the state entry
# and exit functions.
# -----------------------------------------------------------------------  
def get_state_functions(root: ElementTreeType) -> List[str]:
    list: List[str] = []
    if root is None:
        return list;
    
    for child in root:
        if child.tag == 'state':
            entry = child.find('entry')
            if entry is not None:
                list.append(entry.get('brief'))
            exit = child.find('exit')
            if exit is not None:
                list.append(exit.get('brief'))
        list = list + get_state_functions(child)
        
    # Handle more than 1 function in an action
    newList: List[str] = []
    for i in list:
        newList = newList + [x.strip() for x in i.strip(';').split(';')]
        

    # Remove duplicates from the list
    return [i for n, i in enumerate(newList) if i not in newList[:n]]

# -----------------------------------------------------------------------
# get_guard_functions
#
# Traverse the xml tree and return with a list of all the guard functions
# -----------------------------------------------------------------------  
def get_guard_functions(root: ElementTreeType) -> List[str]:
    list: List[str] = []
    if root is None:
        return list;
    
    for child in root:                
        if child.tag == 'guard':
            list.append(child.get('brief'))
        list = list + get_guard_functions(child)

    # Remove duplicates from the list
    return [i for n, i in enumerate(list) if i not in list[:n]]


# ---------------------------------------------------------------------------
# n_parse_function_args
#
# Given a function with an optional event argument,
# return a list of functions
# ---------------------------------------------------------------------------    
def n_parse_function_args(func: str) -> List[str]:
    lines = func.replace('\n', '').replace(' ','').strip(';').split(';')
    return lines
    

# ---------------------------------------------------------------------------
# parse_action
#
# Given an action with an optional event argument,
# return the action and args as strings
# ---------------------------------------------------------------------------    
def parse_action(func: str) -> Tuple[str, str]:

    s = func.split('(')
    actionName = s[0]
    actionArgs = s[1].strip(')')
    return (actionName, actionArgs)


# ---------------------------------------------------------------------------
# print_tree
#
# ---------------------------------------------------------------------------
def print_tree(node: ElementTreeType):
    xml_string = etree.tostring(node, pretty_print=True)
    print(xml_string.decode())


# ---------------------------------------------------------------------------
# state_state_machine
#
# ---------------------------------------------------------------------------
def get_state_machine(qmRoot: ElementTreeType) -> Tuple[ElementTreeType, str]:
    package = qmRoot.find('package')
    className = package.find('class')
    statechart = className.find('statechart')
    smname = className.get('name')
    return statechart, smname
