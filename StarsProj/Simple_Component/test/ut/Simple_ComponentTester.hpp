// ======================================================================
// \title  Simple_ComponentTester.hpp
// \author watney
// \brief  hpp file for Simple_Component component test harness implementation class
// ======================================================================

#ifndef Components_Simple_ComponentTester_HPP
#define Components_Simple_ComponentTester_HPP

#include "Simple_Component/Simple_Component.hpp"
#include "Simple_Component/Simple_ComponentGTestBase.hpp"

namespace Components {

class Simple_ComponentTester final : public Simple_ComponentGTestBase {
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

    //! Construct object Simple_ComponentTester
    Simple_ComponentTester();

    //! Destroy object Simple_ComponentTester
    ~Simple_ComponentTester();

  public:
    // ----------------------------------------------------------------------
    // Tests
    // ----------------------------------------------------------------------

    //! To do
    void toDo();

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
    Simple_Component component;
};

}  // namespace Components

#endif
