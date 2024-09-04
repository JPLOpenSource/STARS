        
#ifndef _SEND_EVENT_H
#define _SEND_EVENT_H
#include "SeqDispatcherImpl.h"

void sendEvent_init(SeqDispatcherImpl *impl);
void sendEvent_send(unsigned int signal);

#endif
