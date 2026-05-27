// ======================================================================
// \title  Arg_Actions_ComponentTester.hpp
// \author watney
// \brief  hpp file for Arg_Actions_Component component test harness implementation class
// ======================================================================

#ifndef Components_Arg_Actions_ComponentTester_HPP
#define Components_Arg_Actions_ComponentTester_HPP

#include "Arg_Actions_Component/Arg_Actions_Component.hpp"
#include "Arg_Actions_Component/Arg_Actions_ComponentGTestBase.hpp"

namespace Components {

class Arg_Actions_ComponentTester final : public Arg_Actions_ComponentGTestBase {
  public:
    // ----------------------------------------------------------------------
    // Constants
    // ----------------------------------------------------------------------

    // Maximum size of histories storing events, telemetry, and port outputs
    static const FwSizeType MAX_HISTORY_SIZE = 10;

    // Instance ID supplied to the component instance under test
    static const FwEnumStoreType TEST_INSTANCE_ID = 0;

    // Queue depth supplied to the component instance under test
    static const FwSizeType TEST_INSTANCE_QUEUE_DEPTH = 10;

  public:
    // ----------------------------------------------------------------------
    // Construction and destruction
    // ----------------------------------------------------------------------

    //! Construct object Arg_Actions_ComponentTester
    Arg_Actions_ComponentTester();

    //! Destroy object Arg_Actions_ComponentTester
    ~Arg_Actions_ComponentTester();

  public:
    // ----------------------------------------------------------------------
    // Tests
    // ----------------------------------------------------------------------

    //! Test state transitions with EV1
    void testTransitions();

    //! Test state transitions with EV2
    void testEV2Transitions();

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
    Arg_Actions_Component component;
};

}  // namespace Components

#endif
