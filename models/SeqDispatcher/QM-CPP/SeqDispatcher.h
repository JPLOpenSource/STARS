
#ifndef SEQDISPATCHER_H_
#define SEQDISPATCHER_H_

// forward declaration of EventSignal
struct EventSignal;

class SeqDispatcher {
  public:
  
    enum SeqDispatcherStates {
      Available,
      Block,
      NonBlock,
    };

    enum SeqDispatcherEvents {
      DONE_SIG,
      START_SIG,
      RUN_SIG,
    };
    
    enum SeqDispatcherStates state;

    void init();
    void update(EventSignal *e);
    
    // state machine implementation functions
    bool noWait(EventSignal *e);
    bool seqRunningNotFile(EventSignal *e);
    void unknownSeqFinished(EventSignal *e);
    void incrSeqAvailable(EventSignal *e);
    void decSeqAvailable(EventSignal *e);
    void seqRunOut(EventSignal *e);
    void sendCmdResponse(EventSignal *e);
    void unexpectedSeqStart(EventSignal *e);
    void invalidSequencer(EventSignal *e);
    void sendExecutionError(EventSignal *e);

};

#endif
