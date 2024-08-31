
#ifndef SEQDISPATCHERIMPL_H_
#define SEQDISPATCHERIMPL_H_

#include "SeqDispatcher.h"
#include <stdbool.h>

typedef struct SeqDispatcherEvent {
    EventSignal super;
    int data1;
    int data2;
} SeqDispatcherEvent;

typedef struct SeqDispatcherImpl {
    SeqDispatcherSM sm;
    bool noWait;
    bool seqRunningNotFile;
} SeqDispatcherImpl;

bool SeqDispatcherImpl_noWait(SeqDispatcherImpl *self, const EventSignal *e);
bool SeqDispatcherImpl_seqRunningNotFile(SeqDispatcherImpl *self, const EventSignal *e);

void SeqDispatcherImpl_unknownSeqFinished(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_incrSeqAvailable(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_decSeqAvailable(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_seqRunOut(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_sendCmdResponse(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_unexpectedSeqStart(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_invalidSequencer(SeqDispatcherImpl *self, const EventSignal *e);
void SeqDispatcherImpl_sendExecutionError(SeqDispatcherImpl *self, const EventSignal *e);

#endif
