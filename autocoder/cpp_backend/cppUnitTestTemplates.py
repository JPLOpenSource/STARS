#!/bin/env python3
# -----------------------------------------------------------------------
# cUnitTestTemplates.py
#
# A python class that contains template code for the Stars 
# c back-end specific for unit testing
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template #type: ignore
from typing import List, Dict, Tuple, Any, Optional, IO


class CppUnitTestTemplate:
    
# -------------------------------------------------------------------------------
# sendEventHeaderFile for unit test
# -------------------------------------------------------------------------------               
        def sendEventHeaderFile(self, smname: str) -> str:
            template = Template("""        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H

class $smname;

typedef struct EventSignal {
    unsigned int sig;
} EventSignal;

void sendEvent_send(unsigned int signal);

#endif
""")
            template.smname = smname
            return str(template)

# -------------------------------------------------------------------------------
# sendEventFile for unit test
# -------------------------------------------------------------------------------               
        def sendEventFile(self, smname: str, triggerList: List[str]) -> str:
            template = Template("""        
\#include <stdio.h>
\#include <assert.h>
\#include <string.h>
\#include "$(smname).h"
\#include "sendEvent.h"

extern $smname sm;

typedef struct $(smname)Event {
    EventSignal super;
    int data1;
    int data2;
} $(smname)Event;


void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    $(smname)Event event;
    char signalName[100];
    
    switch (signal) {

    #for $sig in $triggerList

    case $(smname)::$(sig):
        strcpy(signalName, "$(sig)");
        break;    
    #end for

    default:
        assert(0);
    }


    printf("\\n--> %s\\n", signalName);
    event.super.sig = signal;
    sm.update(&event.super);
}
""")
            template.smname = smname
            template.triggerList = triggerList
            return str(template)
    
# -------------------------------------------------------------------------------
# testDrv for unit test
# -------------------------------------------------------------------------------               
        def testDrv(self, line: str, smname: str) -> str:
            sendEventTemplate = Template("""    sendEvent_send($(smname)::$(event)_SIG);
""")
            guardTemplate = Template("""    extern bool $(guard)Boolean;
    $(guard)Boolean = $(guardVal);
""")
            
            if '=' in line:
                guardString = line.split('=')
                guardTemplate.guard = guardString[0].strip()
                guardTemplate.guardVal = guardString[1].strip()
                guardTemplate.smname = smname
                return str(guardTemplate)
            elif line.strip() == '':
                return line
            elif '//' in line:
                return "    " + line
            else:
                event = line.strip().upper()
                sendEventTemplate.event = event
                sendEventTemplate.smname = smname
                return str(sendEventTemplate)
            
# -------------------------------------------------------------------------------
# testDrvStart for unit test
# -------------------------------------------------------------------------------               
        def testDrvStart(self, smname: str) -> str:
            template = Template("""
\#include <stdio.h>
\#include "sendEvent.h"
\#include "$(smname).h"

void testDrv() {
""")
          
            template.smname = smname
            return str(template)
                      
 
# -------------------------------------------------------------------------------
# testDrvHeader for unit test
# -------------------------------------------------------------------------------               
        def testDrvHeader(self) -> str:
            template = Template("""
#ifndef _TEST_DRV_H_
#define _TEST_DRV_H_

void testDrv();

#endif
""")
          
            return str(template) 
# -------------------------------------------------------------------------------
# mainFile for unit test
# -------------------------------------------------------------------------------               
        def mainFile(self, smname: str) -> str:
            template = Template("""        
\#include <stdio.h>
\#include "$(smname).h"
\#include "sendEvent.h"
\#include "testDrv.h"


// Instantiate the state-machine
$smname sm;

int main(void) {

    // Initialize the state-machine
    sm.init();

    // Drive the state-machine
    testDrv();

}
""")
            template.smname = smname
            return str(template)

       
