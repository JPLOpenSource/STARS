
            
            
#ifndef _SIGNAL_GEN_HPP_
#define _SIGNAL_GEN_HPP_
                                
#include "Fw/Sm/SmSignalBuffer.hpp"
#include "SeqDispatcher.hpp"
#include <config/FpConfig.hpp>

namespace Ref {

class SignalGen : public SeqDispatcher_Interface {
  public:
      SeqDispatcher sm;
      
      SignalGen() : sm(this) {}
                                
      void init(const FwEnumStoreType stateMachineId);
                                
      bool SeqDispatcher_noWait(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
      bool SeqDispatcher_seqRunningNotFile(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_unknownSeqFinished(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_incrSeqAvailable(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_decSeqAvailable(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_seqRunOut(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_sendCmdResponse(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_unexpectedSeqStart(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_invalidSequencer(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
       void SeqDispatcher_sendExecutionError(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SmSignalBuffer &data) override;
};

}
#endif

