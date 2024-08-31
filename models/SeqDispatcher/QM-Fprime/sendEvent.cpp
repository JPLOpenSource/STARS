        
#include <stdio.h>
#include <assert.h>
#include <string.h>
#include "sendEvent.h"
#include "Fw/Types/SMSignalsSerializableAc.hpp"
#include "Fw/SMSignal/SMSignalBuffer.hpp"
#include "SignalGen.hpp"
#include "SeqDispatcher.hpp"

extern Ref::SignalGen component;


void sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals signal) {
    // Instantiate an event
    char signalName[100];
    Fw::SMSignalBuffer data;
    
    switch (signal) {


    case Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG:
        strcpy(signalName, "DONE_SIG");
        break;    

    case Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG:
        strcpy(signalName, "START_SIG");
        break;    

    case Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG:
        strcpy(signalName, "RUN_SIG");
        break;    

    default:
        assert(0);
    }


    printf("\n--> %s\n", signalName);
    component.sm.update(0, signal, data);
}
