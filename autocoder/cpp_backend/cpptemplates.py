#!/bin/env python3
# -----------------------------------------------------------------------
# ctemplates.py
#
# A python class that contains template code for the QMAutocoder 
# c++ back-end 
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO

class CppTemplate:
    
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
                template = Template("""if ($(action)() ) {""")
            else:
                template = Template("""if ($(action)($(args)) ) {""")
     
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)
     
# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname: str, action: str, actions: str) -> str:
            if actions == "":
                template = Template("""bool $(action)()""")
            elif actions == "e":
                template = Template("""bool $(action)(EventSignal *e)""")
            elif actions.isdigit():
                template = Template("""bool $(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)


# -------------------------------------------------------------------------------
# guardDef
# -------------------------------------------------------------------------------   
        def guardDef(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""bool $(smname)::$(action)()""")
            elif args == "e":
                template = Template("""bool $(smname)::$(action)(EventSignal *e)""")
            elif args.isdigit():
                template = Template("""bool $(smname)::$(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)

# -------------------------------------------------------------------------------
# nActionSignature
# -------------------------------------------------------------------------------   
        def actionDef(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""void $(smname)::$(action)()""")       
            elif args == "e":
                template = Template("""void $(smname)::$(action)(EventSignal *e)""")  
            elif args.isdigit():
                template = Template("""void $(smname)::$(action)(int arg)""") 
            else:
                assert True, "Unknown args" 

            template.smname = smname
            template.action = action
            return str(template)

# -------------------------------------------------------------------------------
# action
# -------------------------------------------------------------------------------   
        def action(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""$(action)();""")       
            else:
                template = Template("""$(action)($(args));""")
 
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)
        
        
# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""void $(action)()""")
            elif args == "e":
                template = Template("""void $(action)(EventSignal *e)""")
            elif args.isdigit():
                template = Template("""void $(action)(int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
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
        def fileHeader(self, smname: str, stateList: List[str], eventList: List[str], implFunctions: List[str]) -> str:
            template  = Template("""
#ifndef $(smname.upper())_H_
#define $(smname.upper())_H_

// forward declaration of EventSignal
struct EventSignal;

class $(smname) {
  public:
  
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

    void init();
    void update(EventSignal *e);
    
    // state machine implementation functions
    #for $function in $implFunctions
    $function;
    #end for

};

#endif
""") 
            template.stateList = stateList
            template.eventList = eventList
            template.smname = smname
            template.implFunctions = implFunctions
            return str(template)
        
        
        
# -------------------------------------------------------------------------------
# stateMachineInit
# -------------------------------------------------------------------------------           
        def stateMachineInit(self, smname: str, transition: str) -> str:
            template = Template("""
    
\#include "stdio.h"
\#include "assert.h"
\#include "$(smname).h"
\#include "sendEvent.h"

void $(smname)::init()
{
$transition
}


void $(smname)::update(EventSignal *e)
{
    switch (this->state) {
    """)
            template.smname = smname
            template.transition = transition
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
            
            switch (e->sig) {
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

