// ======================================================================
// \title  Simple_Component.hpp
// \author watney
// \brief  hpp file for Simple_Component component implementation class
// ======================================================================

#ifndef Components_Simple_Component_HPP
#define Components_Simple_Component_HPP

#include "Simple_Component/Simple_ComponentComponentAc.hpp"

namespace Components {

class Simple_Component final : public Simple_ComponentComponentBase {
  public:
    // ----------------------------------------------------------------------
    // Component construction and destruction
    // ----------------------------------------------------------------------

    //! Construct Simple_Component object
    Simple_Component(const char* const compName  //!< The component name
    );

    //! Destroy Simple_Component object
    ~Simple_Component();

  private:

    void schedIn_handler(
          FwIndexType portNum,
          U32 context
    ) override;

    // ----------------------------------------------------------------------
    // State machine implementation functions
    // ----------------------------------------------------------------------

    void Components_Simple_action_s1Entry(
          SmId smId,
          Components_Simple::Signal signal
    ) override;

  };

}  // namespace Components

#endif
