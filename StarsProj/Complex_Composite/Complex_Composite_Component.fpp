module Components {
    include "Complex_Composite_State_Machine.fppi"

    @ Component wrapper for Complex_Composite state machine
    active component Complex_Composite_Component {

        state machine instance complexCompositeState: Complex_Composite

        event init1Event() severity activity high id 0 format "init1 action"
        event s1EntryEvent() severity activity high id 1 format "s1Entry action"
        event s1ExitEvent() severity activity high id 2 format "s1Exit action"
        event s11EntryEvent() severity activity high id 3 format "s11Entry action"
        event s11ExitEvent() severity activity high id 4 format "s11Exit action"
        event s111EntryEvent() severity activity high id 5 format "s111Entry action"
        event s111ExitEvent() severity activity high id 6 format "s111Exit action"
        event s1111EntryEvent() severity activity high id 7 format "s1111Entry action"
        event s1111ExitEvent() severity activity high id 8 format "s1111Exit action"
        event s12EntryEvent() severity activity high id 9 format "s12Entry action"
        event s12ExitEvent() severity activity high id 10 format "s12Exit action"
        event s121EntryEvent() severity activity high id 11 format "s121Entry action"
        event s121ExitEvent() severity activity high id 12 format "s121Exit action"
        event s2EntryEvent() severity activity high id 13 format "s2Entry action"
        event s2ExitEvent() severity activity high id 14 format "s2Exit action"
        event s21EntryEvent() severity activity high id 15 format "s21Entry action"
        event s21ExitEvent() severity activity high id 16 format "s21Exit action"

        @ Command to send Ev1 signal
        async command SEND_EV1() opcode 0

        @ Command to send Ev2 signal
        async command SEND_EV2() opcode 1

        @ Command to send Ev3 signal
        async command SEND_EV3() opcode 2

        @ Command to send Ev4 signal
        async command SEND_EV4() opcode 3

        ###############################################################################
        # Standard AC Ports: Required for Channels, Events, Commands, and Parameters  #
        ###############################################################################
        @ Port for requesting the current time
        time get port timeCaller

        @ Enables command handling
        import Fw.Command

        @ Enables event handling
        import Fw.Event

    }
}
