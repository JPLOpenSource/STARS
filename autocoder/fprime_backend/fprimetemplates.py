#!/bin/env python3
# -----------------------------------------------------------------------
# fprimetemplates.py
#
# A python class that contains template code for the Stars 
# fprime back-end 
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO

class FprimeTemplate:
    
# -------------------------------------------------------------------------------
# target
# -------------------------------------------------------------------------------   
        def target(self, targ: str) -> str:
            
            template = Template("""this->state = $(target);""")
                     
            template.target = targ
            return str(template)
        
# -------------------------------------------------------------------------------
# ifGuard
# ------------------------------------------------------------------------------- 
        def ifGuard(self, smname: str, action: str, args: str) -> str:  
            if args == "":
                template = Template("""if ( parent->$(smname)_$(action)(stateMachineId) ) {""")
            else:
                template = Template("""if (parent->$(smname)_$(action)(stateMachineId, signal, data) ) {""")       

            template.smname = smname
            template.action = action
            template.args = args
            return str(template)  

# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""bool $(smname)_$(action)(const FwEnumStoreType stateMachineId)""")
            elif args == "e":
                template = Template("""bool $(smname)_$(action)(
        const FwEnumStoreType stateMachineId, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")
            elif args.isdigit():
                template = Template("""bool $(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)

# -------------------------------------------------------------------------------
# guardDef
# -------------------------------------------------------------------------------   
        def guardDef(self, smname: str, action: str, component: str, args: str, namespace) -> str:
            if args == "":
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)(const FwEnumStoreType stateMachineId)""")
            elif args == "e":
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)(
        const FwEnumStoreType stateMachineId, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")         

            elif args.isdigit():
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"

            template.smname = smname
            template.namespace = namespace
            template.action = action
            template.component = component
            return str(template)

# -------------------------------------------------------------------------------
# action
# -------------------------------------------------------------------------------   
        def action(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""parent->$(smname)_$(action)(stateMachineId);""")   
            else:
                template = Template("""parent->$(smname)_$(action)(stateMachineId, signal, data);""")         
     
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)


# -------------------------------------------------------------------------------
# call_state
# -------------------------------------------------------------------------------   
        def call_state(self, smname: str) -> str:
            template = Template("""enter_$(smname)(stateMachineId);""")         
     
            template.smname = smname
            return str(template)


# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""void $(smname)_$(action)(const FwEnumStoreType stateMachineId)""")
            elif args == "e":
                template = Template(""" void $(smname)_$(action)(
        const FwEnumStoreType stateMachineId, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")
            elif args.isdigit():
                template = Template("""void $(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)


# -------------------------------------------------------------------------------
# actionDef
# -------------------------------------------------------------------------------   
        def actionDef(self, smname: str, action: str, component: str, args: str, namespace: str) -> str:
            if args == "":
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(const FwEnumStoreType stateMachineId)""")   
            elif args == "e":
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(
        const FwEnumStoreType stateMachineId, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")         
            elif args.isdigit():
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(int arg)""")         
            else:
                assert True, "Unknown args"
                
            template.namespace = namespace
            template.smname = smname
            template.action = action
            template.component = component
            return str(template)

# -------------------------------------------------------------------------------
# stateTransition
# -------------------------------------------------------------------------------   
        def stateTransition(self, signal: str, transitionCode: str, smname) -> str:
            template = Template("""
                case $(smname)_Interface::$(smname)_Signals::$(signal)_SIG:
$(transitionCode)
                    break;
    """)
            template.signal = signal
            template.transitionCode = transitionCode
            template.smname = smname
            return str(template)
        
        
# -------------------------------------------------------------------------------
# fileHeader
# -------------------------------------------------------------------------------   
        def fileHeader(self, 
                       smname: str, 
                       stateList: List[str], 
                       eventList: List[str], 
                       namespace: str, 
                       implFunctions: List[str]) -> str:
            
            template  = Template("""
// ======================================================================
// \\title  $(smname).h
// \\author Auto-generated by STARS
// \\brief  header file for state machine $smname
//
// ======================================================================
           
#ifndef $(smname.upper())_H_
#define $(smname.upper())_H_
                                
\#include <Fw/Sm/SmSignalBuffer.hpp>
\#include <config/FpConfig.hpp>
                                 
namespace $(namespace) {

class $(smname)_Interface {
  public:
    enum $(smname)_Signals {
#for $event in $eventList
      $event,
#end for
    };

#for $function in $implFunctions
                                 
    virtual $function = 0;
                                 
#end for
                                                                  
};

class $(smname) {
                                 
  private:
    $(smname)_Interface *parent;
                                 
  public:
                                 
    $(smname)($(smname)_Interface* parent) : parent(parent) {}
  
    enum $(smname)_States {
#for $state in $stateList
      $state,
#end for
                                 
    };
                                 
#for $state in $stateList
    void enter_$(state)(const FwEnumStoreType stateMachineId);
#end for
    
    enum $(smname)_States state;

    void init(const FwEnumStoreType stateMachineId);
    void update(
        const FwEnumStoreType stateMachineId, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data
    );
};

}

#endif
""") 
            template.stateList = stateList
            template.eventList = eventList
            template.smname = smname
            template.namespace = namespace
            template.implFunctions = implFunctions
            return str(template)
        
        
        
# -------------------------------------------------------------------------------
# stateMachineInit
# -------------------------------------------------------------------------------           
        def stateMachineInit(self, smname: str, transition: str, namespace: str) -> str:
            template = Template("""
// ======================================================================
// \\title  $(smname).cpp
// \\author Auto-generated by STARS
// \\brief  cpp file for state machine $smname
//
// ======================================================================            
    
\#include <Fw/Types/Assert.hpp>
\#include "$(smname).hpp"


void $(namespace)::$(smname)::init(const FwEnumStoreType stateMachineId)
{
$transition
}


void $(namespace)::$(smname)::update(
    const FwEnumStoreType stateMachineId, 
    const $(smname)_Interface::$(smname)_Signals signal, 
    const Fw::SmSignalBuffer &data
)
{
    switch (this->state) {
    """)
            template.smname = smname
            template.transition = transition
            template.namespace = namespace
            return str(template)
        
# -------------------------------------------------------------------------------
# stateEntryFunction
# -------------------------------------------------------------------------------           
        def stateEntryFunction(self, 
                               namespace: str, 
                               smname: str, 
                               stateName: str, 
                               entryActions: List[str], 
                               initialCode: str) -> str:
            
            template = Template("""

void $namespace::$smname::enter_$(stateName)(const FwEnumStoreType stateMachineId)
{
// State entry actions
#for $action in $entryActions
      parent->$(smname)_$(action)(stateMachineId);
#end for
                                
// Initial transition actions and transition
$initialCode
                
}
    """)
            template.namespace = namespace
            template.smname = smname
            template.stateName = stateName
            template.entryActions = entryActions
            template.initialCode = initialCode
            return str(template)
        

# -------------------------------------------------------------------------------
# stateMachineState
# -------------------------------------------------------------------------------     
        def stateMachineState(self, state: str) -> str:
            template = Template("""
            /**
            * state $state
            */
            case $state:
            
            switch (signal) {
""")
            template.state = state
            return str(template)
        
        
# -------------------------------------------------------------------------------
# stateMachineBreak
# -------------------------------------------------------------------------------       
        def stateMachineBreak(self) -> str:
            template = Template("""
                default:
                    break;
            }
            break;
    """)  
            return str(template)
        
        
# -------------------------------------------------------------------------------
# stateMachineFinalBreak
# -------------------------------------------------------------------------------   
        def stateMachineFinalBreak(self) -> str:
            template = Template("""
                default:
                FW_ASSERT(0);
            }
        }
""")
            return str(template)
