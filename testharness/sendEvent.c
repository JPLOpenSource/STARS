        
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "SimpleImpl.h"

SimpleImpl *self = NULL;

void sendEvent_init(SimpleImpl *impl) {
    self = impl;
}

void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    SimpleEvent event;
    char signalName[100];

    assert(self != NULL);
    
    switch (signal) {


    case EV1_SIG:
        strcpy(signalName, "EV1_SIG");
        break;    

    default:
        assert(0);
    }


    printf("\n--> %s\n", signalName);
    event.super.sig = signal;
    SimpleStateUpdate(self, &event.super);
}
