
// ======================================================================
// \title  SeqDispatcher.cpp
// \author Auto-generated
// \brief  cpp file for state machine SeqDispatcher
//
// ======================================================================            
    
#include <Fw/Types/Assert.hpp>
#include "SeqDispatcher.hpp"


void Ref::SeqDispatcher::init(const FwEnumStoreType stateMachineId)
{
    this->state = Available;

}


void Ref::SeqDispatcher::update(
    const FwEnumStoreType stateMachineId, 
    const SeqDispatcher_Interface::SeqDispatcher_Signals signal, 
    const Fw::SmSignalBuffer &data
)
{
    switch (this->state) {
    
            /**
            * state Available
            */
            case Available:
            
            switch (signal) {

                case SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG:
                        parent->SeqDispatcher_unknownSeqFinished(stateMachineId, signal, data);
                        parent->SeqDispatcher_incrSeqAvailable(stateMachineId, signal, data);

                    break;
    
                case SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG:
                        parent->SeqDispatcher_decSeqAvailable(stateMachineId, signal, data);
                        this->state = NonBlock;

                    break;
    
                case SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG:
                        parent->SeqDispatcher_seqRunOut(stateMachineId, signal, data);
                        parent->SeqDispatcher_decSeqAvailable(stateMachineId, signal, data);
                        if (parent->SeqDispatcher_noWait(stateMachineId, signal, data) ) {
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
            
            switch (signal) {

                case SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG:
                        parent->SeqDispatcher_sendCmdResponse(stateMachineId, signal, data);
                        parent->SeqDispatcher_incrSeqAvailable(stateMachineId, signal, data);
                        this->state = Available;

                    break;
    
                case SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG:
                        if (parent->SeqDispatcher_seqRunningNotFile(stateMachineId, signal, data) ) {
                            parent->SeqDispatcher_unexpectedSeqStart(stateMachineId, signal, data);
                        }

                    break;
    
                case SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG:
                        parent->SeqDispatcher_invalidSequencer(stateMachineId, signal, data);
                        parent->SeqDispatcher_sendExecutionError(stateMachineId, signal, data);

                    break;
    
                default:
                    break;
            }
            break;
    
            /**
            * state NonBlock
            */
            case NonBlock:
            
            switch (signal) {

                case SeqDispatcher_Interface::SeqDispatcher_Signals::DONE_SIG:
                        parent->SeqDispatcher_incrSeqAvailable(stateMachineId, signal, data);
                        this->state = Available;

                    break;
    
                case SeqDispatcher_Interface::SeqDispatcher_Signals::START_SIG:
                        if (parent->SeqDispatcher_seqRunningNotFile(stateMachineId, signal, data) ) {
                            parent->SeqDispatcher_unexpectedSeqStart(stateMachineId, signal, data);
                        }

                    break;
    
                case SeqDispatcher_Interface::SeqDispatcher_Signals::RUN_SIG:
                        parent->SeqDispatcher_invalidSequencer(stateMachineId, signal, data);
                        parent->SeqDispatcher_sendExecutionError(stateMachineId, signal, data);

                    break;
    
                default:
                    break;
            }
            break;
    
        default:
        FW_ASSERT(0);
    }
}
