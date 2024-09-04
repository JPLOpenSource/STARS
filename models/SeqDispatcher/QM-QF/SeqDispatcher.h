
#ifndef SEQDISPATCHER_H_
#define SEQDISPATCHER_H_

#include <stdbool.h>
#include <qf_port.h>
#include <qassert.h>
#include <StatechartSignals.h>
#include <SeqDispatcherImpl.h>

/**
 * Enumerate all the states that the state machine may be in at any given time.
 * An addition to the Samek pattern, state enums facilitate convenient
 * query of current state a State Machine is in at a given moment.
 */
typedef enum SeqDispatcher_state {
    SEQDISPATCHER__TOP__, /* Top = 0 */
    SEQDISPATCHER_AVAILABLE,    /* State = 1 */
    SEQDISPATCHER_RUNNING,    /* State = 2 */
    SEQDISPATCHER_RUNNING_BLOCK,    /* State = 3 */
    SEQDISPATCHER_RUNNING_NONBLOCK,    /* State = 4 */
} SeqDispatcher_state;

/**
 * Declare the state machine struct, encapsulating the extended state variables.
 * It tracks any timers, owned orthogonal regions, history states, substates.
 */
typedef struct SeqDispatcher {
    QActive super;  // C-style inheritance
    QActive *active;  // containing machine if this is a submachine instance
    SeqDispatcherImpl *impl;
    enum SeqDispatcher_state myState;
} SeqDispatcher;

/** 
 * SeqDispatcher Constructor
 *
 * This State machine constructor is responsible for initializing
 * the object, allocating and initializing any orthogonal regions, 
 * and initializing the timers.
 */
SeqDispatcher *SeqDispatcher_Constructor (SeqDispatcher *me, SeqDispatcherImpl *implObj, QActive *active);

/**
  * Returns the instance of the Implementation class for this QActive.
  */
SeqDispatcherImpl *SeqDispatcher_getImpl (SeqDispatcher *me);

/**
 * Returns the unique enum representing the current state of this machine.
 */
SeqDispatcher_state SeqDispatcher_getCurrentState (SeqDispatcher *me);

/**
 * Method to initialize state machine to the initial pseudostate
 */
QState SeqDispatcher_initial (SeqDispatcher *me, QEvent *e);

/**
 * State-handler methods
 */
QState SeqDispatcher_Available (SeqDispatcher *me, QEvent *e);     
QState SeqDispatcher_Running (SeqDispatcher *me, QEvent *e);     
QState SeqDispatcher_Running_Block (SeqDispatcher *me, QEvent *e);     
QState SeqDispatcher_Running_NonBlock (SeqDispatcher *me, QEvent *e);     

#endif /* SEQDISPATCHER_H_ */
