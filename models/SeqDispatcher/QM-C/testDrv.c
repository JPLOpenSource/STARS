
#include <stdio.h>
#include "SeqDispatcherImpl.h"
#include "sendEvent.h"

void testDrv(SeqDispatcherImpl *impl) {
    sendEvent_send(DONE_SIG);
    impl->noWait= true;
    sendEvent_send(RUN_SIG);
    sendEvent_send(START_SIG);
    impl->seqRunningNotFile= true;
    sendEvent_send(START_SIG);
    sendEvent_send(RUN_SIG);
    sendEvent_send(DONE_SIG);
    sendEvent_send(START_SIG);
    sendEvent_send(DONE_SIG);
    impl->noWait= false;
    sendEvent_send(RUN_SIG);
    sendEvent_send(RUN_SIG);
    sendEvent_send(DONE_SIG);
}