#!/bin/env python3
# -----------------------------------------------------------------------
# ctemplates.py
#
# A python class that contains template code for the Stars 
# c back-end 
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO


class CTemplate:
    
# -------------------------------------------------------------------------------
# target
# -------------------------------------------------------------------------------   
        def target(self, targ: str) -> str:
            
            template = Template("""self->sm.state = $(target);""")
                     
            template.target = targ
            return str(template)
        

# -------------------------------------------------------------------------------
# ifGuard
# -------------------------------------------------------------------------------  
        def ifGuard(self, smname: str, action: str, args: str) -> str: 
            if args == "":
                template = Template("""if ($(smname)Impl_$(action)(self) ) {""")   
            else:
                 template = Template("""if ($(smname)Impl_$(action)(self, $(args)) ) {""")   

            template.smname = smname
            template.action = action
            template.args = args
            return str(template)

# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":
                template = Template("""bool $(smname)Impl_$(action)($(smname)Impl *self)""")
            elif args == "e":
                template = Template("""bool $(smname)Impl_$(action)($(smname)Impl *self, const EventSignal *e)""")
            elif args.isdigit():
                template = Template("""bool $(smname)Impl_$(action)($(smname)Impl *self, int arg)""")
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
                template = Template("""$(smname)Impl_$(action)(self);""")   
            else:
                template = Template("""$(smname)Impl_$(action)(self, $(args));""")
 
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)

# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname: str, action: str, args: str) -> str:
            if args == "":    
                template = Template("""void $(smname)Impl_$(action)($(smname)Impl *self)""")
            elif args == "e":
                template = Template("""void $(smname)Impl_$(action)($(smname)Impl *self, const EventSignal *e)""")
            elif args.isdigit():
                template = Template("""void $(smname)Impl_$(action)($(smname)Impl *self, int arg)""")
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
        def fileHeader(self, smname: str, stateList: List[str], eventList: List[str]) -> str:
            template  = Template("""
#ifndef $(smname.upper())_H_
#define $(smname.upper())_H_


// forward declaration of the state-machine implementation
typedef struct $(smname)Impl $(smname)Impl;
typedef struct $(smname)Event $(smname)Event;

enum $(smname)States {
#set $index = 0
#for $state in $stateList
    $state = $index,
    #set $index = $index + 1
#end for
};

#set $index = 0
enum $(smname)Events {
#for $event in $eventList
    $event = $index,
    #set $index = $index + 1
#end for
};

typedef struct $(smname)SM {
    enum $(smname)States state;
} $(smname)SM;

typedef struct EventSignal {
    unsigned int sig;
} EventSignal;

void $(smname)StateInit($(smname)Impl *self);
void $(smname)StateUpdate($(smname)Impl *self, const EventSignal *e);

#endif
""") 
            template.stateList = stateList
            template.eventList = eventList
            template.smname = smname
            return str(template)
        
        
        
# -------------------------------------------------------------------------------
# stateMachineInit
# -------------------------------------------------------------------------------           
        def stateMachineInit(self, smname: str, transition: str) -> str:
            template = Template("""
    
\#include "stdio.h"
\#include "assert.h"
\#include "$(smname).h"
\#include "$(smname)Impl.h"

void $(smname)StateInit($(smname)Impl *self)
{
$transition
}


void $(smname)StateUpdate($(smname)Impl *self, const EventSignal *e)
{
    switch (self->sm.state) {
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

