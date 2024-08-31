
    
#include <assert.h>
#include <SeqDispatcher.h>
#include <SeqDispatcherImpl.h>

/**
 * SeqDispatcher Constructor
 */
SeqDispatcher *SeqDispatcher_Constructor (SeqDispatcher *me, SeqDispatcherImpl *implObj, QActive *active) {
    QActive_ctor((QActive *)me, (QStateHandler )&SeqDispatcher_initial);
    me->impl = implObj;
    if (0 == active) {  // self IS the active object
        me->active = (QActive *)me;
    } else {  // set containing machine as active object
        me->active = active;
    }
    SeqDispatcherImpl_set_qactive(me->impl, me->active);  // give impl access to parent QActive

    // State is initially at TOP
    me->myState = SEQDISPATCHER__TOP__;

    return me;
}

SeqDispatcherImpl *SeqDispatcher_getImpl (SeqDispatcher *me) {
    return me->impl;
}

SeqDispatcher_state SeqDispatcher_getCurrentState (SeqDispatcher *me) {
    return me->myState;
}

/**
 * Initial pseudostate of the state machine.
 *
 * This routine handles initial events of the state-machine.
 */
QState SeqDispatcher_initial (SeqDispatcher *me, QEvent *e) {
    return Q_TRAN(&SeqDispatcher_Available);

}
    
/**
 * State Available
 */
QState SeqDispatcher_Available (SeqDispatcher *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = SEQDISPATCHER_AVAILABLE;
        
        return Q_HANDLED();

    case Q_EXIT_SIG:
        
        return Q_HANDLED();
        
    case Q_INIT_SIG:
        
        break;


    case DONE_SIG:
            SeqDispatcherImpl_unknownSeqFinished(me->impl, e);
    SeqDispatcherImpl_incrSeqAvailable(me->impl, e);

        return Q_HANDLED();
    
    case START_SIG:
            SeqDispatcherImpl_decSeqAvailable(me->impl, e);
    return Q_TRAN(&SeqDispatcher_Running);

        return Q_HANDLED();
    
    case RUN_SIG:
            SeqDispatcherImpl_seqRunOut(me->impl, e);
    SeqDispatcherImpl_decSeqAvailable(me->impl, e);
    if ( SeqDispatcherImpl_noWait(me->impl, e) ) {
        return Q_TRAN(&SeqDispatcher_Running_NonBlock);
    }
    else {
        return Q_TRAN(&SeqDispatcher_Running_Block);
    }

        return Q_HANDLED();
    
    }
    return Q_SUPER(&QHsm_top);
}

/**
 * State Running
 */
QState SeqDispatcher_Running (SeqDispatcher *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = SEQDISPATCHER_RUNNING;
        
        return Q_HANDLED();

    case Q_EXIT_SIG:
        
        return Q_HANDLED();
        
    case Q_INIT_SIG:
            return Q_TRAN(&SeqDispatcher_Running_NonBlock);

        break;


    case START_SIG:
            if ( SeqDispatcherImpl_seqRunningNotFile(me->impl, e) ) {
        SeqDispatcherImpl_unexpectedSeqStart(me->impl, e);
    }

        return Q_HANDLED();
    
    case RUN_SIG:
            SeqDispatcherImpl_invalidSequencer(me->impl, e);
    SeqDispatcherImpl_sendExecutionError(me->impl, e);

        return Q_HANDLED();
    
    }
    return Q_SUPER(&QHsm_top);
}

/**
 * State Running_Block
 */
QState SeqDispatcher_Running_Block (SeqDispatcher *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = SEQDISPATCHER_RUNNING_BLOCK;
        
        return Q_HANDLED();

    case Q_EXIT_SIG:
        
        return Q_HANDLED();
        
    case Q_INIT_SIG:
        
        break;


    case DONE_SIG:
            SeqDispatcherImpl_sendCmdResponse(me->impl, e);
    SeqDispatcherImpl_incrSeqAvailable(me->impl, e);
    return Q_TRAN(&SeqDispatcher_Available);

        return Q_HANDLED();
    
    }
    return Q_SUPER(&SeqDispatcher_Running);
}

/**
 * State Running_NonBlock
 */
QState SeqDispatcher_Running_NonBlock (SeqDispatcher *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = SEQDISPATCHER_RUNNING_NONBLOCK;
        
        return Q_HANDLED();

    case Q_EXIT_SIG:
        
        return Q_HANDLED();
        
    case Q_INIT_SIG:
        
        break;


    case DONE_SIG:
            SeqDispatcherImpl_incrSeqAvailable(me->impl, e);
    return Q_TRAN(&SeqDispatcher_Available);

        return Q_HANDLED();
    
    }
    return Q_SUPER(&SeqDispatcher_Running);
}
