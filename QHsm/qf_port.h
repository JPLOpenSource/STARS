/*********************************************************************
 **
 ** Copyright 2014, by the California Institute of Technology. ALL
 ** RIGHTS RESERVED. United States Government Sponsorship
 ** acknowledged. Any commercial use must be negotiated with the Office
 ** of Technology Transfer at the California Institute of Technology.
 ** This software may be subject to U.S. export control laws. By
 ** accepting this software, the user agrees to comply with all
 ** applicable U.S. export laws and regulations. User has the
 ** responsibility to obtain export licenses, or other export authority
 ** as may be required before exporting such information to foreign
 ** countries or providing access to foreign persons.
 **
 ** Description:
 **     This file contains the typedefs used by QF code
 **
 ***********************************************************************/

#ifndef QF_PORT_H
#define QF_PORT_H

#include <stdbool.h>
#include <assert.h>
#include "BasicTypes.hpp"

typedef bool    Bool;
#if 0
typedef uint32_t U32;
typedef uint16_t U16;
typedef uint8_t  U8;
typedef bool     Bool;
typedef int32_t I32;
typedef int16_t I16;
typedef int8_t I8;
#endif

#ifndef FALSE
#define FALSE 0
#endif
#ifndef TRUE
#define TRUE 1
#endif

/* TO DO:  This assert should be replaced with the ISF Assert, but bringing in the ISF Assert header file
 * brings in too many other header files and make this difficult to compile.  Discuss a solution.
 */

#define FSW_ASSERT(test) \
    if (test) { \
    } \
    else assert(false)

#include "hsm_qf.h"

#ifdef SEIS_TEST_HARNESS

void QActive_subscribe(QActive const *me, QSignal sig);

#else

#define QActive_subscribe(me, sig) ((void) 0)

#endif /* SEIS_TEST_HARNESS */


#endif /* QF_PORT_H */
