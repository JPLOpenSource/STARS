        
#include <stdio.h>
#include "testDrv.h"
#include "SignalGen.hpp"


// Instantiate the component
Ref::SignalGen component("signalGen");

int main(void) {

    // Initialize the component
    component.init(10, 0);

    // Drive the state-machine
    testDrv();

}
