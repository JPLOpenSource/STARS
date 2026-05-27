// ======================================================================
// \title  Arg_Actions_Component.hpp
// \author watney
// \brief  hpp file for Arg_Actions_Component component implementation class
// ======================================================================

#ifndef Components_Arg_Actions_Component_HPP
#define Components_Arg_Actions_Component_HPP

#include "Arg_Actions_Component/Arg_Actions_ComponentComponentAc.hpp"

namespace Components {

class Arg_Actions_Component final : public Arg_Actions_ComponentComponentBase {
  public:
    // ----------------------------------------------------------------------
    // Component construction and destruction
    // ----------------------------------------------------------------------

    //! Construct Arg_Actions_Component object
    Arg_Actions_Component(const char* const compName  //!< The component name
    );

    //! Destroy Arg_Actions_Component object
    ~Arg_Actions_Component();

  private:
    // ----------------------------------------------------------------------
    // Handler implementations for typed input ports
    // ----------------------------------------------------------------------

    //! Handler implementation for schedIn
    void schedIn_handler(FwIndexType portNum,  //!< The port number
                         U32 context           //!< The call order
                         ) override;

    //! Handler implementation for schedIn2
    void schedIn2_handler(FwIndexType portNum,  //!< The port number
                          U32 context           //!< The call order
                          ) override;

  private:
    // ----------------------------------------------------------------------
    // Implementations for internal state machine actions
    // ----------------------------------------------------------------------

    //! Implementation for action a1 of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_a1(SmId smId,                                 //!< The state machine id
                                             Components_Arg_Actions_FP::Signal signal,  //!< The signal
                                             U16 value                                  //!< The value
                                             ) override;

    //! Implementation for action a2 of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_a2(SmId smId,                                //!< The state machine id
                                             Components_Arg_Actions_FP::Signal signal  //!< The signal
                                             ) override;

    //! Implementation for action foo of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_foo(SmId smId,                                //!< The state machine id
                                              Components_Arg_Actions_FP::Signal signal  //!< The signal
                                              ) override;

    //! Implementation for action s1Entry of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s1Entry(SmId smId,                                //!< The state machine id
                                                  Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                  ) override;

    //! Implementation for action s1Entry2 of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s1Entry2(SmId smId,                                //!< The state machine id
                                                   Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                   ) override;

    //! Implementation for action s1Exit of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s1Exit(SmId smId,                                //!< The state machine id
                                                 Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                 ) override;

    //! Implementation for action s1Exit2 of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s1Exit2(SmId smId,                                //!< The state machine id
                                                  Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                  ) override;

    //! Implementation for action s2Entry of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s2Entry(SmId smId,                                //!< The state machine id
                                                  Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                  ) override;

    //! Implementation for action s2Entry2 of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s2Entry2(SmId smId,                                //!< The state machine id
                                                   Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                   ) override;

    //! Implementation for action s2Exit of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s2Exit(SmId smId,                                //!< The state machine id
                                                 Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                 ) override;

    //! Implementation for action s2Exit2 of state machine Components_Arg_Actions_FP
    void Components_Arg_Actions_FP_action_s2Exit2(SmId smId,                                //!< The state machine id
                                                  Components_Arg_Actions_FP::Signal signal  //!< The signal
                                                  ) override;

  private:
    // ----------------------------------------------------------------------
    // Implementations for internal state machine guards
    // ----------------------------------------------------------------------

    //! Implementation for guard g1 of state machine Components_Arg_Actions_FP
    bool Components_Arg_Actions_FP_guard_g1(SmId smId,                                //!< The state machine id
                                            Components_Arg_Actions_FP::Signal signal, //!< The signal
                                            U16 value                                 //!< The value
    ) const override;

    //! Implementation for guard g2 of state machine Components_Arg_Actions_FP
    bool Components_Arg_Actions_FP_guard_g2(SmId smId,                                //!< The state machine id
                                            Components_Arg_Actions_FP::Signal signal  //!< The signal
    ) const override;
  private:
    // ----------------------------------------------------------------------
    // Member variables for guard state
    // ----------------------------------------------------------------------
    bool m_g1Value;
    bool m_g2Value;
    U32 m_evCount;

};

}  // namespace Components

#endif
