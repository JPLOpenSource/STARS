        
#include <stdio.h>
#include "SeqDispatcher.h"
#include "sendEvent.h"
#include "testDrv.h"


// Instantiate the state-machine
SeqDispatcher sm;

int main(void) {

    // Initialize the state-machine
    sm.init();

    // Drive the state-machine
    testDrv();

}
