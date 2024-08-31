
            
#include "SignalGen.hpp"
#include "SeqDispatcher.hpp"
#include "stdio.h"
                                
bool noWaitBoolean;
bool seqRunningNotFileBoolean;


void Ref::SignalGen::init(const FwEnumStoreType stateMachineId) {
    sm.init(stateMachineId);
}
                                
bool Ref::SignalGen::SeqDispatcher_noWait(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_noWait() is %d\n", noWaitBoolean);
    return noWaitBoolean;
}
bool Ref::SignalGen::SeqDispatcher_seqRunningNotFile(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_seqRunningNotFile() is %d\n", seqRunningNotFileBoolean);
    return seqRunningNotFileBoolean;
}

void Ref::SignalGen::SeqDispatcher_unknownSeqFinished(const FwEnumStoreType stateMachineId) {
    printf("SeqDispatcherImpl_unknownSeqFinished()\n");
}
void Ref::SignalGen::SeqDispatcher_incrSeqAvailable(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_incrSeqAvailable()\n");
}
void Ref::SignalGen::SeqDispatcher_seqRunOut(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_seqRunOut()\n");
}
void Ref::SignalGen::SeqDispatcher_decSeqAvailable(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_decSeqAvailable()\n");
}
void Ref::SignalGen::SeqDispatcher_unexpectedSeqStart(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_unexpectedSeqStart()\n");
}
void Ref::SignalGen::SeqDispatcher_invalidSequencer(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_invalidSequencer()\n");
}
void Ref::SignalGen::SeqDispatcher_sendExecutionError(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_sendExecutionError()\n");
}
void Ref::SignalGen::SeqDispatcher_sendCmdResponse(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) {
    printf("SeqDispatcherImpl_sendCmdResponse()\n");
}

