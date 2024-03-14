
    
#include <assert.h>
#include <Blinky.h>
#include <BlinkyImpl.h>

/**
 * Blinky Constructor
 */
Blinky *Blinky_Constructor (Blinky *me, BlinkyImpl *implObj, QActive *active) {
    QActive_ctor((QActive *)me, (QStateHandler )&Blinky_initial);
    me->impl = implObj;
    if (0 == active) {  // self IS the active object
        me->active = (QActive *)me;
    } else {  // set containing machine as active object
        me->active = active;
    }
    BlinkyImpl_set_qactive(me->impl, me->active);  // give impl access to parent QActive

    // State is initially at TOP
    me->myState = BLINKY__TOP__;

    return me;
}

BlinkyImpl *Blinky_getImpl (Blinky *me) {
    return me->impl;
}

Blinky_state Blinky_getCurrentState (Blinky *me) {
    return me->myState;
}

/**
 * Initial pseudostate of the state machine.
 *
 * This routine handles initial events of the state-machine.
 */
QState Blinky_initial (Blinky *me, QEvent *e) {
    BlinkyImpl_Bsp_Initialize(me->impl);
    return Q_TRAN(&Blinky_Off);

}
    
/**
 * State Off
 */
QState Blinky_Off (Blinky *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = BLINKY_OFF;
        BlinkyImpl_Bsp_LED_TurnOff(me->impl);
        return Q_HANDLED();

    case Q_EXIT_SIG:
        
        return Q_HANDLED();
        
    case Q_INIT_SIG:
        
        break;


    case TIMEOUT_SIG:
            return Q_TRAN(&Blinky_On);

        return Q_HANDLED();
    
    }
    return Q_SUPER(&QHsm_top);
}

/**
 * State On
 */
QState Blinky_On (Blinky *me, QEvent *e) {

    switch (e->sig) {

    case Q_ENTRY_SIG:
        me->myState = BLINKY_ON;
        BlinkyImpl_Bsp_LED_TurnOn(me->impl);
        return Q_HANDLED();

    case Q_EXIT_SIG:
        
        return Q_HANDLED();
        
    case Q_INIT_SIG:
        
        break;


    case TIMEOUT_SIG:
            return Q_TRAN(&Blinky_Off);

        return Q_HANDLED();
    
    }
    return Q_SUPER(&QHsm_top);
}
