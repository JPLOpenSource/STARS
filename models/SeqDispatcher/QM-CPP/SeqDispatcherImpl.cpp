
    
#include <stdbool.h>
#include <stdio.h> 

#include "SeqDispatcher.h"

bool noWaitBoolean;
bool seqRunningNotFileBoolean;

bool SeqDispatcher::noWait(EventSignal *e) {
    printf("SeqDispatcherImpl_noWait() is %d\n", noWaitBoolean);
    return noWaitBoolean;
}
bool SeqDispatcher::seqRunningNotFile(EventSignal *e) {
    printf("SeqDispatcherImpl_seqRunningNotFile() is %d\n", seqRunningNotFileBoolean);
    return seqRunningNotFileBoolean;
}

void SeqDispatcher::unknownSeqFinished(EventSignal *e) {
    printf("SeqDispatcherImpl_unknownSeqFinished()\n");
}
void SeqDispatcher::incrSeqAvailable(EventSignal *e) {
    printf("SeqDispatcherImpl_incrSeqAvailable()\n");
}
void SeqDispatcher::decSeqAvailable(EventSignal *e) {
    printf("SeqDispatcherImpl_decSeqAvailable()\n");
}
void SeqDispatcher::seqRunOut(EventSignal *e) {
    printf("SeqDispatcherImpl_seqRunOut()\n");
}
void SeqDispatcher::sendCmdResponse(EventSignal *e) {
    printf("SeqDispatcherImpl_sendCmdResponse()\n");
}
void SeqDispatcher::unexpectedSeqStart(EventSignal *e) {
    printf("SeqDispatcherImpl_unexpectedSeqStart()\n");
}
void SeqDispatcher::invalidSequencer(EventSignal *e) {
    printf("SeqDispatcherImpl_invalidSequencer()\n");
}
void SeqDispatcher::sendExecutionError(EventSignal *e) {
    printf("SeqDispatcherImpl_sendExecutionError()\n");
}
