// ======================================================================
// \title  Complex_Composite_Component.hpp
// \author watney
// \brief  hpp file for Complex_Composite_Component component implementation class
// ======================================================================

#ifndef Components_Complex_Composite_Component_HPP
#define Components_Complex_Composite_Component_HPP

#include "Complex_Composite/Complex_Composite_ComponentComponentAc.hpp"

namespace Components {

class Complex_Composite_Component final : public Complex_Composite_ComponentComponentBase {
  public:
    // ----------------------------------------------------------------------
    // Component construction and destruction
    // ----------------------------------------------------------------------

    //! Construct Complex_Composite_Component object
    Complex_Composite_Component(const char* const compName  //!< The component name
    );

    //! Destroy Complex_Composite_Component object
    ~Complex_Composite_Component();

  private:
    // ----------------------------------------------------------------------
    // Handler implementations for commands
    // ----------------------------------------------------------------------

    //! Handler implementation for command SEND_EV1
    //!
    //! Command to send Ev1 signal
    void SEND_EV1_cmdHandler(FwOpcodeType opCode,  //!< The opcode
                             U32 cmdSeq            //!< The command sequence number
                             ) override;

    //! Handler implementation for command SEND_EV2
    //!
    //! Command to send Ev2 signal
    void SEND_EV2_cmdHandler(FwOpcodeType opCode,  //!< The opcode
                             U32 cmdSeq            //!< The command sequence number
                             ) override;

    //! Handler implementation for command SEND_EV3
    //!
    //! Command to send Ev3 signal
    void SEND_EV3_cmdHandler(FwOpcodeType opCode,  //!< The opcode
                             U32 cmdSeq            //!< The command sequence number
                             ) override;

    //! Handler implementation for command SEND_EV4
    //!
    //! Command to send Ev4 signal
    void SEND_EV4_cmdHandler(FwOpcodeType opCode,  //!< The opcode
                             U32 cmdSeq            //!< The command sequence number
                             ) override;

  private:
    // ----------------------------------------------------------------------
    // Implementations for internal state machine actions
    // ----------------------------------------------------------------------

    //! Implementation for action init1 of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_init1(SmId smId,  //!< The state machine id
                                                   Components_Complex_Composite::Signal signal  //!< The signal
                                                   ) override;

    //! Implementation for action s1111Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s1111Entry(SmId smId,  //!< The state machine id
                                                        Components_Complex_Composite::Signal signal  //!< The signal
                                                        ) override;

    //! Implementation for action s1111Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s1111Exit(SmId smId,  //!< The state machine id
                                                       Components_Complex_Composite::Signal signal  //!< The signal
                                                       ) override;

    //! Implementation for action s111Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s111Entry(SmId smId,  //!< The state machine id
                                                       Components_Complex_Composite::Signal signal  //!< The signal
                                                       ) override;

    //! Implementation for action s111Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s111Exit(SmId smId,  //!< The state machine id
                                                      Components_Complex_Composite::Signal signal  //!< The signal
                                                      ) override;

    //! Implementation for action s11Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s11Entry(SmId smId,  //!< The state machine id
                                                      Components_Complex_Composite::Signal signal  //!< The signal
                                                      ) override;

    //! Implementation for action s11Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s11Exit(SmId smId,  //!< The state machine id
                                                     Components_Complex_Composite::Signal signal  //!< The signal
                                                     ) override;

    //! Implementation for action s121Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s121Entry(SmId smId,  //!< The state machine id
                                                       Components_Complex_Composite::Signal signal  //!< The signal
                                                       ) override;

    //! Implementation for action s121Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s121Exit(SmId smId,  //!< The state machine id
                                                      Components_Complex_Composite::Signal signal  //!< The signal
                                                      ) override;

    //! Implementation for action s12Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s12Entry(SmId smId,  //!< The state machine id
                                                      Components_Complex_Composite::Signal signal  //!< The signal
                                                      ) override;

    //! Implementation for action s12Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s12Exit(SmId smId,  //!< The state machine id
                                                     Components_Complex_Composite::Signal signal  //!< The signal
                                                     ) override;

    //! Implementation for action s1Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s1Entry(SmId smId,  //!< The state machine id
                                                     Components_Complex_Composite::Signal signal  //!< The signal
                                                     ) override;

    //! Implementation for action s1Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s1Exit(SmId smId,  //!< The state machine id
                                                    Components_Complex_Composite::Signal signal  //!< The signal
                                                    ) override;

    //! Implementation for action s21Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s21Entry(SmId smId,  //!< The state machine id
                                                      Components_Complex_Composite::Signal signal  //!< The signal
                                                      ) override;

    //! Implementation for action s21Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s21Exit(SmId smId,  //!< The state machine id
                                                     Components_Complex_Composite::Signal signal  //!< The signal
                                                     ) override;

    //! Implementation for action s2Entry of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s2Entry(SmId smId,  //!< The state machine id
                                                     Components_Complex_Composite::Signal signal  //!< The signal
                                                     ) override;

    //! Implementation for action s2Exit of state machine Components_Complex_Composite
    void Components_Complex_Composite_action_s2Exit(SmId smId,  //!< The state machine id
                                                    Components_Complex_Composite::Signal signal  //!< The signal
                                                    ) override;
};

}  // namespace Components

#endif
