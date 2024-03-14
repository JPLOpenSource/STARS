/*****************************************************************************
* Product: QF/C
* Last Updated for Version: 4.2.00
* Date of the Last Update:  Jul 05, 2011
*
* Product: QEP/C
* Last Updated for Version: 4.2.00
* Date of the Last Update:  Jun 29, 2011
*
* Product: QEP/C
* Last Updated for Version: 4.1.05
* Date of the Last Update:  Oct 26, 2010
*
*                    Q u a n t u m     L e a P s
*                    ---------------------------
*                    innovating embedded systems
*
* Copyright (C) 2002-2010 Quantum Leaps, LLC. All rights reserved.
*
* This software may be distributed and modified under the terms of the GNU
* General Public License version 2 (GPL) as published by the Free Software
* Foundation and appearing in the file GPL.TXT included in the packaging of
* this file. Please note that GPL Section 2[b] requires that all works based
* on this software must also be made publicly available under the terms of
* the GPL ("Copyleft").
*
* Alternatively, this software may be distributed and modified under the
* terms of Quantum Leaps commercial licenses, which expressly supersede
* the GPL and are specifically designed for licensees interested in
* retaining the proprietary status of their code.
*
* Contact information:
* Quantum Leaps Web site:  http://www.quantum-leaps.com
* e-mail:                  info@quantum-leaps.com
*****************************************************************************/
/*
 *       File: /src/hsm/hsm_qf.c
 * Created on: Dec 28, 2011 (renamed from qhsm.c)
 *     Author: Shang-Wen Cheng <Shang-Wen.Cheng@jpl.nasa.gov>
 *             (Initial version by Leonard Reder <reder@jpl.nasa.gov>)
 *
 * HSM is a state-machine library based on Miro Samek's Quantum Platform (QP)
 * Hierarchical State Machine C library, version 4.2.  This updated module
 * replaces the MSL HSM module adapted and implemented by Todd Litwin, et. al.
 * The associated JPL StateChart Autocoder v2, taylored to the SMAP Mission,
 * generates code from UML XMI and compiles with this C library.
 *
 * This file is intended to replace a combination of source files, including
 * qf_*.c, qhsm_*.c, and qep_*.c, in Samek's Quantum Framework distribution.
 *===========================================================================
 */

#include "qf_port.h"
#include "hsm_qf.h"

/* Quantum source code adaptation history:
 * [SWC 2011.12.28] Consolidated all qhsm_*.c files;
 * changed QHsm_isIn return type to Bool; removed QSPY macros;
 * changed Q_ASSERT and Q_ALLEGE to using FSW_ASSERT.
 * [SWC 2012.01.12] Removed interrupt locking, QSPY stuff;
 * changed Q_REQUIRE to FSW_ASSERT.
 * [SWC 2012.01.14] QActive_subscribe with empty function is moved to this file;
 * Removed QF_add_ and QF_remove_ functions, along with QF_active_ array;
 * QF_publish adapted to SMAP-flavor publish, and moved to hsm.c.
 * [SWC 2012.01.24] Consolidated all QF source files into a single source file;
 * All *Lkup table types converted from uint8_t to U8 per SMAP coding standards;
 * Eliminated QEP_getVersion and QF_getPortVersion, as QF_getVersion suffices
 * to reflect the version of Quantum we brought in.
 * [SWC 2012.08.29] All hidden pointers in QStateHandler made explicit to
 * conform to Power-of-10 R#9.
 * [SWC 2012.08.29] Hidden pointer dereference in QEP_TRIP/ENTER/EXIT eliminated
 * to conform to JPL Coding Standard Rule 28: all callers now dereference the
 * QStateHandler pointer first.
 * [SWC 2012.08.29] All int8_t converted to JPL datatype I8.
 * [SWC 2012.09.04] Eliminated qa_sub.c content QActive_subscribe, as it's not
 * used on SMAP.
 * [SWC 2012.09.05] Changed all while-/do-loops to for loop with simple bound
 * counter to appease Semmle and eliminate BoundedLoopIterations warnings.
 */

/**
* \file qep.c
* \ingroup qep
* \brief QEP_reservedEvt_; removed QEP_getVersion() implementation.
* 
* Preallocated reserved events
*/
/* Package-scope objects ---------------------------------------------------*/
STATIC QEvent const QEP_reservedEvt_[] = {
    { (QSignal)QEP_EMPTY_SIG_ },
    { (QSignal)Q_ENTRY_SIG },
    { (QSignal)Q_EXIT_SIG },
    { (QSignal)Q_INIT_SIG }
};

/**
* \file qhsm_top.c
* \ingroup qep
* \brief QHsm_top() implementation, do nothing.
*/
QState QHsm_top(QHsm *me, QEvent const *e) {
    (void)me;             /* supress the "unused argument" compiler warning */
    (void)e;              /* supress the "unused argument" compiler warning */
    return Q_IGNORED();                 /* the top state ignores all events */
}

/**
* \file qhsm_ini.c
* \ingroup qep
* \brief QHsm_init() implementation.
*/
void QHsm_init(QHsm *me, QEvent const *e) {
    I32 boundOuter;
    I32 boundInner;
    QStateHandler t;
                           /* the top-most initial transition must be taken */
    FSW_ASSERT(me != NULL);
    FSW_ASSERT((*me->state)(me, e) == Q_RET_TRAN);

    t = (QStateHandler )&QHsm_top;           /* HSM starts in the top state */

    me->ignore_dropped = FALSE;      /* Enable detection for dropped event */

    /* [SWC 2012.09.04] do-loop changed to for-loop to add loop bound and
     *  appease Semmle; loop guard logic became if-condition at end & reversed
     *
     * *LOOP INVARIANT: an initial transition (Q_INIT_SIG) can be taken from 't'
     * *ON LOOP EXIT: 't' is the innermost state after INIT-transition drill-in
     */
    for (boundOuter = QEP_MAX_NEST_DEPTH_ ; boundOuter > 0 ; --boundOuter) {
                                                /* drill into the target... */
        QStateHandler path[QEP_MAX_NEST_DEPTH_];
        I8 ip = (I8)0;                       /* transition entry path index */
                      /* first-time: target of outermost initial transition */
        path[0] = me->state;  /* subsequently: next-level initial transition*/
        (void)QEP_TRIG_(*(me->state), QEP_EMPTY_SIG_);

        
        /* *LOOP INVARIANT: 'me->state' not yet reached the superstate 't'
         * *ON LOOP EXIT: chain of super states established from me->state to t 
         */
        for (boundInner = QEP_MAX_NEST_DEPTH_ - 1 ; (me->state != t) && (boundInner > 0) ; --boundInner) {
            ++ip;
            path[ip] = me->state;
            (void)QEP_TRIG_(*(me->state), QEP_EMPTY_SIG_);
        }
        FSW_ASSERT(boundInner >= 0);

        me->state = path[0];
                                            /* entry path must not overflow */
        FSW_ASSERT(ip < (I8)QEP_MAX_NEST_DEPTH_);

        /* [SWC 2012.09.04] do-loop changed to for-loop to add loop bound and
         *  appease Semmle; do-loop guard becomes for-loop guard since
         *  ip>=0 initially!
         *- bound counter ensures at least 1 execution as original do-loop
         *
         * *LOOP INVARIANT: 'ip' a valid array index AND iterations within bound
         * *ON LOOP EXIT: ENTRY processed on chain of states from t down to the
         *               original me->state in this iteration
         */
        for (boundInner = QEP_MAX_NEST_DEPTH_ ; (boundInner > 0) && (ip >= (I8)0) ; --boundInner) {
                    /* retrace the entry path in reverse (desired) order... */
            QEP_ENTER_(*(path[ip]));                      /* enter path[ip] */
            --ip;
        }
        FSW_ASSERT(boundInner >= 0);

        t = path[0];                /* current state becomes the new source */

        /* This used to be the do-loop condition; but it cannot be converted
         *  to a for-loop condition because the initial 't' is TOP,
         *  which does NOT handle Q_INIT_SIG (it ignore all signals).
         *
         * Takes the initial transition, if any, from state 't'
         */
        if (QEP_TRIG_(*t, Q_INIT_SIG) != Q_RET_TRAN) {  /* INIT transition not taken */
            break;  /* break from loop */
        }
    }
    FSW_ASSERT(boundOuter >= 0);

    me->state = t;

}

/**
* \file qhsm_in.c
* \ingroup qep
* \brief QHsm_isIn() implementation.
*/
Bool QHsm_isIn(QHsm *me, QStateHandler state) {

    QStateHandler s;
    QState r = Q_RET_HANDLED;  /* [SWC] condition to go thru loop at least once */
    Bool inState = FALSE; /* assume that this HSM is not in 'state' */
    I32 bound;

    FSW_ASSERT(me != NULL);
    FSW_ASSERT(state != NULL);

    s = me->state;
    
    /* [SWC 2012.09.04] do-loop changed to for-loop to add loop bound and
     *  appease Semmle; loop guard logic reversed
     *
     * *LOOP INVARIANT: 'r' does not contain Q_IGNORED return code; that can
     *   happen if we've reached TOP state, or found state matching query state
     * *ON LOOP EXIT: 'me->state' matches query state, or is TOP state
     */
    for (bound = QEP_MAX_NEST_DEPTH_ ; (bound > 0) && (r != Q_RET_IGNORED) ; --bound) {
        if (me->state == state) {                   /* do the states match? */
            inState = TRUE;                     /* match found, return TRUE */
            r = Q_RET_IGNORED;                     /* break out of the loop */
        } else {
            r = QEP_TRIG_(*(me->state), QEP_EMPTY_SIG_);
        }
    }
    FSW_ASSERT(bound >= 0);
                                              /* QHsm_top state not reached */
    me->state = s;                            /* restore the original state */

    return inState;                                    /* return the status */
}

/**
* \file qhsm_dis.c
* \ingroup qep
* \brief QHsm_dispatch() implementation.
* 
* [SWC 2012.01.16] Added EVR Warning for dropped events, and that's the ONLY
* modification to the end of this function; the entire function is otherwise
* left pristine and untouched to preserve functional integrity!
* [SWC 2013.02.08] Added logic to set a new QHsm flag indicating whether the
* dispatched event was handled, and to check an input flag 'ignore_dropped' to
* decide whether to assert on dropped event.
*/
void QHsm_dispatch(QHsm *me, QEvent const *e) {  /* FunctionTooLong: @suppress semmle SMAP-579 */
    QStateHandler path[QEP_MAX_NEST_DEPTH_];
    QStateHandler s;
    QStateHandler t;
    QState r;
    I32 bound;
    I32 bound2;

    FSW_ASSERT(me != NULL);
    FSW_ASSERT(e != NULL);


    me->handled = FALSE;                          /* assume event NOT handled */

    t = me->state;                                  /* save the current state */

    
    /* [SWC 2012.09.04] do-loop changed to for-loop to add loop bound and
     *  appease Semmle; loop guard logic reversed
     *- bound counter ensures at least one execution like original do-loop, but
     *  UNO wants to see 's' and 'r' variables explicitly initialized first
     *
     */
                                       /* process the event hierarchically... */
    s = me->state;      /* execute these two lines once to initialize s and r */
    r = (*s)(me, e);                                /* invoke state handler s */
    
    /* *LOOP INVARIANT: 'r' indicates Q_SUPER return code, meaning we've gone up
     *   to super state in state hierarchy of source state s.
     * *ON LOOP EXIT: 's' holds the closest superstate that handles event 'e';
     *   'r' is the handle return code;
     *   'me->state' is potentially the target of transition (confirmed via 'r')
     */
    for (bound = QEP_MAX_NEST_DEPTH_-1 ; (bound > 0) && (r == Q_RET_SUPER) ; --bound) {
        s = me->state;
        r = (*s)(me, e);                            /* invoke state handler s */
    }
    FSW_ASSERT(bound >= 0);

    if (r == Q_RET_TRAN) {                               /* transition taken? */
        I8 ip = (I8)(-1);                      /* transition entry path index */
        I8 iq;                          /* helper transition entry path index */

        path[0] = me->state;             /* save the target of the transition */
        path[1] = t;

        /* *LOOP INVARIANT: 't'/'me->state' not yet reached the superstate 's'
         * *ON LOOP EXIT: EXIT processed on chain of states from 'current' state
         *               up to but not including superstate 's'
         *
         * Since 's' handled the event, it is considered the SOURCE state
         */
        for (bound = QEP_MAX_NEST_DEPTH_ ; (bound > 0) && (t != s) ; --bound) {
                              /* exit current state to transition source s... */
            if (QEP_EXIT_(*t) == Q_RET_HANDLED) {             /*exit handled? */
                (void)QEP_TRIG_(*t, QEP_EMPTY_SIG_);  /* find superstate of t */
            }
            t = me->state;                  /* me->state holds the superstate */
        }
        FSW_ASSERT(bound >= 0);

        t = path[0];                              /* target of the transition */

        if (s == t) {        /* (a) check source==target (transition to self) */
            (void)QEP_EXIT_(*s);                           /* exit the source */
            ip = (I8)0;                                   /* enter the target */
        }
        else {
            (void)QEP_TRIG_(*t, QEP_EMPTY_SIG_);      /* superstate of target */
            t = me->state;
            if (s == t) {                  /* (b) check source==target->super */
                ip = (I8)0;                               /* enter the target */
            }
            else {
                (void)QEP_TRIG_(*s, QEP_EMPTY_SIG_);     /* superstate of src */
                                    /* (c) check source->super==target->super */
                if (me->state == t) {
                    (void)QEP_EXIT_(*s);                   /* exit the source */
                    ip = (I8)0;                           /* enter the target */
                }
                else {
                                           /* (d) check source->super==target */
                    if (me->state == path[0]) {
                        (void)QEP_EXIT_(*s);               /* exit the source */
                    }
                    else {   /* (e) check rest of source==target->super->super..
                              * and store the entry path along the way
                              * 
                              * N.B. at this point, 't' takes on the role of the
                              *   source superstate!
                              */
                        iq = (I8)0;            /* indicate that LCA not found */
                        ip = (I8)1;        /* enter target and its superstate */
                        path[1] = t;         /* save the superstate of target */
                        t = me->state;                  /* save source->super */
                                                 /* find target->super->super */
                        r = QEP_TRIG_(*(path[1]), QEP_EMPTY_SIG_);
                        /*
                         * *LOOP INVARIANT: 'r' contains return code Q_SUPER,
                         *  meaning more superstate in target-hierarchy to do
                         * *ON LOOP EXIT: if LCA found, target->super->super..
                         *  chain of states stored in 'path' array, and 'ip'
                         *  points to state right below LCA; otherwise,
                         *  'path' holds entire target hierarchy up to TOP, and
                         *  'ip' points to TOP
                         */
                        for (bound = QEP_MAX_NEST_DEPTH_ ; (bound > 0) && (r == Q_RET_SUPER) ; --bound) {
                            ++ip;
                            path[ip] = me->state;     /* store the entry path */
                            if (me->state == s) {        /* is it the source? */
                                iq = (I8)1;        /* indicate that LCA found */
                                              /* entry path must not overflow */
                                FSW_ASSERT(ip < (I8)QEP_MAX_NEST_DEPTH_);
                                --ip;              /* do not enter the source */
                                r = Q_RET_HANDLED;      /* terminate the loop */
                            }
                            else {     /* it is not the source, keep going up */
                                r = QEP_TRIG_(*(me->state), QEP_EMPTY_SIG_);
                            }
                        }
                        FSW_ASSERT(bound >= 0);

                        if (iq == (I8)0) {          /* the LCA not found yet? */

                                              /* entry path must not overflow */
                            FSW_ASSERT(ip < (I8)QEP_MAX_NEST_DEPTH_);

                            (void)QEP_EXIT_(*s);           /* exit the source */

                                  /* (f) check the rest of source->super
                                   *                  == target->super->super...
                                   */
                            iq = ip;
                            r = Q_RET_IGNORED;      /* indicate LCA NOT found */
                            /*
                             * [SWC 2012.09.05] do-loop changed to for-loop to
                             *  add loop bound and appease Semmle; do-loop guard
                             *  becomes for-loop guard, since iq>=0 initially!
                             *- bound counter also ensures at least one
                             *  execution like original do-loop
                             *
                             * *LOOP INVARIANT: 'path' array not yet traversed
                             * *ON LOOP EXIT: if LCA found, 'ip' points to state
                             *  in target hierarchy below LCA to begin ENTRY;
                             *  otherwise, 'r' remains Q_IGNORED to try case (g)
                             */
                            for (bound = QEP_MAX_NEST_DEPTH_ ; (bound > 0) && (iq >= (I8)0) ; --bound) {
                                if (t == path[iq]) {      /* is this the LCA? */
                                    r = Q_RET_HANDLED;  /* indicate LCA found */
                                    ip = (I8)(iq - 1);    /* do not enter LCA */
                                    iq = (I8)(-1);      /* terminate the loop */
                                }
                                else {
                                    --iq;   /* try lower superstate of target */
                                }
                            }
                            FSW_ASSERT(bound >= 0);

                            if (r != Q_RET_HANDLED) {   /* LCA not found yet? */
                                            /* (g) check each source->super->...
                                             * for each target->super...
                                             */
                                r = Q_RET_IGNORED;            /* keep looping */
                                
                                /* [SWC 2012.09.05] do-loop changed to for-loop
                                 *  to add loop bound and appease Semmle;
                                 *  do-loop guard becomes for-loop guard, since
                                 *  r != Q_RET_HANDLED initially!
                                 *- bound counter also ensures at least one
                                 *  execution like original do-loop
                                 *
                                 * *LOOP INVARIANT: 'r' does not hold Q_HANDLED
                                 * *ON LOOP EXIT: 'r' holds Q_HANDLED, indicating
                                 *  that the inner loop has found the LCA!
                                 */
                                for (bound = QEP_MAX_NEST_DEPTH_ ; (bound > 0) && (r != Q_RET_HANDLED) ; --bound) {
                                                         /* exit t unhandled? */
                                    if (QEP_EXIT_(*t) == Q_RET_HANDLED) {
                                        (void)QEP_TRIG_(*t, QEP_EMPTY_SIG_);
                                    }
                                    t = me->state;       /* set to super of t */
                                    iq = ip;
                                    
                                    /* [SWC 2012.09.05] do-loop changed to for-
                                     *  loop to add loop bound & appease Semmle;
                                     *  do-loop guard becomes for-loop guard,
                                     *  since iq>=0 initially!
                                     *- bound counter also ensures at least one
                                     *  execution like original do-loop
                                     *
                                     * *LOOP INVARIANT: 'path' not yet traversed
                                     * *ON LOOP EXIT: if LCA is found, 'ip'
                                     *  points to state in target hierarchy
                                     *  below the LCA to begin ENTRY; otherwise,
                                     *  'ip' remains pointing to the TOP state
                                     *  in 'path' array for next outer iteration
                                     */
                                    for (bound2 = QEP_MAX_NEST_DEPTH_ ; (bound2 > 0) && (iq >= (I8)0) ; --bound2) {
                                        if (t == path[iq]) {  /* is this LCA? */
                                                          /* do not enter LCA */
                                            ip = (I8)(iq - 1);
                                            iq = (I8)(-1);     /* break inner */
                                            r = Q_RET_HANDLED; /* break outer */
                                        }
                                        else {
                                            --iq;
                                        }
                                    }
                                    FSW_ASSERT(bound2 >= 0);
                                }
                                FSW_ASSERT(bound >= 0);
                            }
                        }
                    }
                }
            }
        }
                      /* retrace the entry path in reverse (desired) order... */
        for (; ip >= (I8)0; --ip) {
            (void)QEP_ENTER_(*(path[ip]));                  /* enter path[ip] */
        }
        t = path[0];                        /* stick the target into register */
        me->state = t;                            /* update the current state */

        /* This is essentially the same loop as QHsm_init, to take the INITial
         *  transitions in to the target state hierarchy.
         *
         * *LOOP INVARIANT: initial transition (Q_INIT_SIG) can be taken from 't'
         * *ON LOOP EXIT: 't' is innermost state after INIT-transition drill-in
         */
                                        /* drill into the target hierarchy... */
        for (bound = QEP_MAX_NEST_DEPTH_ ; (bound > 0) && (QEP_TRIG_(*t, Q_INIT_SIG) == Q_RET_TRAN) ; --bound) {
            ip = (I8)0;
            path[0] = me->state;
            (void)QEP_TRIG_(*(me->state), QEP_EMPTY_SIG_); /* find superstate */

            /* *LOOP INVARIANT: 'me->state' not yet reached the superstate 't'
             * *ON LOOP EXIT: state chain established from me->state to t
             */
            for (bound2 = QEP_MAX_NEST_DEPTH_ - 1; (bound2 > 0) && (me->state != t) ; --bound2) {
                ++ip;
                path[ip] = me->state;
                (void)QEP_TRIG_(*(me->state), QEP_EMPTY_SIG_);/*find superstate*/
            }
            FSW_ASSERT(bound2 >= 0);
            me->state = path[0];
                                              /* entry path must not overflow */
            FSW_ASSERT(ip < (I8)QEP_MAX_NEST_DEPTH_);

            /* [SWC 2012.09.04] do-loop changed to for-loop to add loop bound
             *  and appease Semmle; do-loop guard becomes for-loop guard since
             *  ip>=0 initially!
             *- bound counter ensures at least 1 execution as original do-loop
             *
             * *LOOP INVARIANT: 'ip' a valid array index
             * *ON LOOP EXIT: ENTRY processed on chain of states from t down
             *               to the original me->state in this iteration
             */
            for (bound2 = QEP_MAX_NEST_DEPTH_ ; (bound2 > 0) && (ip >= (I8)0) ; --bound2) {
                      /* retrace the entry path in reverse (correct) order... */
                (void)QEP_ENTER_(*(path[ip]));              /* enter path[ip] */
                --ip;
            }
            FSW_ASSERT(bound2 >= 0);

            t = path[0];
        }
        FSW_ASSERT(bound >= 0);
    }                                           /* else, transition not taken */

    if (s == ((QStateHandler )&QHsm_top)) {             /* Reached TOP state! */

        
        /* [SWC 2012.08.28] From discussion with Dave/Hyejung:
         *   ASSERT if drop event; reaching the "TOP" state means event dropped!
         * [SWC 2013.02.08] ..unless explictly specified to IGNORE dropped event
         * [SWC 2013.06.21] ..replaced ASSERT with EVR WARNING_LO for R4 onward!
         * [SWC 2013.09.30] ..JIRA SMAP-977: eliminated ASSERT!
         */

        if (!me->ignore_dropped) {

            /* SMAP had an EVR here for dropped events */
 
        }
    } else {

        me->handled = TRUE;              /* dispatched event has been handled */

    }

    me->ignore_dropped = FALSE;      /* reinstate detection for dropped event */

    me->state = t;              /* set new state or restore the current state */
}

/**
* \file qf_act.c
* \ingroup qf
* \brief QF_getVersion() implementation.
* 
* Eliminated QF_active_[], QF_add_()/QF_remove_() items, and QF_getPortVersion()
*/
/*..........................................................................*/
/*lint -e970 -e971            ignore MISRA rules 13 and 14 in this function */
char const* QF_getVersion(void) {
    static char const version[] = {
        (char)(((QP_VERSION >> 12U) & 0xFU) + (U8)'0'),
        '.',
        (char)(((QP_VERSION >>  8U) & 0xFU) + (U8)'0'),
        '.',
        (char)(((QP_VERSION >>  4U) & 0xFU) + (U8)'0'),
        (char)((QP_VERSION          & 0xFU) + (U8)'0'),
        '\0'
    };
    return version;
}
