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

void Arg_Actions_ComponentTester ::testTransitions() {
    // Initial state should be S1 after initialization
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(1);

    // Send EV1 (g1 toggles to true, guard passes, S1->S2)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);

    // Send EV1 from S2 (no guard, always transitions S2->S1)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(2);

    // Send EV1 again (g1 toggles to true, guard passes, S1->S2)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(2);

    // Send EV1 from S2 (transition S2->S1)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(3);
}

void Arg_Actions_ComponentTester ::testEV2Transitions() {
    // Initial state should be S1 after initialization
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    clearHistory();

    // Send EV2 (g2 toggles to true, guard passes, S1->S2)
    invoke_to_schedIn2(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S2);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);

    // Send EV1 from S2 to return to S1 (no guard, always transitions S2->S1)
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    clearHistory();

    // Send EV2 with g2=false (should stay in S1)
    invoke_to_schedIn2(0, 0);
    dispatchAll();
    ASSERT_EQ(component.argActionsState_getState(), Components::Arg_Actions_FP_State::S1);
    ASSERT_EVENTS_s2EntryEvent_SIZE(0);  // Should not have entered S2

    // Send EV2 with g2=true again (should transition to S2)
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
