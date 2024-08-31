
#include <stdio.h>
#include "SeqDispatcher.hpp"
#include "sendEvent.h"
#include "SignalGen.hpp"

void testDrv() {
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG);
    extern bool noWaitBoolean;
    noWaitBoolean = true;
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG);
    extern bool seqRunningNotFileBoolean;
    seqRunningNotFileBoolean = true;
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG);
    extern bool noWaitBoolean;
    noWaitBoolean = false;
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG);
    sendEvent_send(Ref::SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG);
}