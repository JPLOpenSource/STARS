// ======================================================================
// \title  Simple_Component.cpp
// \author watney
// \brief  cpp file for Simple_Component component implementation class
// ======================================================================

#include "Simple_Component/Simple_Component.hpp"

namespace Components {

// ----------------------------------------------------------------------
// Component construction and destruction
// ----------------------------------------------------------------------

Simple_Component ::Simple_Component(const char* const compName) : Simple_ComponentComponentBase(compName) {}

Simple_Component ::~Simple_Component() {}

// ----------------------------------------------------------------------
// Handler implementations for commands
// ----------------------------------------------------------------------

void Simple_Component::schedIn_handler(
          FwIndexType portNum,
          U32 context
) {
    simpleState_sendSignal_EV1();
}


void Simple_Component::Components_Simple_action_s1Entry(
          SmId smId,
          Components_Simple::Signal signal
    ) {
        this->log_ACTIVITY_HI_s1EntryEvent();
    }

}  // namespace Components
