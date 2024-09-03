
// ======================================================================
// \title  SeqDispatcher.h
// \author Auto-generated
// \brief  header file for state machine SeqDispatcher
//
// ======================================================================
           
#ifndef SEQDISPATCHER_H_
#define SEQDISPATCHER_H_
                                
#include <Fw/Sm/SMSignalBuffer.hpp>
#include <config/FpConfig.hpp>
                                 
namespace Ref {

class SeqDispatcher_Interface {
  public:
    enum SeqDispatcher_Signals {
      DONE_SIG,
      RUN_SIG,
      START_SIG,
    };

                                 
    virtual bool SeqDispatcher_noWait(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual bool SeqDispatcher_seqRunningNotFile(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual void SeqDispatcher_unknownSeqFinished(const FwEnumStoreType stateMachineId) = 0;
                                 
                                 
    virtual  void SeqDispatcher_incrSeqAvailable(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual  void SeqDispatcher_seqRunOut(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual  void SeqDispatcher_decSeqAvailable(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual  void SeqDispatcher_unexpectedSeqStart(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual  void SeqDispatcher_invalidSequencer(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual  void SeqDispatcher_sendExecutionError(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                 
    virtual  void SeqDispatcher_sendCmdResponse(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data) = 0;
                                 
                                                                  
};

class SeqDispatcher {
                                 
  private:
    SeqDispatcher_Interface *parent;
                                 
  public:
                                 
    SeqDispatcher(SeqDispatcher_Interface* parent) : parent(parent) {}
  
    enum SeqDispatcher_States {
      Available,
      NonBlock,
      Block,
    };
    
    enum SeqDispatcher_States state;

    void init(const FwEnumStoreType stateMachineId);
    void update(
        const FwEnumStoreType stateMachineId, 
        const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
        const Fw::SMSignalBuffer &data
    );
};

}

#endif
