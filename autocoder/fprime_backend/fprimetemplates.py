#!/bin/env python3
# -----------------------------------------------------------------------
# fprimetemplates.py
#
# A python class that contains template code for the Stars 
# fprime back-end 
#
# -----------------------------------------------------------------------
import qmlib
from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO

class FprimeTemplate:
        
        SM_ID = "const FwEnumStoreType stateMachineId"
        full_function_signature = "$(namespace)::$(component)::$(smname)_$(action)"
    
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
        def ifGuard(self, smname: str, guard: str) -> str:  
            guardName, args = qmlib.parse_action(guard)
            if args == "":
                template = Template("""if ( parent->$(smname)_$(guard)(stateMachineId) ) {""")
            else:
                template = Template("""if (parent->$(smname)_$(guard)(stateMachineId, signal, data) ) {""")       

            template.smname = smname
            template.guard = guardName
            return str(template)  

# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname: str, action: str) -> str:
            actionName, args = qmlib.parse_action(action)
            if args == "":
                template = Template(f"""bool $(smname)_$(action)({self.SM_ID})""")
            elif args == "e":
                template = Template(f"""bool $(smname)_$(action)(
        {self.SM_ID}, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")
            elif args.isdigit():
                template = Template("""bool $(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = actionName
            return str(template)

# -------------------------------------------------------------------------------
# guardDef
# -------------------------------------------------------------------------------   
        def guardDef(self, smname: str, action: str, component: str, namespace) -> str:
            actionName, args = qmlib.parse_action(action)
            if args == "":
                template = Template(f"""bool {self.full_function_signature}({self.SM_ID})""")
            elif args == "e":
                template = Template(f"""bool {self.full_function_signature}(
        {self.SM_ID}, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")         

            elif args.isdigit():
                template = Template(f"""bool {self.full_function_signature}(int arg)""")
            else:
                assert True, "Unknown args"

            template.smname = smname
            template.namespace = namespace
            template.action = actionName
            template.component = component
            return str(template)

# -------------------------------------------------------------------------------
# action
# -------------------------------------------------------------------------------   
        def action(self, smname: str, action: str) -> str:
            actionName, args = qmlib.parse_action(action)
            if args == "":
                template = Template(f"""parent->$(smname)_$(action)(stateMachineId);""")   
            else:
                template = Template(f"""parent->$(smname)_$(action)(stateMachineId, signal, data);""")         
     
            template.smname = smname
            template.action = actionName
            return str(template)


# -------------------------------------------------------------------------------
# call_state
# -------------------------------------------------------------------------------   
        def call_state(self, smname: str) -> str:
            template = Template(f"""enter_$(smname)(stateMachineId);""")         
     
            template.smname = smname
            return str(template)


# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname: str, action: str) -> str:
            actionName, args = qmlib.parse_action(action)
            if args == "":
                template = Template(f"""void $(smname)_$(action)({self.SM_ID})""")
            elif args == "e":
                template = Template(f""" void $(smname)_$(action)(
        {self.SM_ID}, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")
            elif args.isdigit():
                template = Template(f"""void $(smname)_$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = actionName
            return str(template)


# -------------------------------------------------------------------------------
# actionDef
# -------------------------------------------------------------------------------   
        def actionDef(self, smname: str, action: str, component: str, namespace: str) -> str:
            actionName, args = qmlib.parse_action(action)

            if args == "":
                template = Template(f"""void {self.full_function_signature}({self.SM_ID})""")   
            elif args == "e":
                template = Template(f"""void {self.full_function_signature}(
        {self.SM_ID}, 
        const $(smname)_Interface::$(smname)_Signals signal, 
        const Fw::SmSignalBuffer &data)""")         
            elif args.isdigit():
                template = Template(f"""void {self.full_function_signature}(int arg)""")         
            else:
                assert True, "Unknown args"
                
            template.namespace = namespace
            template.smname = smname
            template.action = actionName
            template.component = component
            return str(template)

# -------------------------------------------------------------------------------
# stateTransition
# -------------------------------------------------------------------------------   
        def stateTransition(self, signal: str, transitionCode: str, smname) -> str:
            template = Template(f"""
                case $(smname)_Interface::$(smname)_Signals::$(signal.upper())_SIG:
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
      $(event.upper())_SIG,
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
    void enter_$(state)($(smId));
#end for
    
    enum $(smname)_States state;

    void init($(smId));
    void update(
        $(smId), 
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
            template.smId = self.SM_ID
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


void $(namespace)::$(smname)::init($(smId))
{
$transition
}


void $(namespace)::$(smname)::update(
    $(smId), 
    const $(smname)_Interface::$(smname)_Signals signal, 
    const Fw::SmSignalBuffer &data
)
{
    switch (this->state) {
    """)
            template.smname = smname
            template.transition = transition
            template.namespace = namespace
            template.smId = self.SM_ID
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

void $namespace::$smname::enter_$(stateName)($(smId))
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
            template.smId = self.SM_ID
            return str(template)

# -------------------------------------------------------------------------------
# junctionEntryFunction
# -------------------------------------------------------------------------------   
        def junctionEntryFunction(self,
                                  namespace: str, 
                                  smname: str,
                                  stateName: str, 
                                  guard: str, 
                                  ifTarget: str, 
                                  elseTarget: str, 
                                  ifActions: List[str], 
                                  elseActions: List[str]) -> str:
            
            template = Template("""

void $namespace::$smname::enter_$(stateName)($(smId))
{
    if (parent->$(smname)_$(guard)(stateMachineId)) {
#for action in $ifActions
        parent->$(smname)_$(action)(stateMachineId);
#end for
        $ifTarget
    }                      
    else {
#for action in $elseActions
        parent->$(smname)_$(action)(stateMachineId);
#end for
        $elseTarget                   
    }
}
                                
    """)
            template.namespace = namespace
            template.smname = smname
            template.stateName = stateName
            template.guard = guard
            template.ifTarget = ifTarget
            template.elseTarget = elseTarget
            template.ifActions = ifActions
            template.elseActions = elseActions
            template.smId = self.SM_ID
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
