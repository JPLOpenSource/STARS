        
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "Blinky.h"
#include "sendEvent.h"

extern Blinky sm;

typedef struct BlinkyEvent {
    EventSignal super;
    int data1;
    int data2;
} BlinkyEvent;


void sendEvent_send(unsigned int signal) {
    // Instantiate an event
    BlinkyEvent event;
    char signalName[100];
    
    switch (signal) {


    case Blinky::TIMEOUT_SIG:
        strcpy(signalName, "TIMEOUT_SIG");
        break;    

    default:
        assert(0);
    }


    printf("\n--> %s\n", signalName);
    event.super.sig = signal;
    sm.update(&event.super);
}
