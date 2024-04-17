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
                template = Template("""if (parent->$(smname)_$(action)($(args)) ) {""")       

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
                template = Template("""bool $(smname)_$(action)(const Svc::SMEvents *e)""")
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
                template = Template("""bool $($namespace)::$(component)::$(smname)_$(action)(const Svc::SMEvents *e)""")
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
                template = Template("""parent->$(smname)_$(action)($(args));""")         
     
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
                template = Template("""void $(smname)_$(action)(const Svc::SMEvents *e)""")
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
                template = Template("""void $(namespace)::$(component)::$(smname)_$(action)(const Svc::SMEvents *e)""")         
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
        def stateTransition(self, signal: str, transition: str) -> str:
            template = Template("""
                case $(signal):
$(transition)
                    break;
    """)
            template.signal = signal
            template.transition = transition
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
// \\copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================
           
#ifndef $(smname.upper())_H_
#define $(smname.upper())_H_

namespace Svc {
  class SMEvents;
}

namespace $(namespace) {

class $(smname)If {
  public:
    #for $function in $implFunctions
    virtual $function = 0;
    #end for
                                                                  
};

class $(smname) {
                                 
  private:
    $(smname)If *parent;
                                 
  public:
                                 
    $(smname)($(smname)If* parent) : parent(parent) {}
  
    enum $(smname)States {
#for $state in $stateList
      $state,
#end for
    };

    enum $(smname)Events {
#for $event in $eventList
      $event,
#end for
    };
    
    enum $(smname)States state;

    void * extension;

    void init();
    void update(const Svc::SMEvents *e);

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
// \\copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================            
    
\#include "stdio.h"
\#include "assert.h"
\#include "SMEvents.hpp"
\#include "$(smname).h"


void $(namespace)::$(smname)::init()
{
$transition
}


void $(namespace)::$(smname)::update(const Svc::SMEvents *e)
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
            
            switch (e->geteventSignal()) {
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
# smBaseHeader
# -------------------------------------------------------------------------------           
        def smBaseHeader(self, 
                        state_machines,
                        nameSpace: str,
                        component: str,
                        componentPath: str,
                        autoHeaderFile: str,
                        componentBase: str) -> str: 
            template = Template("""
#ifndef $(component.upper())_SM_BASE_HPP
#define $(component.upper())_SM_BASE_HPP
// ======================================================================
// \\title  $(component)SmBase.hpp
// \\author Auto-generated
// \\brief  Header file for the state machine base class
//
// \\copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================            
\#include "$(componentPath)/$(autoHeaderFile)"
#for $state in $state_machines
\#include "$(componentPath)/$(state.stateName).h"
#end for
                                
namespace $nameSpace {
    namespace StateMachine {
        typedef enum {
        #for $state in $state_machines
            #for $impl in $state.stateMachineInstance
            $(impl.upper()),
            #end for
        #end for
        } SmId;                           
    };

    class $(component)SmBase : public $(componentBase)
    #for $state in $state_machines
        ,public $(state.stateName)If
    #end for
                                
    {
        public:
            $(component)SmBase(const char* const compName);
            void init(
                        NATIVE_INT_TYPE queueDepth,
                        NATIVE_INT_TYPE instance
            );
            
            // Interface to send an event to the state-machine
            void sendEvent(U32 eventSignal, StateMachine::SmId id);

            // Internal Interface handler for sendEvents
            void sendEvents_internalInterfaceHandler(const Svc::SMEvents& ev);
                                
            // Instantiate the state machines
            #for $state in $state_machines
                #for $impl in $state.stateMachineInstance
            $state.stateName $(impl);
                #end for
            #end for
            
                                
    };
}
#endif

            """)
            template.state_machines = state_machines
            template.nameSpace = nameSpace
            template.component = component
            template.componentPath = componentPath
            template.autoHeaderFile = autoHeaderFile
            template.componentBase = componentBase
            return str(template)
        
# -------------------------------------------------------------------------------
# smBaseCpp
# -------------------------------------------------------------------------------           
        def smBaseCpp(self,
                      state_machines,
                      nameSpace: str,
                      component: str,
                      componentPath: str,
                      autoHeaderFile: str,
                      componentBase: str) -> str: 
            template = Template("""
// ======================================================================
// \\title  $(component)SmBase.cpp
// \\author Auto-generated
// \\brief  Cpp file for the state machine base class
//
// \\copyright
// Copyright 2009-2015, by the California Institute of Technology.
// ALL RIGHTS RESERVED.  United States Government Sponsorship
// acknowledged.
//
// ======================================================================            
\#include "$(componentPath)/$(component)SmBase.hpp"
#for $state in $state_machines
\#include "$(componentPath)/$(state.stateName).h"
#end for
                                
$(nameSpace)::$(component)SmBase::$(component)SmBase(const char* const compName):
    $(componentBase)(compName)
    #for $state in $state_machines
        #for $impl in $state.stateMachineInstance
    ,$(impl)(this)
        #end for
    #end for
{
                                
}                               

void $(nameSpace)::$(component)SmBase::init(
            NATIVE_INT_TYPE queueDepth,
            NATIVE_INT_TYPE instance)
{
    $(componentBase)::init(queueDepth, instance);
                                
    // Initialize the state machine
    #for $state in $state_machines
        #for $impl in $state.stateMachineInstance
    $(impl).init();
        #end for
    #end for
    
} 

void $(nameSpace)::$(component)SmBase:: sendEvent(U32 eventSignal, StateMachine::SmId id) {
                                
    Svc::SMEvents event;
    event.seteventSignal(eventSignal);
    event.setsmId(id);
    sendEvents_internalInterfaceInvoke(event);
}

void $(nameSpace)::$(component)SmBase::sendEvents_internalInterfaceHandler(const Svc::SMEvents& ev)
{
    U16 id = ev.getsmId();
    switch (id) {
                                
        #for $state in $state_machines
            #for $impl in $state.stateMachineInstance
        case StateMachine::$impl.upper():
            this->$(impl).update(&ev);
            break;
            #end for
        #end for
        default:
            FW_ASSERT(0);
    }

}
            """)
            template.state_machines = state_machines
            template.nameSpace = nameSpace
            template.component = component
            template.componentPath = componentPath
            template.autoHeaderFile = autoHeaderFile
            template.componentBase = componentBase
            return str(template)
        
# -------------------------------------------------------------------------------
# smEvents
# -------------------------------------------------------------------------------           
        def smEvents(self) -> str:

            template = Template("""
# This is an Auto generate file from the STARS Autocoder

module Svc {

    struct SMEvents {
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
internal port sendEvents(ev: Svc.SMEvents) 
                                
#for $state in $state_machines
    include "$(state.stateName).fppi"
#end for

                                
            """)

            template.state_machines = state_machines
            return str(template)
