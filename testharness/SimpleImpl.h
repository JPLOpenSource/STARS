
#ifndef SIMPLEIMPL_H_
#define SIMPLEIMPL_H_

#include "Simple.h"
#include <stdbool.h>

typedef struct SimpleEvent {
    EventSignal super;
    int data1;
    int data2;
} SimpleEvent;

typedef struct SimpleImpl {
    SimpleSM sm;
} SimpleImpl;


void SimpleImpl_s1Entry(SimpleImpl *self);

#endif
