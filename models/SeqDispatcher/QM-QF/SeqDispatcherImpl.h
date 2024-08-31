
#ifndef SEQDISPATCHERIMPL_H_
#define SEQDISPATCHERIMPL_H_

#include <qf_port.h>
#include <qassert.h>

typedef struct QEventData {
    QEvent super;
    int data1;
    int data2;
} QEventData;

typedef struct SeqDispatcherImpl {
    QActive *active;
    bool noWait;
    bool seqRunningNotFile;
} SeqDispatcherImpl;

SeqDispatcherImpl *SeqDispatcherImpl_Constructor (SeqDispatcherImpl *mepl);  // Default constructor
void SeqDispatcherImpl_set_qactive (SeqDispatcherImpl *mepl, QActive *active);
int32_t SeqDispatcherImpl_get_verbosity ();

bool SeqDispatcherImpl_noWait(SeqDispatcherImpl *mepl, QEvent *e);
bool SeqDispatcherImpl_seqRunningNotFile(SeqDispatcherImpl *mepl, QEvent *e);

void SeqDispatcherImpl_unknownSeqFinished(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_incrSeqAvailable(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_decSeqAvailable(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_seqRunOut(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_unexpectedSeqStart(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_invalidSequencer(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_sendExecutionError(SeqDispatcherImpl *mepl, QEvent *e);
void SeqDispatcherImpl_sendCmdResponse(SeqDispatcherImpl *mepl, QEvent *e);

#endif
