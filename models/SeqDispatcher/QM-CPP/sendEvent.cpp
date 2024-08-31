        
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "SeqDispatcher.h"
#include "sendEvent.h"

extern SeqDispatcher sm;

typedef struct SeqDispatcherEvent {
    EventSignal super;
    int data1;
    int data2;
} SeqDispatcherEvent;


void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    SeqDispatcherEvent event;
    char signalName[100];
    
    switch (signal) {


    case SeqDispatcher::DONE_SIG:
        strcpy(signalName, "DONE_SIG");
        break;    

    case SeqDispatcher::START_SIG:
        strcpy(signalName, "START_SIG");
        break;    

    case SeqDispatcher::RUN_SIG:
        strcpy(signalName, "RUN_SIG");
        break;    

    default:
        assert(0);
    }


    printf("\n--> %s\n", signalName);
    event.super.sig = signal;
    sm.update(&event.super);
}
