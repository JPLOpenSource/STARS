# Define a basic state machine event type
# Only contains the required state machine ID and an event signal,
# no payload data
struct SMEvents {
    smId : U32
    eventSignal : U32
}

# Start of the state machine definition
state machine Device {

    event RTI: SMEvents
    event Complete: SMEvents
    event Calibrate: SMEvents
    event Fault: SMEvents
    event Drive: SMEvents
    event Stop: SMEvents
    event Resume: SMEvents
    event POR: SMEvents

    state Off {
        Entry: offEntry()
        Exit: offExit()
    }

    state On {
        Entry: turnOnPower()
        Exit: turnOffPower()

        state Initializing {
            Entry: initDevice()
            Exit: initExit()
        }

        state Idle {
            Entry: idleEntry()
            Exit: idleExit()
        }

        state Calibrating {
            Entry: calibratingEntry()
            Exit: calibratingExit()

            guard doCalibrate: SMEvents
            Internal: event RTI
                      guard doCalibrate
        }

        state Driving {
            Entry: startMotor()
            Exit: shutOffMotor()

            action motorControl: SMEvents
            Internal: event RTI
                      action motorControl
        }

        [*] --> Initializing

        Initializing --> Idle: event Complete

        Idle --> Driving: event Drive

        guard calibrateReady: SMEvents
        Idle --> Calibrating: event Calibrate
                              guard calibrateReady

        action reportFault: SMEvents
        Calibrating --> Idle: event Fault
                              action reportFault

        Calibrating --> Idle: event Complete

        Driving --> Idle: event Stop
    }

    state Recovery {
        Entry: startRecovery()
        Exit: recoveryExit()

        action doSafe: SMEvents
        Internal: event RTI
                  action doSafe
    }

    state Diagnostics {
        Entry: diagnosticsEntry()
        Exit: diagnosticsExit()

        action doDiagnostics: SMEvents
        Internal: event RTI
                  action: doDiagnostics
    }
 
    [*] --> Off
 
    Off --> On: event q

    On --> Off: event PowerOff

    action reportFault: SMEvents
    On --> Recovery: event Fault
                     action reportFault

    Diagnostics --> On: event Resume

    Recovery --> Diagnostics: event Complete

    On --> On: event POR
}