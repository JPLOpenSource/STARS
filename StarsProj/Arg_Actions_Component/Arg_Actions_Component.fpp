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