
    
#include "SeqDispatcherImpl.h"
#include <stdbool.h>
#include <stdio.h> 

bool SeqDispatcherImpl_noWait(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_noWait() is %d\n", self->noWait);
    return self->noWait;
}
bool SeqDispatcherImpl_seqRunningNotFile(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_seqRunningNotFile() is %d\n", self->seqRunningNotFile);
    return self->seqRunningNotFile;
}

void SeqDispatcherImpl_unknownSeqFinished(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_unknownSeqFinished()\n");
}
void SeqDispatcherImpl_incrSeqAvailable(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_incrSeqAvailable()\n");
}
void SeqDispatcherImpl_decSeqAvailable(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_decSeqAvailable()\n");
}
void SeqDispatcherImpl_seqRunOut(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_seqRunOut()\n");
}
void SeqDispatcherImpl_sendCmdResponse(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_sendCmdResponse()\n");
}
void SeqDispatcherImpl_unexpectedSeqStart(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_unexpectedSeqStart()\n");
}
void SeqDispatcherImpl_invalidSequencer(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_invalidSequencer()\n");
}
void SeqDispatcherImpl_sendExecutionError(SeqDispatcherImpl *self, const EventSignal *e) {
    printf("SeqDispatcherImpl_sendExecutionError()\n");
}
