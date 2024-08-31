
    
#include "stdio.h"
#include "assert.h"
#include "SeqDispatcher.h"
#include "sendEvent.h"

void SeqDispatcher::init()
{
    this->state = Available;

}


void SeqDispatcher::update(EventSignal *e)
{
    switch (this->state) {
    
            /**
            * state Available
            */
            case Available:
            
            switch (e->sig) {

                case DONE_SIG:
                        unknownSeqFinished(e);
                        incrSeqAvailable(e);

                    break;
    
                case START_SIG:
                        decSeqAvailable(e);
                        this->state = NonBlock;

                    break;
    
                case RUN_SIG:
                        seqRunOut(e);
                        decSeqAvailable(e);
                        if (noWait(e) ) {
                            this->state = NonBlock;
                        }
                        else {
                            this->state = Block;
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
                        sendCmdResponse(e);
                        incrSeqAvailable(e);
                        this->state = Available;

                    break;
    
                case START_SIG:
                        if (seqRunningNotFile(e) ) {
                            unexpectedSeqStart(e);
                        }

                    break;
    
                case RUN_SIG:
                        invalidSequencer(e);
                        sendExecutionError(e);

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
                        incrSeqAvailable(e);
                        this->state = Available;

                    break;
    
                case START_SIG:
                        if (seqRunningNotFile(e) ) {
                            unexpectedSeqStart(e);
                        }

                    break;
    
                case RUN_SIG:
                        invalidSequencer(e);
                        sendExecutionError(e);

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        assert(0);
    }
}
