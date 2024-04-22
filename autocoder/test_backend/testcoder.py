#!/bin/env python3
# -----------------------------------------------------------------------
# testcoder.py
#
# Implements an Oracle for testing a state machine
# -----------------------------------------------------------------------

import qmlib
import flattenstatemachine as flatt

from test_backend.testtemplates import TestTemplate
from typing import List, Dict, Tuple, Any, Optional, IO
from qmlib import ElementTreeType
from pydantic import BaseModel
import json
import os
import sys

# Pydantic classes that specify the configSm.json
class Guard(BaseModel):
    name: str
    state: str
    
class TestConfig(BaseModel):
    currentState: str
    event: str
    guards: List[Guard]


# Initialize global variables
codeTemplate = TestTemplate()

TEST_JSON_FILE = "test.json"

# ---------------------------------------------------------------------------
# testHarnessTransition
#
# ---------------------------------------------------------------------------
def testHarnessTransition(smname: str, tran: ElementTreeType) -> List[str]:
    rstr = []
    
    # Action
    action = qmlib.pick_action(tran)
    if action:
        functionList = qmlib.n_parse_function_args(action)
        for func in functionList:
            actionName, actionArgs = qmlib.parse_action(func)
            sig = codeTemplate.pythonAction(actionName)
            rstr.append(sig)
    
    # Target
    targetState = tran.get('target')
    if targetState:
        rstr.append(f'return (actionList,"{targetState}")')
      
    # Choices  
    choices = tran.findall('choice')
    if len(choices) == 0:
        return rstr
        
    ifChoice = None
    elseChoice = None

    for choice in choices:
        guard = choice.find('guard')
        if guard is not None:
            if ifChoice is None:
                ifChoice = choice
        else:
            elseChoice = choice

    # Do the ifchoice    
    initialGuard = qmlib.pick_guard(ifChoice)
    actionName, actionArgs = qmlib.parse_action(initialGuard)   #type: ignore
    sig = codeTemplate.ifPythonGuard(actionName)
    rstr.append(sig)

    rstr = rstr + testHarnessTransition(smname, ifChoice)
    rstr.append("}")

    # Do the elseChoice
    if elseChoice is not None:
        rstr.append("else: {")
        rstr = rstr + testHarnessTransition(smname, elseChoice)
        rstr.append("}")

    return rstr


# -----------------------------------------------------------------------
# generatePythonCode
#
# This function
#
# ----------------------------------------------------------------------- 
def genPythonCode(flatchart: ElementTreeType, smname: str, currentState: str, event: str, guards: List[Guard]):
    states = flatchart.iter("state")
    for state in states:
        if state.get("name") == currentState:
            trans = state.findall('tran')
            for tran in trans:
                if tran.get("trig") == event:
                    oracleCode = qmlib.format_python(testHarnessTransition(smname, tran), 6)
                    return codeTemplate.pythonOracle(guards, oracleCode)
            assert False, f'Could not find event {event}'
    assert False, f'Could not find state {currentState}'

# -----------------------------------------------------------------------
# generateCode
#
# This function
#
# ----------------------------------------------------------------------- 
def generateCode(smname: str, statechart: ElementTreeType):
    global codeTemplate
    global unitTestTemplate
    global codeImplTemplate

    with open(TEST_JSON_FILE, 'r') as file:
        json_data = json.load(file)

    config = TestConfig(**json_data)
    currentState = config.currentState
    event = config.event
    guards = config.guards

    flatchart : ElementTreeType = flatt.flatten_state_machine(statechart)
    
    python_code = genPythonCode(flatchart, smname, currentState, event, guards)

    local_vars = {}
    exec(python_code, {}, local_vars)
    result = local_vars['result']
    print(result)

    sys.exit()
