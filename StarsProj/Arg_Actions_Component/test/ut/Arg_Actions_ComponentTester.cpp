// ======================================================================
// \title  Arg_Actions_ComponentTester.cpp
// \author watney
// \brief  cpp file for Arg_Actions_Component component test harness implementation class
// ======================================================================

#include "Arg_Actions_ComponentTester.hpp"

namespace Components {

// ----------------------------------------------------------------------
// Construction and destruction
// ----------------------------------------------------------------------

Arg_Actions_ComponentTester ::Arg_Actions_ComponentTester()
    : Arg_Actions_ComponentGTestBase("Arg_Actions_ComponentTester", Arg_Actions_ComponentTester::MAX_HISTORY_SIZE),
      component("Arg_Actions_Component") {
    this->connectPorts();
    this->initComponents();
}

Arg_Actions_ComponentTester ::~Arg_Actions_ComponentTester() {
    this->component.deinit();
}

// ----------------------------------------------------------------------
// Tests
// ----------------------------------------------------------------------

    void Arg_Actions_ComponentTester::testDataCommand() {
        this->sendCmd_SET_G1(0, 0, true);
        this->sendCmd_TEST_CMD(0, 0, 1234);
        dispatchAll();
        ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
        ASSERT_EVENTS_g1GuardEvent_SIZE(1);
        ASSERT_EVENTS_g1GuardEvent(0, 1234);
        ASSERT_EVENTS_s2EntryEvent_SIZE(1);
        ASSERT_EVENTS_s2Entry2Event_SIZE(1);
        ASSERT_EVENTS_fooEvent_SIZE(3);

        this->sendCmd_TEST_CMD(0, 0, 4567);
        dispatchAll();
        ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
        ASSERT_EVENTS_a1Event(0, 4567);
    }

    void Arg_Actions_ComponentTester ::testTransitions() {
    // Initial state should be S1 after initialization
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(1);
    clearHistory();

    // Set g1=false, send EV1 (guard fails, should stay in S1)
    this->sendCmd_SET_G1(0, 0, false);
    dispatchAll();
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s2EntryEvent_SIZE(0);  // Should not transition
    clearHistory();

    // Set g1=true, send EV1 (guard passes, S1->S2)
    this->sendCmd_SET_G1(0, 1, true);
    dispatchAll();
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);

    // Send EV1 from S2 (no guard, always transitions S2->S1)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    clearHistory();

    // Set g1=true, send EV1 again (guard passes, S1->S2)
    this->sendCmd_SET_G1(0, 2, true);
    dispatchAll();
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);

    // Send EV1 from S2 (transition S2->S1)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
}

void Arg_Actions_ComponentTester ::testEV2Transitions() {
    // Initial state should be S1 after initialization
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    clearHistory();

    // Set g2=true, send EV2 (guard passes, S1->S2)
    this->sendCmd_SET_G2(0, 0, true);
    dispatchAll();
    invoke_to_schedIn2(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);

    // Send EV1 from S2 to return to S1 (no guard, always transitions S2->S1)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    clearHistory();

    // Set g2=false, send EV2 (guard fails, should stay in S1)
    this->sendCmd_SET_G2(0, 1, false);
    dispatchAll();
    invoke_to_schedIn2(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s2EntryEvent_SIZE(0);  // Should not have entered S2

    // Set g2=true, send EV2 (guard passes, should transition to S2)
    this->sendCmd_SET_G2(0, 2, true);
    dispatchAll();
    invoke_to_schedIn2(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);
}

void Arg_Actions_ComponentTester::dispatchAll() 
{
    while (this->component.m_queue.getMessagesAvailable() > 0)
        this->component.doDispatch();
}

void Arg_Actions_ComponentTester::textLogIn(
    FwEventIdType id, //!< The event ID
    const Fw::Time& timeTag, //!< The time
    const Fw::LogSeverity severity, //!< The severity
    const Fw::TextLogString& text //!< The event string
) {
    TextLogEntry e = {id, timeTag, severity, text};
    printTextLogHistoryEntry(e, stdout);
}


}  // namespace Components
