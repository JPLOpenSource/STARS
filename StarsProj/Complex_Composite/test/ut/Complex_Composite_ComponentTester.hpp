// ======================================================================
// \title  Complex_Composite_ComponentTester.hpp
// \author watney
// \brief  hpp file for Complex_Composite_Component component test harness implementation class
// ======================================================================

#ifndef Components_Complex_Composite_ComponentTester_HPP
#define Components_Complex_Composite_ComponentTester_HPP

#include "Complex_Composite/Complex_Composite_Component.hpp"
#include "Complex_Composite/Complex_Composite_ComponentGTestBase.hpp"

namespace Components {

class Complex_Composite_ComponentTester final : public Complex_Composite_ComponentGTestBase {
  public:
    // ----------------------------------------------------------------------
    // Constants
    // ----------------------------------------------------------------------

    // Maximum size of histories storing events, telemetry, and port outputs
    static const FwSizeType MAX_HISTORY_SIZE = 50;

    // Instance ID supplied to the component instance under test
    static const FwEnumStoreType TEST_INSTANCE_ID = 0;

    // Queue depth supplied to the component instance under test
    static const FwSizeType TEST_INSTANCE_QUEUE_DEPTH = 10;

  public:
    // ----------------------------------------------------------------------
    // Construction and destruction
    // ----------------------------------------------------------------------

    //! Construct object Complex_Composite_ComponentTester
    Complex_Composite_ComponentTester();

    //! Destroy object Complex_Composite_ComponentTester
    ~Complex_Composite_ComponentTester();

  public:
    // ----------------------------------------------------------------------
    // Tests
    // ----------------------------------------------------------------------

    //! Test all state transitions
    void testAllTransitions();

  private:
    // ----------------------------------------------------------------------
    // Helper functions
    // ----------------------------------------------------------------------

    //! Connect ports
    void connectPorts();

    //! Initialize components
    void initComponents();

    void textLogIn(
      FwEventIdType id, //!< The event ID
      const Fw::Time& timeTag, //!< The time
      const Fw::LogSeverity severity, //!< The severity
      const Fw::TextLogString& text //!< The event string
    );
    
    void dispatchAll(); 

  private:
    // ----------------------------------------------------------------------
    // Member variables
    // ----------------------------------------------------------------------

    //! The component under test
    Complex_Composite_Component component;
};

}  // namespace Components

#endif
