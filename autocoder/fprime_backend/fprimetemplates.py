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
                template = Template("""if ( parent->$(smname)_$(action)() ) {""")
            else:
                template = Template("""if (parent->$(smname)_$(action)(signal, data) ) {""")       

            template.smname = smname
            template.action = action
            template.args = args
            return str(template)  

# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""bool $(smname)_$(action)()""")
            elif args == "e":
                template = Template("""bool $(smname)_$(action)(const $(smname)_Interface::$(smname)Events signal, const Fw::SMSignalBuffer &data)""")
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
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)()""")
            elif args == "e":
                template = Template("""bool $(namespace)::$(component)::$(smname)_$(action)(const $(smname)_Interface::$(smname)Events signal, const Fw::SMSignalBuffer &data)""")         

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
                template = Template("""parent->$(smname)_$(action)();""")   
            else:
                template = Template("""parent->$(smname)_$(action)(signal, data);""")         
     
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)


# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""void $(smname)_$(action)()""")
            elif args == "e":
                template = Template("""void $(smname)_$(action)(const $(smname)_Interface::$(smname)Events signal, const Fw::SMSignalBuffer &data)""")
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
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)()""")   
            elif args == "e":
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(const $(smname)_Interface::$(smname)Events signal, const Fw::SMSignalBuffer &data)""")         
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
        def stateTransition(self, signal: str, transition: str, smname) -> str:
            template = Template("""
                case $(smname)_Interface::$(smname)Events::$(signal):
$(transition)
                    break;
    """)
            template.signal = signal
            template.transition = transition
            template.smname = smname
            return str(template)
        
        
# -------------------------------------------------------------------------------
# fileHeader
# -------------------------------------------------------------------------------   
        def fileHeader(self, smname: str, stateList: List[str], eventList: List[str], namespace: str, implFunctions: List[str]) -> str:
            template  = Template("""
// ======================================================================
// \\title  $(smname).h
// \\author Auto-generated
// \\brief  header file for state machine $smname
//
// ======================================================================
           
#ifndef $(smname.upper())_H_
#define $(smname.upper())_H_
                                
\#include <Fw/SMSignal/SMSignalBuffer.hpp>
\#include <config/FpConfig.hpp>
                                 
namespace Fw {
  class SMSignals;
}

namespace $(namespace) {

class $(smname)_Interface {
  public:
    enum $(smname)Events {
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
  
    enum $(smname)States {
#for $state in $stateList
      $state,
#end for
    };
    
    enum $(smname)States state;

    void * extension;

    void init();
    void update(const FwEnumStoreType stateMachineId, const $(smname)_Interface::$(smname)Events signal, const Fw::SMSignalBuffer &data);

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
// \\author Auto-generated
// \\brief  cpp file for state machine $smname
//
// ======================================================================            
    
\#include "stdio.h"
\#include "assert.h"
\#include "Fw/Types/SMSignalsSerializableAc.hpp"
\#include "$(smname).hpp"


void $(namespace)::$(smname)::init()
{
$transition
}


void $(namespace)::$(smname)::update(const FwEnumStoreType stateMachineId, const $(smname)_Interface::$(smname)Events signal, const Fw::SMSignalBuffer &data)
{
    switch (this->state) {
    """)
            template.smname = smname
            template.transition = transition
            template.namespace = namespace
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
        assert(0);
    }
}
""")
            return str(template)

# -------------------------------------------------------------------------------
# smSignals
# -------------------------------------------------------------------------------           
        def smSignalss(self) -> str:

            template = Template("""
# This is an Auto generate file from the STARS Autocoder

module Fw {

    struct SMSignals {
        smId : U32
        eventSignal: U32
        payload: [128] U8
    }

}       
                                
            """)
            return str(template)
        
# -------------------------------------------------------------------------------
# internalQ
# -------------------------------------------------------------------------------           
        def internalQ(self, state_machines) -> str:
            
            template = Template("""
                                
# This is an Auto generate file from the STARS Autocoder
                                
@ internal port for handling state-machine Events
internal port sendEvents(ev: Fw.SMSignals) 
                                
#for $state in $state_machines
    include "$(state.stateName).fppi"
#end for

                                
            """)

            template.state_machines = state_machines
            return str(template)
