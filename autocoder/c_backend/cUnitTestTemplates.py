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


class CUnitTestTemplate:
    
# -------------------------------------------------------------------------------
# sendEventHeaderFile for unit test
# -------------------------------------------------------------------------------               
        def sendEventHeaderFile(self, smname: str) -> str:
            template = Template("""        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H
\#include "$(smname)Impl.h"

void sendEvent_init($(smname)Impl *impl);
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
\#include "$(smname)Impl.h"

$(smname)Impl *self = NULL;

void sendEvent_init($(smname)Impl *impl) {
    self = impl;
}

void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    $(smname)Event event;
    char signalName[100];

    assert(self != NULL);
    
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
    $(smname)StateUpdate(self, &event.super);
}
""")
            template.smname = smname
            template.triggerList = triggerList
            return str(template)
    
 
# -------------------------------------------------------------------------------
# testDrv for unit test
# -------------------------------------------------------------------------------               
        def testDrv(self, line: str) -> str:
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
        def testDrvStart(self, smname: str) -> str:
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
        def testDrvHeader(self, smname: str) -> str:
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
# mainFile for unit test
# -------------------------------------------------------------------------------               
        def mainFile(self, smname: str) -> str:
            template = Template("""        
\#include <stdio.h>
\#include "$(smname).h"
\#include "$(smname)Impl.h"
\#include "sendEvent.h"
\#include "testDrv.h"


// Instantiate the state-machine
$(smname)Impl impl;

int main(void) {

    // Initialize the state-machine
    $(smname)StateInit(&impl);

    // Initialize the sendEvent with the implementation
    sendEvent_init(&impl);

    // Drive the state-machine
    testDrv(&impl);

}
""")
            template.smname = smname
            return str(template)

       
