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

#ifndef log_event_h
#define log_event_h
#include <stdbool.h>


/*******************************************************************************
 ** @fn LogEventLog()
 ** @brief Logs Events
 ** @param Event message string
 ** @return None
 *******************************************************************************/
void LogEvent_log(char *msg);

#endif /* log_event_h */
