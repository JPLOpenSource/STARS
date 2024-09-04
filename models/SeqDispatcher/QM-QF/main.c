    
#include <stdio.h>
#include "SeqDispatcher.h"
#include "SeqDispatcherImpl.h"
#include "sendEvent.h"
#include "testDrv.h"

// Instantiate the state-machine and implementation
SeqDispatcherImpl impl;
SeqDispatcher sm;


int main(void) {

    // Initialize the state-machine and implementation
    SeqDispatcherImpl_Constructor(&impl);
    SeqDispatcher_Constructor(&sm, &impl, 0);
    QHsm_init(&(sm.super.super), 0);

    // Initialize the sendEvent with the implementation
    sendEvent_init(&sm);

    // Drive the state-machine
    testDrv(&impl);
}
