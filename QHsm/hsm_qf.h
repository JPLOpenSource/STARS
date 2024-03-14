/*****************************************************************************
* Product:  QP/C
* Last Updated for Version: 4.2.00
* Date of the Last Update:  Jun 29, 2011
*
* Product:  QEP/C platform-independent public interface
* Last Updated for Version: 4.0.02
* Date of the Last Update:  Nov 10, 2008
*
* Product:  QF/C platform-independent public interface
* Last Updated for Version: 4.2.00
* Date of the Last Update:  Jul 13, 2011
*
*                    Q u a n t u m     L e a P s
*                    ---------------------------
*                    innovating embedded systems
*
* Copyright (C) 2002-2011 Quantum Leaps, LLC. All rights reserved.
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
 *       File: /src/hsm/hsm_qf.h
 * Created on: Dec 28, 2011
 *     Author: Shang-Wen Cheng <Shang-Wen.Cheng@jpl.nasa.gov>
 *             (Initial version by Leonard Reder <reder@jpl.nasa.gov>)
 *
 * HSM is a state-machine library based on Miro Samek's Quantum Platform (QP)
 * Hierarchical State Machine C library, version 4.2.  This updated module
 * replaces the MSL HSM module adapted and implemented by Todd Litwin, et. al.
 * The associated JPL StateChart Autocoder v2, taylored to the SMAP Mission,
 * generates code from UML XMI and compiles with this C library.
 *
 * This file is intended to replace a combination of header files, including
 * qf_port, qep_port, qep_pkg.h, etc., in the original Miro Samek Quantum
 * Framework distribution.
 *===========================================================================
 */
#ifndef HSM_QF_H
#define HSM_QF_H

#include "qf_port.h"


/* Quantum source code adaptation history:
 * [SWC 2011.12.28] Changed int types; removed QSPY stuff; slimmed down QActive;
 * eliminated QActive_defer and QActive_recall, which we're NOT going to use.
 * [SWC 2012.01.06] Removed all QActive queue-related functions, unused on SMAP.
 * Eliminated QF functions pertaining to event pools and QF lifecycle.
 * [SWC 2012.01.14] Removed QActive subscription functions, replacing them with
 * SMAP-flavor hsm_[de]register_sig functions (QActive_subscribe is kept due to
 * StateMachine code pattern requiring it);
 * Massively pared down various macro definitions to simplify file, including
 *   removing QF_EVENT_SIZ_SIZE and QF_TIMEEVT_CTR_SIZE;
 * Removed QF_add_ and QF_remove_ functions, and QF_active_ array;
 * Removed QActive.prio and .running attributes as they'll not going to be used;
 * Removed all interrupt related macros, QF_INT_*LOCK*.
 * [SWC 2012.01.15] Eliminated Q_SIGNAL_SIZE, harcoding 4-byte signals
 * [SWC 2012.01.24] Consolidated all QF headers into a single header file;
 * Eliminated unnecessary macro lines whose purpose was to faciliate customizing
 * Quantum code, such as ifndef QF_ACTIVE_SUPER_;
 * Merged QHsm and QFsmTag typedefs, since no QFsm code is needed/included;
 * Eliminated all Q_ROM, Q_ROM_VAR, and Q_ROM_BYTE definition and usages, since
 * SMAP FSW memory handling is handled per usual by MEM and flight computer;
 * Eliminated QEP_getVersion and QF_getPortVersion, as QF_getVersion suffices
 * to reflect the version of Quantum we brought in.
 * [SWC 2012.01.29] QF_publish replaced with hsm_publish and moved to hsm.c.
 * [SWC 2012.08.29] Hidden pointer dereference in QEP_TRIP/ENTER/EXIT eliminated
 * to conform to JPL Coding Standard Rule 28.
 * [SWC 2012.08.31] Hidden pointer in QStateHandler is left intact; for removing
 * it to address P10#9 warning leads to hundreds more JPL #30 warnings about
 * casting of function pointers into "other" types.
 * [SWC 2012.09.04] Eliminated qa_sub.c content QActive_subscribe, as it's not
 * used on SMAP.
 * [SWC 2012.09.05] QTimeEvt and all timer event function declarations removed
 * since on SMAP, timers are realized directly via TIM timer subscriptions.
 */

/**
* \file qf_port.h
*
* The maximum number of active objects in the application
*/
#define QF_MAX_ACTIVE   (16)   /* anticipate not exceeding 16 machines/submachines in SMAP! */

/**
* \file qevent.h  (SWC: header that all other headers depended on)
* \ingroup qep qf qk
* \brief QEvent class and basic macros used by all QP components.
*/
/****************************************************************************/
/** \brief The current QP version number
*
* \return version of the QP as a hex constant constant 0xXYZZ, where X is
* a 1-digit major version number, Y is a 1-digit minor version number, and
* ZZ is a 2-digit release number.
*/
#define QP_VERSION      (0x4200U)

/****************************************************************************/
typedef U32 QSignal;  /* [SWC 2011.12.28] using FSW int types */

/****************************************************************************/
/** \brief Event structure.
*
* QEvent represents events without parameters and serves as the base structure
* for derivation of events with parameters.
*
* The following example illustrates how to add an event parameter by
* derivation of the QEvent structure. Please note that the QEvent member
* super_ is defined as the FIRST member of the derived struct.
* \include qep_qevent.c
*
* \sa \ref derivation
*/
typedef struct QEventTag {
    QSignal sig;                          /**< signal of the event instance */
    /* [SWC 2011.12.28] eliminated unused poolId_ and refCtr_ from QP4.2 */
    /* uint8_t poolId_; */                   /**< pool ID (0 for static event) */
    /* uint8_t refCtr_; */                              /**< reference counter */
} QEvent;

/****************************************************************************/
/** helper macro to calculate static dimension of a 1-dim array \a array_ */
#define Q_DIM(array_) (sizeof(array_) / sizeof(array_[0]))


/**
* \file qep.h
* \ingroup qep qf qk
* \brief Public QEP/C interface.
*
* [SWC 2011.12.28] removed QSPY macros and QFsm functions; changed int types.
* [SWC 2012.01.24] merged QFsmTag and QHsm typedef; functionally equivalent;
* Elim. QEP_getVersion.
*/
/****************************************************************************/

/** \brief Type returned from  a state-handler function */
typedef U8 QState;

/** \brief Signature of a state-handler function without pointer reference */
typedef QState (*QStateHandler)(void *me, QEvent const *e);  /* HiddenPointerIndirection: @suppress semmle SMAP-579 */

/****************************************************************************/
/** \brief Hierarchical State Machine
*
* QHsm represents a Hierarchical Finite State Machine (HSM) with full
* support for hierarchical nesting of states, entry/exit actions,
* and initial transitions in any composite state.
*
* \note QHsm is not intended to be instantiated directly, but rather serves
* as the base structure for derivation of state machines in the application
* code.
*
* The following example illustrates how to derive a state machine structure
* from QHsm. Please note that the QHsm member super is defined as the FIRST
* member of the derived struct.
* \include qep_qhsm.c
*
* \sa \ref derivation
*/
typedef struct QFsmTag {
    QStateHandler state;         /**< current active state (state-variable) */

    /* [SWC 2013.02.08] added two additional states
     *- Output Boolean "handled" for whether QHsm dispatched the event
     *- Input Boolean "ignore_dropped" to ignore or ASSERT on dropped event
     */
    Bool handled;           /**< did QHsm handle the last dispatched event? */
    Bool ignore_dropped;              /**< ignore dropped event, or assert? */
} QHsm;

/* public methods */

/** \brief protected "constructor" of a HSM.
* Performs the first step of HSM initialization by assigning the
* initial pseudostate to the currently active state of the state machine.
*
* \note Must be called only by the "constructors" of the derived state
* machines.
* \note Must be called before QHsm_init().
*
* The following example illustrates how to invoke QHsm_ctor() in the
* "constructor" of a derived state machine:
* \include qep_qhsm_ctor.c
*
* \sa #QFsm_ctor
*/
#define QHsm_ctor(me_, initial_) ((me_)->state  = (initial_))

/** \brief Performs the second step of HSM initialization by triggering the
* top-most initial transition.
*
* \param me pointer the state machine structure derived from QHsm
* \param e constant pointer the QEvent or a structure derived from QEvent
* \note Must be called only ONCE after the "constructor" QHsm_ctor().
*
* The following example illustrates how to initialize a HSM, and dispatch
* events to it:
* \include qep_qhsm_use.c
*/
void QHsm_init(QHsm *me, QEvent const *e);

/** \brief Dispatches an event to a HSM
*
* Processes one event at a time in Run-to-Completion fashion.
* \param me is the pointer the state machine structure derived from ::QHsm.
* \param e is a constant pointer the ::QEvent or a structure derived
* from ::QEvent.
*
* \note Must be called after the "constructor" QHsm_ctor() and QHsm_init().
*
* \sa example for QHsm_init() \n \ref derivation
*/
void QHsm_dispatch(QHsm *me, QEvent const *e);

/** \brief Tests if a given state is part of the current active state
* configuratioin
*
* \param me is the pointer the state machine structure derived from ::QHsm.
* \param state is a pointer to the state handler function, e.g., &QCalc_on.
*/
Bool QHsm_isIn(QHsm *me, QStateHandler state);

/* protected methods */

/** \brief the top-state.
*
* QHsm_top() is the ultimate root of state hierarchy in all HSMs derived
* from ::QHsm. This state handler always returns (QSTATE)0, which means
* that it "handles" all events.
*
* \sa Example of the QCalc_on() state handler for Q_INIT().
*/
QState QHsm_top(QHsm *me, QEvent const *e);

/** \brief Value returned by a non-hierarchical state-handler function when
* it ignores (does not handle) the event.
*/
#define Q_RET_IGNORED       ((QState)1)

/** \brief The macro returned from a non-hierarchical state-handler function
* when it ignores (does not handle) the event.
*
* You call that macro after the return statement (return Q_IGNORED();)
*
* \include qepn_qfsm.c
*/
#define Q_IGNORED()         (Q_RET_IGNORED)

/** \brief Value returned by a state-handler function when it handles
* the event.
*/
#define Q_RET_HANDLED       ((QState)0)

/** \brief Value returned by a state-handler function when it handles
* the event.
*
* You call that macro after the return statement (return Q_HANDLED();)
* Q_HANDLED() can be used both in the FSMs and HSMs.
*
* \include qepn_qfsm.c
*/
#define Q_HANDLED()         (Q_RET_HANDLED)

/** \brief Value returned by a state-handler function when it takes a
* regular state transition.
*/
#define Q_RET_TRAN          ((QState)2)

/** \brief Designates a target for an initial or regular transition.
* Q_TRAN() can be used both in the FSMs and HSMs.
*
* [SWC 2012.01.24] Changed typecast to QHsm*, as FSM definitions were removed.
*
* \include qepn_qtran.c
*/
/*lint -e960 */     /* ignore MISRA Rule 42 (comma operator) for this macro */
#define Q_TRAN(target_)  \
    (((QHsm *)me)->state = (QStateHandler )(target_), Q_RET_TRAN)

/** \brief Value returned by a state-handler function when it cannot
* handle the event.
*/
#define Q_RET_SUPER         ((QState)3)

/** \brief Designates the superstate of a given state in an HSM.
*
* \include qepn_qhsm.c
*/
/*lint -e960 */     /* ignore MISRA Rule 42 (comma operator) for this macro */
#define Q_SUPER(super_)  \
    (((QHsm *)me)->state = (QStateHandler )(super_),  Q_RET_SUPER)


/****************************************************************************/
/** \brief QEP reserved signals */
enum QReservedSignals {
    Q_ENTRY_SIG = 1,                   /**< signal for coding entry actions */
    Q_EXIT_SIG  = 2,                    /**< signal for coding exit actions */
    Q_INIT_SIG  = 3,             /**< signal for coding initial transitions */
    Q_USER_SIG  = 4 /**< first signal that can be used in user applications */
};

/** internal QEP constants */
enum QEPConst {
    QEP_EMPTY_SIG_ = 0,    /**< reserved empty signal for internal use only */

    /** maximum depth of state nesting (including the top level),
     * must be >= 3
     */
    QEP_MAX_NEST_DEPTH_ = 6
};

/**
* \file qep_pkg.h
* \ingroup qep
* \brief Internal (package scope) QEP/C interface.
*
* Removed QEP_reservedEvt declaration, as it only needs to be declared STATIC'ly
* in hsm_qf.c.
*/

/** helper macro to trigger reserved event in an HSM */
#define QEP_TRIG_(state_, sig_) \
    ((state_)(me, &QEP_reservedEvt_[sig_]))

/** helper macro to trigger exit action in an HSM */
#define QEP_EXIT_(state_) \
    (QEP_TRIG_(state_, Q_EXIT_SIG))

/** helper macro to trigger entry action in an HSM */
#define QEP_ENTER_(state_) \
    (QEP_TRIG_(state_, Q_ENTRY_SIG))


/**
* \file qf.h
* \ingroup qf qk
* \brief QF/C platform-independent public interface.
*
* [SWC 2012.01.24] Elim. QF_getPortVersion().
* [SWC 2012.08.29] Elim. unused/unnecessary QF_ACTIVE_SUPER_, QF_ACTIVE_CTOR_,
* and QF_ACTIVE_STATE_, essentially eliminating the QF_ACTIVE "class"
* flexibility introduced by the Quantum Framework, in favor of simplicity of
* understanding.
* [SWC 2013.04.25] Moved QF_ACTIVE_DISPATCH_ to hsm_pub.h to change its
* invoked function to hsm_dispatch_event().
*/
/****************************************************************************/
#if (QF_MAX_ACTIVE < 1) || (63 < QF_MAX_ACTIVE)
    #error "QF_MAX_ACTIVE not defined or out of range. Valid range is 1..63"
#endif

typedef U16 QEventSize;  /* [SWC 2011.12.28] using FSW int types */
typedef U16 QTimeEvtCtr;

/** \brief The initialization of the ::QActive state machine.
 */
#define QF_ACTIVE_INIT_(me_, e_)       (QHsm_init((me_), (e_)))

/****************************************************************************/
/** \brief Active Object structure
*
* QActive is the base structure for derivation of active objects. Active
* objects in QF are encapsulated tasks (each embedding a state machine and
* an event queue) that communicate with one another asynchronously by
* sending and receiving events. Within an active object, events are
* processed sequentially in a run-to-completion (RTC) fashion, while QF
* encapsulates all the details of thread-safe event exchange and queuing.
*
* \note QActive is not intended to be instantiated directly, but rather
* serves as the base structure for derivation of active objects in the
* application code.
*
* The following example illustrates how to derive an active object from
* QActive. Please note that the QActive member super_ is defined as the
* FIRST member of the derived struct.
* \include qf_qactive.c
*
* \sa ::QActiveTag for the description of the data members \n \ref derivation
*/
typedef struct QActiveTag {
    /** base structure of QActive.
    */
    QHsm super;
} QActive;


/* protected functions ...*/

/** \brief protected "constructor" of an active object.
* Performs the first step of active object initialization by assigning the
* initial pseudostate to the currently active state of the state machine.
*
* \note Must be called only by the "constructors" of the derived active
* objects, as shown in the following example:
* \include qf_ctor.c
*
* \note Must be called before QActive_start().
*
* The following example illustrates how to invoke QFsm_ctor() in the
* "constructor" of a derived state machine:
* \include qep_qhsm_ctor.c
*
* \sa #QHsm_ctor and #QFsm_ctor
*/
#define QActive_ctor(me_, initial_) (QHsm_ctor(&(me_)->super, (initial_)))


/*****************************************************************************
* QF facilities
*/

/** \brief Subscriber-List structure
*
* This data type represents a set of active objects that subscribe to
* a given signal. The set is represented as an array of bits, where each
* bit corresponds to the unique priority of an active object.
*
* \sa ::QSubscrListTag for the description of the data members
*/
typedef struct QSubscrListTag {

    /** An array of bits representing subscriber active objects. Each bit
    * in the array corresponds to the unique priority of the active object.
    * The size of the array is determined of the maximum number of active
    * objects in the application configured by the #QF_MAX_ACTIVE macro.
    * For example, an active object of priority p is a subscriber if the
    * following is true: ((bits[QF_div8Lkup[p]] & QF_pwr2Lkup[p]) != 0)
    *
    * \sa QF_psInit(), ::QF_div8Lkup, ::QF_pwr2Lkup, #QF_MAX_ACTIVE
    */
    U8 bits[((QF_MAX_ACTIVE - 1) / 8) + 1];
} QSubscrList;

/* functions used in the QF ports only -------------------------------------*/

/** \brief Returns the QF version.
*
* This function returns constant version string in the format x.y.zz,
* where x (one digit) is the major version, y (one digit) is the minor
* version, and zz (two digits) is the maintenance release version.
* An example of the version string is "3.1.03".
*
* The following example illustrates the usage of this function:
* \include qf_version.c
*/
char const* QF_getVersion(void);


#endif /* HSM_QF_H */

/**
* \file qf.h
* \brief From Samek QHsm Lib: QF/C platform-independent public interface.
*/

/**
* \file qf_port.h
* \brief From Samek QHsm Lib: QF/C platform-specific definitions
*/

/**
* \file qep.h
* \brief From Samek QHsm Lib: Public QEP/C interface.
*/

/**
* \file qep_pkg.h
* \brief From Samek QHsm Lib: Internal (package scope) QEP/C interface.
*/

/**
* \file qhsm_top.c
* \brief From Samek QHsm Lib: QHsm_top() implementation.
*/

/**
* \file qhsm_in.c
* \brief From Samek QHsm Lib: QHsm_isIn() implementation.
*/

/**
* \file qhsm_ini.c
* \brief From Samek QHsm Lib: QHsm_init() implementation.
*/

/**
* \file qhsm_dis.c
* \brief From Samek QHsm Lib: QHsm_dispatch() implementation.
*/
