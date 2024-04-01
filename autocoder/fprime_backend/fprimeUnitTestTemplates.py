#!/bin/env python3
# -----------------------------------------------------------------------
# fprimeUnitTestTemplates.py
#
# A python class that contains template code for the Stars 
# frime back-end specific for unit testing
#
# -----------------------------------------------------------------------

from Cheetah.Template import Template # type: ignore

class FprimeUnitTestTemplate:
    
# -------------------------------------------------------------------------------
# sendEventHeaderFile for unit test
# -------------------------------------------------------------------------------               
        def sendEventHeaderFile(self):
            template = Template("""        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H

void sendEvent_send(unsigned int signal);

#endif
""")
            return str(template)

# -------------------------------------------------------------------------------
# sendEventFile for unit test
# -------------------------------------------------------------------------------               
        def sendEventFile(self, smname, component, namespace, implHdr, triggerList):
            template = Template("""        
\#include <stdio.h>
\#include <assert.h>
\#include <string.h>
\#include "sendEvent.h"
\#include "SMEvents/SMEventsSerializableAc.hpp"
\#include "$(implHdr)"
\#include "$(smname).h"

extern $(namespace)::$(component) component;


void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    Svc::SMEvents event;
    char signalName[100];
    
    switch (signal) {

    #for $sig in $triggerList

    case $(namespace)::$(smname)::$(sig):
        strcpy(signalName, "$(sig)");
        break;    
    #end for

    default:
        assert(0);
    }


    printf("\\n--> %s\\n", signalName);
    event.seteventSignal(signal);
    component.sm.update(&event);
}
""")
            template.smname = smname
            template.component = component
            template.namespace = namespace
            template.implHdr = implHdr
            template.triggerList = triggerList
            return str(template)
    


# -------------------------------------------------------------------------------
# testDrv for unit test
# -------------------------------------------------------------------------------               
        def testDrv(self, line, smname, namespace):
            sendEventTemplate = Template("""    sendEvent_send($(namespace)::$(smname)::$(event)_SIG);
""")
            guardTemplate = Template("""    extern bool $(guard)Boolean;
    $(guard)Boolean = $(guardVal);
""")
            
            if '=' in line:
                guardString = line.split('=')
                guardTemplate.guard = guardString[0].strip()
                guardTemplate.guardVal = guardString[1].strip()
                guardTemplate.smname = smname
                guardTemplate.namespace = namespace
                return str(guardTemplate)
            elif line.strip() == '':
                return line
            elif '//' in line:
                return "    " + line
            else:
                event = line.strip().upper()
                sendEventTemplate.event = event
                sendEventTemplate.smname = smname
                sendEventTemplate.namespace = namespace
                return str(sendEventTemplate)
            
# -------------------------------------------------------------------------------
# testDrvStart for unit test
# -------------------------------------------------------------------------------               
        def testDrvStart(self, smname, component):
            template = Template("""
\#include <stdio.h>
\#include "sendEvent.h"
\#include "$(component).hpp"
\#include "$(smname).h"

void testDrv() {
""")
          
            template.smname = smname
            template.component = component
            return str(template)
                      
 
# -------------------------------------------------------------------------------
# testDrvHeader for unit test
# -------------------------------------------------------------------------------               
        def testDrvHeader(self):
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
        def mainFile(self, implHdr, component, namespace):
            template = Template("""        
\#include <stdio.h>
\#include "sendEvent.h"
\#include "testDrv.h"
\#include "$(implHdr)"


// Instantiate the component
$(namespace)::$(component) component;

int main(void) {

    // Initialize the component
    component.init();

    // Drive the state-machine
    testDrv();

}
""")
            template.implHdr = implHdr
            template.namespace = namespace
            template.component = component
            return str(template)

       
