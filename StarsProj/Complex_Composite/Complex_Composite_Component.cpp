// ======================================================================
// \title  Complex_Composite_Component.cpp
// \author watney
// \brief  cpp file for Complex_Composite_Component component implementation class
// ======================================================================

#include "Complex_Composite/Complex_Composite_Component.hpp"

namespace Components {

// ----------------------------------------------------------------------
// Component construction and destruction
// ----------------------------------------------------------------------

Complex_Composite_Component ::Complex_Composite_Component(const char* const compName)
    : Complex_Composite_ComponentComponentBase(compName) {}

Complex_Composite_Component ::~Complex_Composite_Component() {}

// ----------------------------------------------------------------------
// Handler implementations for commands
// ----------------------------------------------------------------------

void Complex_Composite_Component ::SEND_EV1_cmdHandler(FwOpcodeType opCode, U32 cmdSeq) {
    complexCompositeState_sendSignal_Ev1();
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

void Complex_Composite_Component ::SEND_EV2_cmdHandler(FwOpcodeType opCode, U32 cmdSeq) {
    complexCompositeState_sendSignal_Ev2();
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

void Complex_Composite_Component ::SEND_EV3_cmdHandler(FwOpcodeType opCode, U32 cmdSeq) {
    complexCompositeState_sendSignal_Ev3();
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

void Complex_Composite_Component ::SEND_EV4_cmdHandler(FwOpcodeType opCode, U32 cmdSeq) {
    complexCompositeState_sendSignal_Ev4();
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

// ----------------------------------------------------------------------
// Implementations for internal state machine actions
// ----------------------------------------------------------------------

void Complex_Composite_Component ::Components_Complex_Composite_action_init1(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_init1Event();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s1111Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s1111EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s1111Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s1111ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s111Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s111EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s111Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s111ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s11Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s11EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s11Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s11ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s121Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s121EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s121Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s121ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s12Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s12EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s12Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s12ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s1Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s1EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s1Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s1ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s21Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s21EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s21Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s21ExitEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s2Entry(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s2EntryEvent();
}

void Complex_Composite_Component ::Components_Complex_Composite_action_s2Exit(
    SmId smId,
    Components_Complex_Composite::Signal signal) {
    this->log_ACTIVITY_HI_s2ExitEvent();
}

}  // namespace Components
