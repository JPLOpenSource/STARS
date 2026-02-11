
#ifndef SIMPLE_H_
#define SIMPLE_H_


// forward declaration of the state-machine implementation
typedef struct SimpleImpl SimpleImpl;
typedef struct SimpleEvent SimpleEvent;

enum SimpleStates {
    State1 = 0,
    State2 = 1,
    State3 = 2,
    State4 = 3,
};

enum SimpleEvents {
    EV1_SIG = 0,
    EV2_SIG = 1,
    EV4_SIG = 2,
    EV3_SIG = 3,
    EV5_SIG = 4,
};

typedef struct SimpleSM {
    enum SimpleStates state;
} SimpleSM;

typedef struct EventSignal {
    unsigned int sig;
} EventSignal;

void SimpleStateInit(SimpleImpl *self);
void SimpleStateUpdate(SimpleImpl *self, const EventSignal *e);

#endif
