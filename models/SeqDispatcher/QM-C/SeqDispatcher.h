
#ifndef SEQDISPATCHER_H_
#define SEQDISPATCHER_H_


// forward declaration of the state-machine implementation
typedef struct SeqDispatcherImpl SeqDispatcherImpl;
typedef struct SeqDispatcherEvent SeqDispatcherEvent;

enum SeqDispatcherStates {
    Available = 0,
    Block = 1,
    NonBlock = 2,
};

enum SeqDispatcherEvents {
    DONE_SIG = 0,
    START_SIG = 1,
    RUN_SIG = 2,
};

typedef struct SeqDispatcherSM {
    enum SeqDispatcherStates state;
} SeqDispatcherSM;

typedef struct EventSignal {
    unsigned int sig;
} EventSignal;

void SeqDispatcherStateInit(SeqDispatcherImpl *self);
void SeqDispatcherStateUpdate(SeqDispatcherImpl *self, const EventSignal *e);

#endif
