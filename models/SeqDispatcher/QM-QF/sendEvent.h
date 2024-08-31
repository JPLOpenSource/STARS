        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H
#include "SeqDispatcher.h"

void sendEvent_init(SeqDispatcher *sm);
void sendEvent_send(QSignal signal);

#endif
