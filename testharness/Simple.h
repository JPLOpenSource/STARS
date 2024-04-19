
#ifndef SIMPLE_H_
#define SIMPLE_H_


// forward declaration of the state-machine implementation
typedef struct SimpleImpl SimpleImpl;
typedef struct SimpleEvent SimpleEvent;

enum SimpleStates {
    S1 = 0,
    S2 = 1,
};

enum SimpleEvents {
    EV1_SIG = 0,
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
