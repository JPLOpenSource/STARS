#include <stdio.h>
#include "SignalGen.hpp"
#include "Toggle.h"

extern Ref::SignalGen component;


void testDrv() {
    Svc::SMEvents event;
 
    printf("\n--> %s\n", "EV1_SIG");
    event.seteventSignal(Ref::Simple::EV1_SIG);
    component.simple1.update(&event);
    component.simple2.update(&event);

    printf("\n--> %s\n", "EV1_SIG");
    event.seteventSignal(Ref::Simple::EV1_SIG);
    component.simple1.update(&event);
    component.simple2.update(&event);

    printf("\n--> %s\n", "TOGGLEEV_SIG");
    event.seteventSignal(Ref::Toggle::TOGGLEEV_SIG);
    component.toggle.update(&event);

    printf("\n--> %s\n", "TOGGLEEV_SIG");
    event.seteventSignal(Ref::Toggle::TOGGLEEV_SIG);
    component.toggle.update(&event);
}
