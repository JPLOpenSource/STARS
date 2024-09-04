        
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "SeqDispatcherImpl.h"

SeqDispatcherImpl *self = NULL;

void sendEvent_init(SeqDispatcherImpl *impl) {
    self = impl;
}

void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    SeqDispatcherEvent event;
    char signalName[100];

    assert(self != NULL);
    
    switch (signal) {


    case DONE_SIG:
        strcpy(signalName, "DONE_SIG");
        break;    

    case RUN_SIG:
        strcpy(signalName, "RUN_SIG");
        break;    

    case START_SIG:
        strcpy(signalName, "START_SIG");
        break;    

    default:
        assert(0);
    }


    printf("\n--> %s\n", signalName);
    event.super.sig = signal;
    SeqDispatcherStateUpdate(self, &event.super);
}
