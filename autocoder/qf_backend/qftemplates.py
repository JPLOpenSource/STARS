#!/bin/env python3
# -----------------------------------------------------------------------
# ctemplates.py
#
# A python class that contains template code for the QMAutocoder 
# c back-end 
#
# -----------------------------------------------------------------------
# mypy: ignore-errors

from Cheetah.Template import Template

class QFTemplate:
    
# -------------------------------------------------------------------------------
# target 
# -------------------------------------------------------------------------------   
        def target(self, sm, targ):
            template = Template("""return Q_TRAN(&$(sm)_$(target));""")
            template.sm = sm        
            template.target = targ
            return str(template)

# -------------------------------------------------------------------------------
# action
# -------------------------------------------------------------------------------   
        def action(self, smname, action, args):
            if args == "":
                template = Template("""$(smname)Impl_$(action)(me->impl);""")    
            else:
                template = Template("""$(smname)Impl_$(action)(me->impl, $(args));""")         
  
            template.smname = smname
            template.action = action
            template.args = args
            return str(template)

# -------------------------------------------------------------------------------
# actionSignature
# -------------------------------------------------------------------------------   
        def actionSignature(self, smname, action, args):
            if args == "":
                template = Template("""void $(smname)Impl_$(action)($(smname)Impl *this)""")
            elif args == "e":
                template = Template("""void $(smname)Impl_$(action)($(smname)Impl *mepl, QEvent *e)""")
            elif args.isdigit():
                template = Template("""void $(smname)Impl_$(action)($(smname)Impl *mepl, int arg)""")
            else:
                assert True, "Unknown args"


            template.smname = smname
            template.action = action
            return str(template)

# -------------------------------------------------------------------------------
# ifGuard
# ------------------------------------------------------------------------------- 
        def ifGuard(self, smname, action, args):  
            if args == "":
                template = Template("""if ( $(smname)Impl_$(action)(me->impl) ) {""")    
            else:
                template = Template("""if ( $(smname)Impl_$(action)(me->impl, $(args)) ) {""")       

            template.smname = smname
            template.action = action
            template.args = args
            return str(template)

# -------------------------------------------------------------------------------
# guardSignature
# -------------------------------------------------------------------------------   
        def guardSignature(self, smname, action, args):
            if args == "":
                template = Template("""bool $(smname)Impl_$(action)($(smname)Impl *mepl)""")
            elif args == "e":
                template = Template("""bool $(smname)Impl_$(action)($(smname)Impl *mepl, QEvent *e)""") 
            elif args.isdigit():
                template = Template("""bool $(smname)Impl_$(action)($(smname)Impl *mepl, int arg)""") 
            else:
                assert True, "Unknown args"

            template.smname = smname
            template.action = action
            return str(template)

        
# -------------------------------------------------------------------------------
# stateTransition
# -------------------------------------------------------------------------------   
        def stateTransition(self, signal, transition):
            template = Template("""
    case $(signal):
        $(transition)
        return Q_HANDLED();
    """)
            template.signal = signal
            template.transition = transition
            return str(template)
        
        
# -------------------------------------------------------------------------------
# fileHeader
# -------------------------------------------------------------------------------   
        def fileHeader(self, stateList, smname):
            template  = Template("""
#ifndef $(sm.upper())_H_
#define $(sm.upper())_H_

\#include <stdbool.h>
\#include <qf_port.h>
\#include <qassert.h>
\#include <StatechartSignals.h>
\#include <$(sm)Impl.h>

/**
 * Enumerate all the states that the state machine may be in at any given time.
 * An addition to the Samek pattern, state enums facilitate convenient
 * query of current state a State Machine is in at a given moment.
 */
#set $enum = 0
typedef enum $(sm)_state {
    $(sm.upper())__TOP__, /* Top = 0 */
#for $state in $stateList
#set $enum = $enum + 1
    $(sm.upper())_$state.upper(),    /* State = $enum */
#end for
} $(sm)_state;

/**
 * Declare the state machine struct, encapsulating the extended state variables.
 * It tracks any timers, owned orthogonal regions, history states, substates.
 */
typedef struct $sm {
    QActive super;  // C-style inheritance
    QActive *active;  // containing machine if this is a submachine instance
    $(sm)Impl *impl;
    enum $(sm)_state myState;
} $sm;

/** 
 * $sm Constructor
 *
 * This State machine constructor is responsible for initializing
 * the object, allocating and initializing any orthogonal regions, 
 * and initializing the timers.
 */
$sm *$(sm)_Constructor ($sm *me, $(sm)Impl *implObj, QActive *active);

/**
  * Returns the instance of the Implementation class for this QActive.
  */
$(sm)Impl *$(sm)_getImpl ($sm *me);

/**
 * Returns the unique enum representing the current state of this machine.
 */
$(sm)_state $(sm)_getCurrentState ($sm *me);

/**
 * Method to initialize state machine to the initial pseudostate
 */
QState $(sm)_initial ($sm *me, QEvent *e);

/**
 * State-handler methods
 */
#for $state in $stateList
QState $(sm)_$state ($sm *me, QEvent *e);     
#end for

#endif /* $(sm.upper())_H_ */
""") 
            template.stateList = stateList
            template.sm = smname
            return str(template)
        
        
# -------------------------------------------------------------------------------
# stateMachineInit
# -------------------------------------------------------------------------------           
        def stateMachineInit(self, smname, transition):
            template = Template("""
    
\#include <assert.h>
\#include <$(sm).h>
\#include <$(sm)Impl.h>

/**
 * $sm Constructor
 */
$sm *$(sm)_Constructor ($sm *me, $(sm)Impl *implObj, QActive *active) {
    QActive_ctor((QActive *)me, (QStateHandler )&$(sm)_initial);
    me->impl = implObj;
    if (0 == active) {  // self IS the active object
        me->active = (QActive *)me;
    } else {  // set containing machine as active object
        me->active = active;
    }
    $(sm)Impl_set_qactive(me->impl, me->active);  // give impl access to parent QActive

    // State is initially at TOP
    me->myState = $(sm.upper())__TOP__;

    return me;
}

$(sm)Impl *$(sm)_getImpl ($sm *me) {
    return me->impl;
}

$(sm)_state $(sm)_getCurrentState ($sm *me) {
    return me->myState;
}

/**
 * Initial pseudostate of the state machine.
 *
 * This routine handles initial events of the state-machine.
 */
QState $(sm)_initial ($sm *me, QEvent *e) {
$transition
}
    """)
            template.sm = smname
            template.transition = transition
            """
            template.initial = initial
            if actionList is not None:
                template.actionList = actionList
            """
            return str(template)
        


# -------------------------------------------------------------------------------
# stateMachineState
# -------------------------------------------------------------------------------     
        def stateMachineState(self, sm, stateName, initTransition, stateEntryFunction, stateExitFunction):
            template = Template("""
/**
 * State $stateName
 */
QState $(sm)_$(stateName) ($sm *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = $(sm.upper())_$(stateName.upper());
        $getVar('stateEntryFunction', '')
        return Q_HANDLED();

    case Q_EXIT_SIG:
        $getVar('stateExitFunction', '')
        return Q_HANDLED();
        
    case Q_INIT_SIG:
        $getVar('initTransition', '')
        break;

""")
            
            template.sm = sm
            template.stateName = stateName
            if initTransition is not None:
                template.initTransition = initTransition
            if stateEntryFunction is not None:
                template.stateEntryFunction = stateEntryFunction
            if stateExitFunction is not None:
                template.stateExitFunction = stateExitFunction
            return str(template)
                    



# -------------------------------------------------------------------------------
# stateParent
# -------------------------------------------------------------------------------       
        def stateParent(self, parent):
            template = Template("""
    }
    return Q_SUPER(&$getVar('parent', 'QHsm_top'));
}
""")  
            if parent is not None:
                template.parent = parent
            return str(template)    

# -------------------------------------------------------------------------------
# signals
# -------------------------------------------------------------------------------       
        def signals(self, triggerList):
            template = Template("""
#ifndef STATECHARTSIGNALS_H_
#define STATECHARTSIGNALS_H_

enum StatechartSignals {
    /* "During" signal */
    DURING = Q_USER_SIG,

    /* User defined signals */
#set $enum = 5
#for $signal in $triggerList
    $(signal),  /* $enum */
#set $enum = $enum + 1
#end for
    /* Maximum signal id */
    Q_BAIL_SIG = 0x7FFFFFF-1 /* Internal: terminate region/submachine */,
    MAX_SIG    = 0x7FFFFFF   /* Last possible ID! */
};
#endif /* STATECHARTSIGNALS_H_ */
""") 
            template.triggerList = triggerList 
            return str(template)        
        
        
        
        
