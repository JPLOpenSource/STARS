#!/bin/env python3
# -----------------------------------------------------------------------
# ctemplates.py
#
# A python class that contains template code for the Stars 
# c back-end 
#
# -----------------------------------------------------------------------
# mypy: ignore-errors

from Cheetah.Template import Template

class QFUnitTestTemplate:
    
       
# -------------------------------------------------------------------------------
# sendEventFile for unit test
# -------------------------------------------------------------------------------               
        def sendEventFile(self, smname, triggerList):
            template = Template("""        
\#include <stdio.h>
\#include <assert.h>
\#include <string.h>
\#include "$(smname).h"
\#include "StatechartSignals.h"

$(smname) *this = NULL;

void sendEvent_init($(smname)* sm) {
    this = sm;
}


void sendEvent_send(QSignal signal) {
    // Instantiate an event
    QEventData event;
    char signalName[100];

    assert(this != NULL);
    
    switch (signal) {

    #for $sig in $triggerList

    case $(sig):
        strcpy(signalName, "$(sig)");
        break;    
    #end for

    default:
        assert(0);
    }

    printf("\\n--> %s\\n", signalName);
    event.super.sig = signal;
    QHsm_dispatch((QHsm*)this, &event.super);
}
""")
            template.smname = smname
            template.triggerList = triggerList
            return str(template)
    
# -------------------------------------------------------------------------------
# sendEventHeaderFile
# -------------------------------------------------------------------------------               
        def sendEventHeaderFile(self, smname):
            template = Template("""        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H
\#include "$(smname).h"

void sendEvent_init($(smname) *sm);
void sendEvent_send(QSignal signal);

#endif
""")
            template.smname = smname
            return str(template)
 
# -------------------------------------------------------------------------------
# testDrv for unit test
# -------------------------------------------------------------------------------               
        def testDrv(self, line):
            sendEventTemplate = Template("""    sendEvent_send($(event)_SIG);
""")
            guardTemplate = Template("""    impl->$(guard)= $(guardVal);
""")
            
            if '=' in line:
                guardString = line.split('=')
                guardTemplate.guard = guardString[0].strip()
                guardTemplate.guardVal = guardString[1].strip()
                return str(guardTemplate)
            elif line.strip() == '':
                return line
            elif '//' in line:
                return "    " + line
            else:
                event = line.strip().upper()
                sendEventTemplate.event = event
                return str(sendEventTemplate)
            
# -------------------------------------------------------------------------------
# testDrvStart for unit test
# -------------------------------------------------------------------------------               
        def testDrvStart(self, smname):
            template = Template("""
\#include <stdio.h>
\#include "$(smname)Impl.h"
\#include "sendEvent.h"

void testDrv($(smname)Impl *impl) {
""")
          
            template.smname = smname
            return str(template)
                      
 
# -------------------------------------------------------------------------------
# testDrvHeader for unit test
# -------------------------------------------------------------------------------               
        def testDrvHeader(self, smname):
            template = Template("""
#ifndef _TEST_DRV_H_
#define _TEST_DRV_H_
\#include "$(smname)Impl.h"
\#include "sendEvent.h"

void testDrv($(smname)Impl *impl);

#endif
""")
          
            template.smname = smname
            return str(template)
    
# -------------------------------------------------------------------------------
# mainFile
# -------------------------------------------------------------------------------               
        def mainFile(self, smname):
            template = Template("""    
\#include <stdio.h>
\#include "$(smname).h"
\#include "$(smname)Impl.h"
\#include "sendEvent.h"
\#include "testDrv.h"

// Instantiate the state-machine and implementation
$(smname)Impl impl;
$(smname) sm;


int main(void) {

    // Initialize the state-machine and implementation
    $(smname)Impl_Constructor(&impl);
    $(smname)_Constructor(&sm, &impl, 0);
    QHsm_init(&(sm.super.super), 0);

    // Initialize the sendEvent with the implementation
    sendEvent_init(&sm);

    // Drive the state-machine
    testDrv(&impl);
}
""")
            template.smname = smname
            return str(template)
        
 
               
               
        