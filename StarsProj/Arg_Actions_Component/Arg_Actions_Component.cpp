// ======================================================================
// \title  Arg_Actions_Component.cpp
// \author watney
// \brief  cpp file for Arg_Actions_Component component implementation class
// ======================================================================

#include "Arg_Actions_Component/Arg_Actions_Component.hpp"

namespace Components {

// ----------------------------------------------------------------------
// Component construction and destruction
// ----------------------------------------------------------------------

Arg_Actions_Component ::Arg_Actions_Component(const char* const compName)
    : Arg_Actions_ComponentComponentBase(compName), m_g1Value(false), m_g2Value(false), m_evCount(0) {}

Arg_Actions_Component ::~Arg_Actions_Component() {}

// ----------------------------------------------------------------------
// Handler implementations for typed input ports
// ----------------------------------------------------------------------

void Arg_Actions_Component ::schedIn_handler(FwIndexType portNum, U32 context) {
    // Send EV1 signal with incrementing U16 parameter
    argActionsState_sendSignal_EV1(static_cast<U16>(m_evCount++));
}

void Arg_Actions_Component ::schedIn2_handler(FwIndexType portNum, U32 context) {
    // Send EV2 signal to test g2 guard
    argActionsState_sendSignal_EV2();
}

// ----------------------------------------------------------------------
// Handler implementations for commands
// ----------------------------------------------------------------------

void Arg_Actions_Component ::TEST_CMD_cmdHandler(FwOpcodeType opCode, U32 cmdSeq, U16 value) {
    argActionsState_sendSignal_EV1(value);
    
    // Send command response
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

void Arg_Actions_Component ::SET_G1_cmdHandler(FwOpcodeType opCode, U32 cmdSeq, bool value) {
    m_g1Value = value;
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

void Arg_Actions_Component ::SET_G2_cmdHandler(FwOpcodeType opCode, U32 cmdSeq, bool value) {
    m_g2Value = value;
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

// ----------------------------------------------------------------------
// Implementations for internal state machine actions
// ----------------------------------------------------------------------

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_a1(SmId smId,
                                                                 Components_Arg_Actions_FP::Signal signal,
                                                                 U16 value) {
    this->log_ACTIVITY_HI_a1Event(value);
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_a2(SmId smId, Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_a2Event();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_foo(SmId smId, Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_fooEvent();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s1Entry(SmId smId,
                                                                      Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s1EntryEvent();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s1Entry2(SmId smId,
                                                                       Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s1Entry2Event();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s1Exit(SmId smId,
                                                                     Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s1ExitEvent();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s1Exit2(SmId smId,
                                                                      Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s1Exit2Event();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s2Entry(SmId smId,
                                                                      Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s2EntryEvent();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s2Entry2(SmId smId,
                                                                       Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s2Entry2Event();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s2Exit(SmId smId,
                                                                     Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s2ExitEvent();
}

void Arg_Actions_Component ::Components_Arg_Actions_FP_action_s2Exit2(SmId smId,
                                                                      Components_Arg_Actions_FP::Signal signal) {
    this->log_ACTIVITY_HI_s2Exit2Event();
}

// ----------------------------------------------------------------------
// Implementations for internal state machine guards
// ----------------------------------------------------------------------

bool Arg_Actions_Component ::Components_Arg_Actions_FP_guard_g1(SmId smId,
                                                                Components_Arg_Actions_FP::Signal signal,
                                                                U16 value) const {
    const_cast<Arg_Actions_Component*>(this)->log_ACTIVITY_HI_g1GuardEvent(value);
    return m_g1Value;
}

bool Arg_Actions_Component ::Components_Arg_Actions_FP_guard_g2(SmId smId,
                                                                Components_Arg_Actions_FP::Signal signal) const {
    return m_g2Value;
}

}  // namespace Components
