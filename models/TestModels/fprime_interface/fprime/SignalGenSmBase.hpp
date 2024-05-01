
#ifndef SIGNALGEN_SM_BASE_HPP
#define SIGNALGEN_SM_BASE_HPP
// ======================================================================
// \title  SignalGenSmBase.hpp
// \author Auto-generated
// \brief  Header file for the state machine base class
//
// ======================================================================            
#include "./SignalGenComponentAc.hpp"
#include "./Simple.h"
#include "./Toggle.h"
                                
namespace Ref {
    namespace StateMachine {
        typedef enum {
            SIMPLE1,
            SIMPLE2,
            TOGGLE,
        } SmId;                           
    };

    class SignalGenSmBase : public SignalGenComponentBase
        ,public SimpleIf
        ,public ToggleIf
                                
    {
        public:
            SignalGenSmBase(const char* const compName);
            void init(
                        NATIVE_INT_TYPE queueDepth,
                        NATIVE_INT_TYPE instance
            );
            
            // Interface to send an event to the state-machine
            void sendEvent(U32 eventSignal, StateMachine::SmId id);

            // Internal Interface handler for sendEvents
            void sendEvents_internalInterfaceHandler(const Svc::SMEvents& ev);
                                
            // Instantiate the state machines
            Simple simple1;
            Simple simple2;
            Toggle toggle;
            
                                
    };
}
#endif

            