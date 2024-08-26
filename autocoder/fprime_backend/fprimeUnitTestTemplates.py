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
        def sendEventHeaderFile(self, smname, namespace):
            template = Template("""        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H
\#include "$(smname).hpp"

void sendEvent_send($(namespace)::$(smname)::$(smname)Events signal);

#endif
""")
            template.smname = smname
            template.namespace = namespace
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
\#include "Fw/Types/SMSignalsSerializableAc.hpp"
\#include "Fw/SMSignal/SMSignalBuffer.hpp"
\#include "$(implHdr)"
\#include "$(smname).hpp"

extern $(namespace)::$(component) component;


void sendEvent_send($(namespace)::$(smname)::$(smname)Events signal) {
    // Instantiate an event
    char signalName[100];
    Fw::SMSignalBuffer data;
    
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
    component.sm.update(signal, data);
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
            sendEventTemplate = Template("""    sendEvent_send($(namespace)::$(smname)::$(smname)Events::$(event)_SIG);
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
\#include "$(smname).hpp"
\#include "sendEvent.h"
\#include "$(component).hpp"

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

       
