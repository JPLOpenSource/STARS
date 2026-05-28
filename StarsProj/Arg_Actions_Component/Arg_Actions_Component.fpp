module Components {
    include "Arg_Actions_FP_State_Machine.fppi"

    @ Component wrapper for Arg_Actions_FP state machine
    active component Arg_Actions_Component {

        state machine instance argActionsState: Arg_Actions_FP

        async input port schedIn: Svc.Sched
        async input port schedIn2: Svc.Sched

        event s1EntryEvent() severity activity high id 0 format "s1Entry Event"
        event s1Entry2Event() severity activity high id 1 format "s1Entry2 Event"
        event s1ExitEvent() severity activity high id 2 format "s1Exit Event"
        event s1Exit2Event() severity activity high id 3 format "s1Exit2 Event"
        event s2EntryEvent() severity activity high id 4 format "s2Entry Event"
        event s2Entry2Event() severity activity high id 5 format "s2Entry2 Event"
        event s2ExitEvent() severity activity high id 6 format "s2Exit Event"
        event s2Exit2Event() severity activity high id 7 format "s2Exit2 Event"
        event a1Event(value: U16) severity activity high id 8 format "a1 action with value {}"
        event a2Event() severity activity high id 9 format "a2 Event"
        event fooEvent() severity activity high id 10 format "foo Event"
        event g1GuardEvent(value: U16) severity activity high id 11 format "g1 guard called with value {}"

        @ Command to set a test value
        async command TEST_CMD(value: U16) opcode 0

        @ Command to set guard g1 value
        async command SET_G1(value: bool) opcode 1

        @ Command to set guard g2 value
        async command SET_G2(value: bool) opcode 2

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