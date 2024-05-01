
// ======================================================================
// \title  SignalGenSmBase.cpp
// \author Auto-generated
// \brief  Cpp file for the state machine base class
//
// ======================================================================            
#include "./SignalGenSmBase.hpp"
#include "./Simple.h"
#include "./Toggle.h"
                                
Ref::SignalGenSmBase::SignalGenSmBase(const char* const compName):
    SignalGenComponentBase(compName)
    ,simple1(this)
    ,simple2(this)
    ,toggle(this)
{
                                
}                               

void Ref::SignalGenSmBase::init(
            NATIVE_INT_TYPE queueDepth,
            NATIVE_INT_TYPE instance)
{
    SignalGenComponentBase::init(queueDepth, instance);
                                
    // Initialize the state machine
    simple1.init();
    simple2.init();
    toggle.init();
    
} 

void Ref::SignalGenSmBase:: sendEvent(U32 eventSignal, StateMachine::SmId id) {
                                
    Svc::SMEvents event;
    event.seteventSignal(eventSignal);
    event.setsmId(id);
    sendEvents_internalInterfaceInvoke(event);
}

void Ref::SignalGenSmBase::sendEvents_internalInterfaceHandler(const Svc::SMEvents& ev)
{
    U16 id = ev.getsmId();
    switch (id) {
                                
        case StateMachine::SIMPLE1:
            this->simple1.update(&ev);
            break;
        case StateMachine::SIMPLE2:
            this->simple2.update(&ev);
            break;
        case StateMachine::TOGGLE:
            this->toggle.update(&ev);
            break;
        default:
            FW_ASSERT(0);
    }

}
            