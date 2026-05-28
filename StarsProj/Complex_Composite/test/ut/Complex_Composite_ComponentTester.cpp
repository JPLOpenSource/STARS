// ======================================================================
// \title  Complex_Composite_ComponentTester.cpp
// \author watney
// \brief  cpp file for Complex_Composite_Component component test harness implementation class
// ======================================================================

#include "Complex_Composite_ComponentTester.hpp"

namespace Components {

// ----------------------------------------------------------------------
// Construction and destruction
// ----------------------------------------------------------------------

Complex_Composite_ComponentTester ::Complex_Composite_ComponentTester()
    : Complex_Composite_ComponentGTestBase("Complex_Composite_ComponentTester",
                                            Complex_Composite_ComponentTester::MAX_HISTORY_SIZE),
      component("Complex_Composite_Component") {
    this->connectPorts();
    this->initComponents();
}

Complex_Composite_ComponentTester ::~Complex_Composite_ComponentTester() {
    this->component.deinit();
}

// ----------------------------------------------------------------------
// Tests
// ----------------------------------------------------------------------

void Complex_Composite_ComponentTester::testAllTransitions() {
    dispatchAll();
    
    // Initial state: S1.S11.S111.s1111
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S1_S11_S111_s1111);
    
    // Verify init1 and entry actions were called
    ASSERT_EVENTS_init1Event_SIZE(1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(1);
    ASSERT_EVENTS_s11EntryEvent_SIZE(1);
    ASSERT_EVENTS_s111EntryEvent_SIZE(1);
    ASSERT_EVENTS_s1111EntryEvent_SIZE(1);
    
    clearHistory();
    
    // Test 1: S111 -> S12 via Ev1 (line 37 in PlantUML)
    // From s1111 (within S111), Ev1 transitions to S12.S121
    this->sendCmd_SEND_EV1(0, 0);
    dispatchAll();
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S1_S12_S121);
    ASSERT_EVENTS_s1111ExitEvent_SIZE(1);
    ASSERT_EVENTS_s111ExitEvent_SIZE(1);
    ASSERT_EVENTS_s11ExitEvent_SIZE(1);
    ASSERT_EVENTS_s12EntryEvent_SIZE(1);
    ASSERT_EVENTS_s121EntryEvent_SIZE(1);
    
    clearHistory();
    
    // Test 2: S12 -> S11 via Ev2 (line 36 in PlantUML)
    // From S12, Ev2 transitions back to S11.S111.s1111
    this->sendCmd_SEND_EV2(0, 1);
    dispatchAll();
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S1_S11_S111_s1111);
    ASSERT_EVENTS_s121ExitEvent_SIZE(1);
    ASSERT_EVENTS_s12ExitEvent_SIZE(1);
    ASSERT_EVENTS_s11EntryEvent_SIZE(1);
    ASSERT_EVENTS_s111EntryEvent_SIZE(1);
    ASSERT_EVENTS_s1111EntryEvent_SIZE(1);
    
    clearHistory();
    
    // Test 3: s1111 -> S2.S21 via Ev2 (line 33 in PlantUML - crosses top-level boundary)
    // From s1111, Ev2 transitions to S2.S21
    this->sendCmd_SEND_EV2(0, 2);
    dispatchAll();
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S2_S21);
    ASSERT_EVENTS_s1111ExitEvent_SIZE(1);
    ASSERT_EVENTS_s111ExitEvent_SIZE(1);
    ASSERT_EVENTS_s11ExitEvent_SIZE(1);
    ASSERT_EVENTS_s1ExitEvent_SIZE(1);
    ASSERT_EVENTS_s2EntryEvent_SIZE(1);
    ASSERT_EVENTS_s21EntryEvent_SIZE(1);
    
    clearHistory();
    
    // Test 4: S2 -> S1 via Ev1 (line 51 in PlantUML)
    // From S2, Ev1 transitions back to S1.S11.S111.s1111
    this->sendCmd_SEND_EV1(0, 3);
    dispatchAll();
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S1_S11_S111_s1111);
    ASSERT_EVENTS_s21ExitEvent_SIZE(1);
    ASSERT_EVENTS_s2ExitEvent_SIZE(1);
    ASSERT_EVENTS_s1EntryEvent_SIZE(1);
    ASSERT_EVENTS_s11EntryEvent_SIZE(1);
    ASSERT_EVENTS_s111EntryEvent_SIZE(1);
    ASSERT_EVENTS_s1111EntryEvent_SIZE(1);
    
    clearHistory();
    
    // Test 5: s1111 -> S12.S121 via Ev3 (line 34 in PlantUML)
    // From s1111, Ev3 transitions to S12.S121
    this->sendCmd_SEND_EV3(0, 4);
    dispatchAll();
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S1_S12_S121);
    ASSERT_EVENTS_s1111ExitEvent_SIZE(1);
    ASSERT_EVENTS_s111ExitEvent_SIZE(1);
    ASSERT_EVENTS_s11ExitEvent_SIZE(1);
    ASSERT_EVENTS_s12EntryEvent_SIZE(1);
    ASSERT_EVENTS_s121EntryEvent_SIZE(1);
    
    clearHistory();
    
    // Test 6: S121 -> S111 via Ev4 (line 35 in PlantUML)
    // From S121, Ev4 transitions back to S111.s1111
    this->sendCmd_SEND_EV4(0, 5);
    dispatchAll();
    ASSERT_EQ(component.complexCompositeState_getState(), Components::Complex_Composite_State::S1_S11_S111_s1111);
    ASSERT_EVENTS_s121ExitEvent_SIZE(1);
    ASSERT_EVENTS_s12ExitEvent_SIZE(1);
    ASSERT_EVENTS_s11EntryEvent_SIZE(1);
    ASSERT_EVENTS_s111EntryEvent_SIZE(1);
    ASSERT_EVENTS_s1111EntryEvent_SIZE(1);
}

// ----------------------------------------------------------------------
// Helper functions
// ----------------------------------------------------------------------

void Complex_Composite_ComponentTester::dispatchAll() 
{
    while (this->component.m_queue.getMessagesAvailable() > 0)
        this->component.doDispatch();
}

void Complex_Composite_ComponentTester::textLogIn(
    FwEventIdType id,
    const Fw::Time& timeTag,
    const Fw::LogSeverity severity,
    const Fw::TextLogString& text
) {
    TextLogEntry e = {id, timeTag, severity, text};
    printTextLogHistoryEntry(e, stdout);
}

}  // namespace Components
