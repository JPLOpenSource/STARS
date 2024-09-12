state machine Device {

  action calibratingEntry
  action calibratingExit
  action diagnosticsEntry
  action diagnosticsExit
  action doCalibrate
  action doDiagnostics
  action doSafe
  action idleEntry
  action idleExit
  action initDevice
  action initExit
  action motorControl
  action offEntry
  action offExit
  action recoveryExit
  action reportFault
  action shutOffMotor
  action startMotor
  action startRecovery
  action turnOffPower
  action turnOnPower

  guard calibrateReady

  signal Calibrate
  signal Complete
  signal Drive
  signal Fault
  signal POR
  signal PowerOff
  signal PowerOn
  signal RTI
  signal Resume
  signal Stop

  state On {
   entry do { turnOnPower }
   exit do { turnOffPower }
    state Initializing {
     entry do { initDevice }
     exit do { initExit }
      on Complete enter Idle
    }

    state Driving {
     entry do { startMotor }
     exit do { shutOffMotor }
      on Stop enter Idle
      on RTI do { motorControl }
    }

    state Calibrating {
     entry do { calibratingEntry }
     exit do { calibratingExit }
      on Complete enter Idle
      on Fault do { reportFault } enter Idle
      on RTI do { doCalibrate }
    }

    state Idle {
     entry do { idleEntry }
     exit do { idleExit }
      on Drive enter Driving
      on Calibrate if calibrateReady enter Calibrating
    }

    initial enter Initializing
    on PowerOff enter Off
    on Fault do { reportFault } enter Recovery
    on POR enter On
  }

  state Off {
   entry do { offEntry }
   exit do { offExit }
    on PowerOn enter On
  }

  state Recovery {
   entry do { startRecovery }
   exit do { recoveryExit }
    on Complete enter Diagnostics
    on RTI do { doSafe }
  }

  state Diagnostics {
   entry do { diagnosticsEntry }
   exit do { diagnosticsExit }
    on Resume enter On
    on RTI do { doDiagnostics }
  }

  initial enter Off
}
