// ======================================================================
// \title  Simple_ComponentTester.cpp
// \author watney
// \brief  cpp file for Simple_Component component test harness implementation class
// ======================================================================

#include "Simple_ComponentTester.hpp"

namespace Components {

// ----------------------------------------------------------------------
// Construction and destruction
// ----------------------------------------------------------------------

Simple_ComponentTester ::Simple_ComponentTester()
    : Simple_ComponentGTestBase("Simple_ComponentTester", Simple_ComponentTester::MAX_HISTORY_SIZE),
      component("Simple_Component") {
    this->connectPorts();
    this->initComponents();
}

Simple_ComponentTester ::~Simple_ComponentTester() {
    this->component.deinit();
}

// ----------------------------------------------------------------------
// Tests
// ----------------------------------------------------------------------

void Simple_ComponentTester ::toDo() {
    dispatchAll();
    ASSERT_EQ(component.simpleState_getState(), Components::Simple_State::S1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(1);
    
    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.simpleState_getState(), Components::Simple_State::S2);

    invoke_to_schedIn(0, 0);
    dispatchAll();
    ASSERT_EQ(component.simpleState_getState(), Components::Simple_State::S1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(2);
}

void Simple_ComponentTester::dispatchAll() 
{
    while (this->component.m_queue.getMessagesAvailable() > 0)
        this->component.doDispatch();
}

void Simple_ComponentTester::textLogIn(
    FwEventIdType id, //!< The event ID
    const Fw::Time& timeTag, //!< The time
    const Fw::LogSeverity severity, //!< The severity
    const Fw::TextLogString& text //!< The event string
) {
    TextLogEntry e = {id, timeTag, severity, text};
    printTextLogHistoryEntry(e, stdout);
}


}  // namespace Components
