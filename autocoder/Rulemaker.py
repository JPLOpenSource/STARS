#!/bin/env python3

# -----------------------------------------------------------------------------------------------------------------------
# Rulemaker.py
#
# Generates and/or appends Rules declarations and definitions to the file test/ut/MyRules.hpp and test/ut/MyRules.cpp
# In addition, generates test/ut/RulesHeaders.hpp if the file does not already exist.
#
# Example:
#    ./Rulemaker <Rule Name>
#
# Replace the Namespace 'ns' with your namespace
# -----------------------------------------------------------------------------------------------------------------------

from Cheetah.Template import Template
from pathlib import Path
import argparse
import sys

# !!!! Change this !!!!
ns = "Nav"


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
def rulesHeaders():

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
def headerFile(RuleName, ns):

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
def implFile(RuleName, ns, includeTheHeader):

    template = Template("""
    
    #if $includeTheHeader
  \#include "Tester.hpp"
    #end if


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
    template.includeTheHeader = includeTheHeader

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
def transImplFile(RuleName, ns, includeTheHeader, InitState, Trans, FinalState):

    template = Template("""
    
    #if $includeTheHeader
  \#include "Tester.hpp"
    #end if


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
                        
    return state.component.powerMgr->state == NavPwr::PowerMgr::PowerMgrStates::${InitState};
  }

  
  void ${ns}::Tester::${RuleName}::action(
            ${ns}::Tester& state //!< The test state
        ) 
  {
    printf("--> Rule: %s \\n", this->name);
    state.clearHistory();
                        
    // Actions
    // ${Trans}
        
    // Final state               
    EXPECT_EQ(state.component.powerMgr->state, NavPwr::PowerMgr::PowerMgrStates::${FinalState});

  }

"""
    )

    template.RuleName = RuleName
    template.ns = ns
    template.includeTheHeader = includeTheHeader
    template.InitState = InitState
    template.Trans = Trans
    template.FinalState = FinalState

    return(str(template))

def read_file_to_tuples(file_path):
    """
    Reads a text file where each line contains three fields separated by whitespace.
    Returns a list of tuples, each tuple containing the three fields of a line.
    """
    tuples_list = []

    with open(file_path, 'r') as file:
        for line in file:
            # Splitting the line into parts and creating a tuple
            fields = line.strip().split()
            if len(fields) == 3:
                tuples_list.append(tuple(fields))

    return tuples_list

def to_upper_camel_case(s):
    """
    Convert a string from upper case with underscores to upper camel case.
    Example: "WAIT_INIT" will be converted to "WaitInit".
    """
    # Split the string by underscores, convert each part to title case, and then join them without spaces
    return ''.join(word.title() for word in s.split('_'))


def first_char_to_lower(s):
    if not s:
        # Return the original string if it's empty
        return s
    return s[0].lower() + s[1:]



def rule_exists(rule):
    thisFile = Path(rulesHFile)
    if thisFile.is_file():
        with open(thisFile, 'r') as fp:
            content = fp.read()
            if f'struct {rule}' in content:
                return True
            else:
                return False


def make_rule(rule):
    if rule is None:
        return
    if rule_exists(rule):
        print(f'Rule {rule} already exists!!')
        return False

    thisFile = Path(rulesCFile)
    if thisFile.is_file():
        includeTheHeader = False
    else:
        includeTheHeader = True

    print(f"Generating Rule {rule}")

    hFile = open(rulesHFile, "a")
    hFile.write(headerFile(rule, ns))
    hFile.close()

    iFile = open(rulesCFile, "a")
    if args.sm:
        iFile.write(transImplFile(rule, ns, includeTheHeader, InitState, Trans, FinalState))
    else:
        iFile.write(implFile(rule, ns, includeTheHeader))

    iFile.close()

    thisFile = Path(rulesHeaderFile)
    if not thisFile.is_file():
        print(f'Generating {rulesHeaderFile}')
        hFile = open(rulesHeaderFile, 'w')
        hFile.write(rulesHeaders());
        hFile.close()    
    return True

def instance_of_rule(rule):
    return f'\t{rule}\t{first_char_to_lower(rule)};'

def execution_of_rule(rule):
    return f'\t{first_char_to_lower(rule)}.apply(*this);'

# -------------------------------------------------------------------------------------------------------------------------
# Main routine
# -------------------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Unit Test Rule Generator.')
parser.add_argument('rule', nargs='?', default=None, help='The name of the rule')
parser.add_argument('--sm', action='store_true', help='Use the state transition template')

args = parser.parse_args()

rulesHFile = "test/ut/MyRules.hpp"
rulesCFile = "test/ut/MyRules.cpp"
rulesHeaderFile = "test/ut/RulesHeaders.hpp"

instanceList = []
executionList = []

if args.sm:

    TransList = read_file_to_tuples("PwrMgrStates.txt")

    for trans in TransList:
        InitState = trans[0]
        Trans = trans[1]
        FinalState = trans[2]
        rule = to_upper_camel_case(InitState) + "_" + \
               to_upper_camel_case(Trans) + "_" + \
               to_upper_camel_case(FinalState)
        
        if make_rule(rule):
            instanceList.append(instance_of_rule(rule))
            executionList.append(execution_of_rule(rule))

    print('\nInstances:')
    for instance in instanceList:
        print(f'{instance}')

    print('\nExecute:')
    for execution in executionList:
        print(f'{execution}')

else:
    make_rule(args.rule)

