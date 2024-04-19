        
#include <stdio.h>
#include "Simple.h"
#include "SimpleImpl.h"
#include "sendEvent.h"
#include "testDrv.h"


// Instantiate the state-machine
SimpleImpl impl;

int main(void) {

    // Initialize the state-machine
    SimpleStateInit(&impl);

    // Initialize the sendEvent with the implementation
    sendEvent_init(&impl);

    // Drive the state-machine
    testDrv(&impl);

}
