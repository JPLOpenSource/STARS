module Components {
      include "Simple_State_Machine.fppi"

    @ Component wrap around Simple state machine
    active component Simple_Component {

        state machine instance simpleState: Simple 

        async input port schedIn: Svc.Sched

        event s1EntryEvent() severity activity high id 0 format "s1Entry Event"

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
