
    
#include "stdio.h"
#include "assert.h"
#include "SeqDispatcher.h"
#include "SeqDispatcherImpl.h"

void SeqDispatcherStateInit(SeqDispatcherImpl *self)
{
    self->sm.state = Available;

}


void SeqDispatcherStateUpdate(SeqDispatcherImpl *self, const EventSignal *e)
{
    switch (self->sm.state) {
    
            /**
            * state Available
            */
            case Available:
            
            switch (e->sig) {

                case DONE_SIG:
                        SeqDispatcherImpl_unknownSeqFinished(self, e);
                        SeqDispatcherImpl_incrSeqAvailable(self, e);

                    break;
    
                case START_SIG:
                        SeqDispatcherImpl_decSeqAvailable(self, e);
                        self->sm.state = NonBlock;

                    break;
    
                case RUN_SIG:
                        SeqDispatcherImpl_seqRunOut(self, e);
                        SeqDispatcherImpl_decSeqAvailable(self, e);
                        if (SeqDispatcherImpl_noWait(self, e) ) {
                            self->sm.state = NonBlock;
                        }
                        else {
                            self->sm.state = Block;
                        }

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state Block
            */
            case Block:
            
            switch (e->sig) {

                case DONE_SIG:
                        SeqDispatcherImpl_sendCmdResponse(self, e);
                        SeqDispatcherImpl_incrSeqAvailable(self, e);
                        self->sm.state = Available;

                    break;
    
                case START_SIG:
                        if (SeqDispatcherImpl_seqRunningNotFile(self, e) ) {
                            SeqDispatcherImpl_unexpectedSeqStart(self, e);
                        }

                    break;
    
                case RUN_SIG:
                        SeqDispatcherImpl_invalidSequencer(self, e);
                        SeqDispatcherImpl_sendExecutionError(self, e);

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state NonBlock
            */
            case NonBlock:
            
            switch (e->sig) {

                case DONE_SIG:
                        SeqDispatcherImpl_incrSeqAvailable(self, e);
                        self->sm.state = Available;

                    break;
    
                case START_SIG:
                        if (SeqDispatcherImpl_seqRunningNotFile(self, e) ) {
                            SeqDispatcherImpl_unexpectedSeqStart(self, e);
                        }

                    break;
    
                case RUN_SIG:
                        SeqDispatcherImpl_invalidSequencer(self, e);
                        SeqDispatcherImpl_sendExecutionError(self, e);

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        assert(0);
    }
}
