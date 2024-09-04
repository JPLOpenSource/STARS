
#include <stdio.h>
#include "sendEvent.h"
#include "SeqDispatcher.h"

void testDrv() {
    sendEvent_send(SeqDispatcher::DONE_SIG);
    extern bool noWaitBoolean;
    noWaitBoolean = true;
    sendEvent_send(SeqDispatcher::RUN_SIG);
    sendEvent_send(SeqDispatcher::START_SIG);
    extern bool seqRunningNotFileBoolean;
    seqRunningNotFileBoolean = true;
    sendEvent_send(SeqDispatcher::START_SIG);
    sendEvent_send(SeqDispatcher::RUN_SIG);
    sendEvent_send(SeqDispatcher::DONE_SIG);
    sendEvent_send(SeqDispatcher::START_SIG);
    sendEvent_send(SeqDispatcher::DONE_SIG);
    extern bool noWaitBoolean;
    noWaitBoolean = false;
    sendEvent_send(SeqDispatcher::RUN_SIG);
    sendEvent_send(SeqDispatcher::RUN_SIG);
    sendEvent_send(SeqDispatcher::DONE_SIG);
}