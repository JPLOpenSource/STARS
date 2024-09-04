
    
#include <stdio.h>
#include <qf_port.h>
#include <qassert.h>
#include <assert.h>
#include <SeqDispatcherImpl.h>
#include <StatechartSignals.h>

int32_t SeqDispatcherImpl_verbosity_level = 0;

SeqDispatcherImpl *SeqDispatcherImpl_Constructor (SeqDispatcherImpl *mepl) {
    mepl->noWait = 0;
    mepl->seqRunningNotFile = 0;
    return mepl;
}

void SeqDispatcherImpl_set_qactive (SeqDispatcherImpl *mepl, QActive *active) {
    mepl->active = active;
}

int32_t SeqDispatcherImpl_get_verbosity () {
    return SeqDispatcherImpl_verbosity_level;
}

bool SeqDispatcherImpl_noWait(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_noWait() is %d\n", mepl->noWait);
    return mepl->noWait;
}
bool SeqDispatcherImpl_seqRunningNotFile(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_seqRunningNotFile() is %d\n", mepl->seqRunningNotFile);
    return mepl->seqRunningNotFile;
}

void SeqDispatcherImpl_unknownSeqFinished(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_unknownSeqFinished()\n");
}
void SeqDispatcherImpl_incrSeqAvailable(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_incrSeqAvailable()\n");
}
void SeqDispatcherImpl_decSeqAvailable(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_decSeqAvailable()\n");
}
void SeqDispatcherImpl_seqRunOut(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_seqRunOut()\n");
}
void SeqDispatcherImpl_unexpectedSeqStart(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_unexpectedSeqStart()\n");
}
void SeqDispatcherImpl_invalidSequencer(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_invalidSequencer()\n");
}
void SeqDispatcherImpl_sendExecutionError(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_sendExecutionError()\n");
}
void SeqDispatcherImpl_sendCmdResponse(SeqDispatcherImpl *mepl, QEvent *e) {
    printf("SeqDispatcherImpl_sendCmdResponse()\n");
}
