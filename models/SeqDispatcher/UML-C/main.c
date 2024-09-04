        
#include <stdio.h>
#include "SeqDispatcher.h"
#include "SeqDispatcherImpl.h"
#include "sendEvent.h"
#include "testDrv.h"


// Instantiate the state-machine
SeqDispatcherImpl impl;

int main(void) {

    // Initialize the state-machine
    SeqDispatcherStateInit(&impl);

    // Initialize the sendEvent with the implementation
    sendEvent_init(&impl);

    // Drive the state-machine
    testDrv(&impl);

}
