        
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "SeqDispatcher.h"
#include "StatechartSignals.h"

SeqDispatcher *this = NULL;

void sendEvent_init(SeqDispatcher* sm) {
    this = sm;
}


void sendEvent_send(QSignal signal) {
    // Instantiate an event
    QEventData event;
    char signalName[100];

    assert(this != NULL);
    
    switch (signal) {


    case DONE_SIG:
        strcpy(signalName, "DONE_SIG");
        break;    

    case START_SIG:
        strcpy(signalName, "START_SIG");
        break;    

    case RUN_SIG:
        strcpy(signalName, "RUN_SIG");
        break;    

    default:
        assert(0);
    }

    printf("\n--> %s\n", signalName);
    event.super.sig = signal;
    QHsm_dispatch((QHsm*)this, &event.super);
}
