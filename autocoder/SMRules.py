#!/bin/env python3

# -----------------------------------------------------------------------------------------------------------------------
# SMRules.py
# 
# Author: Garth Watney
#
# Generates Rules for state-machine transitions
#
# usage: SMRules.py [-h] [--ovr] transfile namespace
#
# Unit Test Rule Generator.
#
# positional arguments:
#   transfile   State transition text file
#   namespace   Namespace for the Rules
#
# optional arguments:
#   -h, --help  show this help message and exit
#   --ovr       Override any existing Rule
#
# Example:
#    ./SMRules.py PowerMgr.trans Nav --ovr
#
# -----------------------------------------------------------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from pathlib import Path
import argparse
import sys
import os
from typing import List, Dict, Tuple

RULES_H_FILE: str = "test/ut/SMRules.hpp"
RULES_C_FILE: str = "test/ut/SMRules.cpp"
RULES_HEADER_FILE: str = "test/ut/RulesHeaders.hpp"


# -------------------------------------------------------------------------------------------------------------------------
# rulesHeaders
#
# Encapsulates the template for RulesHeaders.hpp
#
# Inputs:
#
# Returns:
#    The string of the declaration
#
# -------------------------------------------------------------------------------------------------------------------------
def rulesHeaders() -> str:

    template = Template("""

#ifndef __RULES_HEADERS__
#define __RULES_HEADERS__

\#include "STest/STest/Rule/Rule.hpp"
\#include "STest/Scenario/BoundedScenario.hpp"
\#include "STest/Scenario/RandomScenario.hpp"
\#include "STest/Scenario/Scenario.hpp"

#endif
""")

    return(str(template))


# -------------------------------------------------------------------------------------------------------------------------
# headerFile
#
# Encapsulates the template for a Rule class declaration
#
# Inputs:
#   RuleName :  The name of the Rule
#   ns       :  The namespace of Tester
#
# Returns:
#    The string of the declaration
#
# -------------------------------------------------------------------------------------------------------------------------
def headerFile(RuleName: str, ns: str) -> str:

    template = Template("""



    // ------------------------------------------------------------------------------------------------------
    // Rule:  ${RuleName}
    //
    // ------------------------------------------------------------------------------------------------------
    struct ${RuleName} : public STest::Rule<${ns}::Tester> {

            // ----------------------------------------------------------------------
            // Construction
            // ----------------------------------------------------------------------

            //! Constructor
            ${RuleName}();

            // ----------------------------------------------------------------------
            // Public member functions
            // ----------------------------------------------------------------------

            //! Precondition
            bool precondition(
                const ${ns}::Tester& state //!< The test state
            );

            //! Action
            void action(
                ${ns}::Tester& state //!< The test state
            );

    };

    """
    )

    template.RuleName = RuleName
    template.ns = ns
    return(str(template))

# -------------------------------------------------------------------------------------------------------------------------
# implFile
#
# Encapsulates the template for a Rule class definition
#
# Inputs:
#   RuleName :  The name of the Rule
#   ns       :  The namespace of Tester
#
# Returns:
#    The string of the definition
#
# The first time this is used, add
# \#include "Tester.hpp" in the template
# 
# -------------------------------------------------------------------------------------------------------------------------
def implFile(RuleName: str, ns: str) -> str:

    template = Template("""
    
  // ------------------------------------------------------------------------------------------------------
  // Rule:  ${RuleName}
  //
  // ------------------------------------------------------------------------------------------------------
  
  ${ns}::Tester::${RuleName}::${RuleName}() :
        STest::Rule<${ns}::Tester>("${RuleName}")
  {
  }


  bool ${ns}::Tester::${RuleName}::precondition(
            const ${ns}::Tester& state //!< The test state
        ) 
  {
      return true;
  }

  
  void ${ns}::Tester::${RuleName}::action(
            ${ns}::Tester& state //!< The test state
        ) 
  {
      printf("--> Rule: %s \\n", this->name);
  }

"""
    )

    template.RuleName = RuleName
    template.ns = ns

    return(str(template))



# -------------------------------------------------------------------------------------------------------------------------
# transImplFile
#
# Encapsulates the template for a Rule class definition for a state transition
#
# Inputs:
#   RuleName :  The name of the Rule
#   ns       :  The namespace of Tester
#   InitState : The initial state
#   Trans    : The transition event
#   FinalState : The final state
#
# Returns:
#    The string of the definition
#
# The first time this is used, add
# \#include "Tester.hpp" in the template
#
# -------------------------------------------------------------------------------------------------------------------------
def transImplFile(RuleName: str, ns: str, InitState: str, Trans: str, Guards: str, Actions: str, FinalState: str) -> str:

    template = Template("""

  // ------------------------------------------------------------------------------------------------------
  // Rule:  ${RuleName}
  //
  // ------------------------------------------------------------------------------------------------------

  ${ns}::Tester::${RuleName}::${RuleName}() :
        STest::Rule<${ns}::Tester>("${RuleName}")
  {
  }


  bool ${ns}::Tester::${RuleName}::precondition(
            const ${ns}::Tester& state //!< The test state
        )
  {

    if (state.current_state(PowerMgr::PowerMgrStates::${InitState}))
    {
        #for $guard in $guardList
        if (!state.$(guard)) {
            return false;
        }
        #end for
        return true;                        
    } else {
        return false;
    }
                        
  }


  void ${ns}::Tester::${RuleName}::action(
            ${ns}::Tester& state //!< The test state
        )
  {
    printf("--> Rule: %s \\n", this->name);
    state.clearHistory();

    // Generate the commands or events
    state.$(Trans)();
                        
    // Generate action checks
    #for $action in $actionList
    state.$(action);
    #end for
                        
    // Final state
    EXPECT_TRUE(state.current_state(PowerMgr::PowerMgrStates::${FinalState}));

  }

"""
    )

    template.RuleName = RuleName
    template.ns = ns
    template.InitState = InitState
    template.Trans = Trans
    template.FinalState = FinalState
    
    template.guardList = []
    if Guards != "None":
        template.guardList = Guards.split(";")

    template.actionList = []
    if Actions != "None":
        # Remove white spaces and split
        template.actionList = ''.join(Actions.split()).split(';')

    return(str(template))




# -------------------------------------------------------------------------------------------------------
# to_upper_camel_case()
# 
# -------------------------------------------------------------------------------------------------------
def to_upper_camel_case(s: str) -> str:
    """
    Convert a string from upper case with underscores to upper camel case.
    Example: "WAIT_INIT" will be converted to "WaitInit".
    """
    # Split the string by underscores, convert each part to title case, and then join them without spaces
    return ''.join(word.title() for word in s.split('_'))


# -------------------------------------------------------------------------------------------------------
# first_char_to_lower()
# 
# -------------------------------------------------------------------------------------------------------
def first_char_to_lower(s: str) -> str:
    if not s:
        # Return the original string if it's empty
        return s
    return s[0].lower() + s[1:]



# -------------------------------------------------------------------------------------------------------
# rule_exists()
# 
# -------------------------------------------------------------------------------------------------------
def rule_exists(rule: str) -> bool:
    thisFile = Path(RULES_H_FILE)
    if thisFile.is_file():
        with open(thisFile, 'r') as fp:
            content = fp.read()
            if f'struct {rule}' in content:
                return True
            else:
                return False
    else:
        return False

# -------------------------------------------------------------------------------------------------------
# make_trans_rule()
# 
# -------------------------------------------------------------------------------------------------------
def make_trans_rule(rule: str, InitialState: str, Event: str, Guards: str, Actions: str, TargetState: str):

    print(f"Generating Rule {rule}")

    hFile = open(RULES_H_FILE, "a")
    hFile.write(headerFile(rule, NAME_SPACE))
    hFile.close()

    iFile = open(RULES_C_FILE, "a")
    iFile.write(transImplFile(rule, NAME_SPACE, InitialState, Event, Guards, Actions, TargetState))
    iFile.close()

    thisFile = Path(RULES_HEADER_FILE)
    if not thisFile.is_file():
        print(f'Generating {RULES_HEADER_FILE}')
        hFile = open(RULES_HEADER_FILE, 'w')
        hFile.write(rulesHeaders());
        hFile.close()

# -------------------------------------------------------------------------------------------------------
# make_guard_rule()
# 
# -------------------------------------------------------------------------------------------------------
def make_guard_rule(rule: str):

    print(f"Generating Rule {rule}")

    hFile = open(RULES_H_FILE, "a")
    hFile.write(headerFile(rule, NAME_SPACE))
    hFile.close()

    iFile = open(RULES_C_FILE, "a")
    iFile.write(implFile(rule, NAME_SPACE))
    iFile.close()

    thisFile = Path(RULES_HEADER_FILE)
    if not thisFile.is_file():
        print(f'Generating {RULES_HEADER_FILE}')
        hFile = open(RULES_HEADER_FILE, 'w')
        hFile.write(rulesHeaders());
        hFile.close()

# -------------------------------------------------------------------------------------------------------
# instance_of_rule()
# 
# -------------------------------------------------------------------------------------------------------

def instance_of_rule(rule: str) -> str:
    return f'\t{rule}\t{first_char_to_lower(rule)};'


# -------------------------------------------------------------------------------------------------------
# instance_of_rule()
# 
# -------------------------------------------------------------------------------------------------------
def execution_of_rule(rule: str) -> str:
    return f'\t{first_char_to_lower(rule)}.apply(*this);'

# -------------------------------------------------------------------------------------------------------
# read_file_and_parse_data()
# 
# -------------------------------------------------------------------------------------------------------
def read_file_and_parse_data(file_path: str) -> List[Dict[str, str]]:
#def read_file_and_parse_data(file_path):
    # List to hold all the data structures
    data_list = []

    # Open the file and read line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Check that there are no dashes in the line because dashes
            # are reserved to separate guard names.
            if '-' in line:
                print(f'*** ERROR! Dashes not allowed: {line}')
                sys.exit()
            # Split the line by commas and then by '=' to get key-value pairs
            parts = line.split(', ')
            data = {}
            for part in parts:
                key, value = part.split(' = ')
                # Store the key-value pair in the dictionary
                data[key.strip()] = value.strip()

            # Add the dictionary to the list
            data_list.append(data)

    return data_list

# -------------------------------------------------------------------------------------------------------
# genRuleName()
# 
# -------------------------------------------------------------------------------------------------------
def genRuleName(initialState: str, event: str, guards: str, targetState: str) -> str:

    if guards != "None":
        guardName = guards.replace(';', '00').replace('(', '').replace(')', '')
    else:
        guardName = ""

    ruleName = to_upper_camel_case(initialState) + "_" + \
               to_upper_camel_case(event) + "_" + \
               to_upper_camel_case(guardName) + "_" +\
               to_upper_camel_case(targetState)
    
    return ruleName


# -------------------------------------------------------------------------------------------------------
# genGuardRuleName()
# 
# -------------------------------------------------------------------------------------------------------
def genGuardRuleName(guard: str) -> Tuple[str, str]:
    setRuleName = "set_" + to_upper_camel_case(guard)
    clearRuleName = "clear_" + to_upper_camel_case(guard)
    return (setRuleName, clearRuleName)

# ------------------------------------------------------------------------------------------------------------------------
# getAllGuards()
# Go through all the data and collect a list of unique guard names
# ------------------------------------------------------------------------------------------------------------------------
def getAllGuards(parsedData: List[Dict[str, str]]) -> List[str]:
    guardList = []
    for data in parsedData:
        Guards = data["guard"]
        if Guards != "None":
            glist = Guards.split(';')
            for g in glist:
                guardName = g.replace('(', '').replace(')', '')
                if guardName not in guardList:
                    guardList.append(guardName)
    return guardList



# -------------------------------------------------------------------------------------------------------------------------
# init_file()
# -------------------------------------------------------------------------------------------------------------------------
def init_files(ovr: bool, hFileName: str, cFileName: str):
    if ovr:
        print("We are going to override any exsting rules")

        try:
            os.remove(hFileName)
        except FileNotFoundError:
            pass  # File does not exist, no action needed

        try:
            os.remove(cFileName)
        except FileNotFoundError:
            pass  # File does not exist, no action needed

    # If the C file does not exist, then open it and 
    # write an include header.
    # If the C file does exist, then just open it.    
    thisFile = Path(cFileName)
    if thisFile.is_file():
        cFile = open(cFileName, "a")
    else:
        cFile = open(cFileName, "a")
        cFile.write('#include "Tester.hpp"\n')
    cFile.close()


# -------------------------------------------------------------------------------------------------------------------------
# process_guard_rules
# -------------------------------------------------------------------------------------------------------------------------
def process_guard_rules(parsedData: List[Dict[str, str]]) -> List[str]:
    ruleList = []
    guardList: List[str] = getAllGuards(parsedData)
    for guard in guardList:
        rules: Tuple[str, str] = genGuardRuleName(guard)
        setRule: str = rules[0]
        clearRule: str = rules[1]

        if rule_exists(setRule):
            print(f'Rule {setRule} already exists!!')
        else:
            make_guard_rule(setRule)
            ruleList.append(setRule)

        if rule_exists(clearRule):
            print(f'Rule {clearRule} already exists!!')
        else:
            make_guard_rule(clearRule)
            ruleList.append(clearRule)
    return ruleList


# -------------------------------------------------------------------------------------------------------------------------
# process_trans_rules
# -------------------------------------------------------------------------------------------------------------------------
def process_trans_rules(parsedData: List[Dict[str, str]]) -> List[str]:
    ruleList = []
    # Make a Rule for every state-machine transition
    for data in parsedData:

        InitialState = data["InitialState"]
        Event = data["Event"]
        Guards = data["guard"]
        Actions = data['action']
        TargetState = data["TargetState"]

        rule: str = genRuleName(InitialState, Event, Guards, TargetState)

        if rule_exists(rule):
            print(f'Rule {rule} already exists!!')
        else:
            make_trans_rule(rule, InitialState, Event, Guards, Actions, TargetState)
            ruleList.append(rule)
    return ruleList


# -------------------------------------------------------------------------------------------------------------------------
# printRules()
# -------------------------------------------------------------------------------------------------------------------------
def printRules(transRules: List[str], guardRules: List[str]):

    print("\n\t//Trans Rules Instantiation:")
    for rule in transRules:
        print(instance_of_rule(rule))

    print("\n\t//Guard Rules Instantiation:")
    for rule in guardRules:
        print(instance_of_rule(rule))

    print("\n\t//Trans Rules Execution:")
    for rule in transRules:
        print(execution_of_rule(rule))

    print("\n\t//Guard Rules Execution:")
    for rule in guardRules:
        print(execution_of_rule(rule))
    print("\n")

# -------------------------------------------------------------------------------------------------------------------------
# Main routine
# -------------------------------------------------------------------------------------------------------------------------

# Application arguments
parser = argparse.ArgumentParser(description='Unit Test Rule Generator.')
parser.add_argument('--ovr', action='store_true', help='Override any existing Rule')
parser.add_argument('transfile', help='State transition text file')
parser.add_argument('namespace', help='Namespace for the Rules')
args = parser.parse_args()

TRANS_FILE = args.transfile
NAME_SPACE = args.namespace

if not os.path.exists(TRANS_FILE):
    print(f'*** Error, the file {TRANS_FILE} does not exist')
    sys.exit()

# Initialize files
init_files(args.ovr, RULES_H_FILE, RULES_C_FILE)

# Get the data
parsedData: List[Dict[str, str]] = read_file_and_parse_data(TRANS_FILE)

transRules: List[str] = process_trans_rules(parsedData)

guardRules: List[str] = process_guard_rules(parsedData)

printRules(transRules, guardRules)

print(f'Number Transition Rules = {len(transRules)}')
print(f'Number Guard Rules = {len(guardRules)}')
