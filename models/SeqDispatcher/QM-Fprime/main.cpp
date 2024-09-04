        
#include <stdio.h>
#include "sendEvent.h"
#include "testDrv.h"
#include "SignalGen.hpp"


// Instantiate the component
Ref::SignalGen component;

int main(void) {

    // Initialize the component
    component.init(0);

    // Drive the state-machine
    testDrv();

}
