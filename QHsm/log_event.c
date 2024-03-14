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
 **
 ** Description:
 **
 **    This file contains LogEvent implementation
 **
 ***********************************************************************/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "qf_port.h"
#include "hsm_qf.h"
#include "log_event.h"


/*******************************************************************************
 * @fn LogEventLog()
 * @brief logs Events
 * @param Input string
 * @return None
 *******************************************************************************/
void LogEvent_log(char *msg)
{
    (void)printf("%s\n", msg);
}



