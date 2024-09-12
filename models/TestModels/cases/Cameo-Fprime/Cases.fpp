state machine Cases {

  action A1
  action DiagEntry
  action DiagExit
  action InitEntry
  action InitExit
  action OFFENTRY
  action OnEntry
  action OnExit
  action offexit

  guard G1

  signal EV1
  signal ev2

  state OFF {
   entry do { OFFENTRY }
   exit do { offexit }
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    initial enter Diag
    on EV1 enter J_19_0_3_9120299_1629496586218_255778_42420
  }

  state on {
   entry do { OnEntry }
   exit do { OnExit }
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    initial enter Init
    on ev2 enter OFF
  }

  initial enter OFF
  junction J_19_0_3_9120299_1629496586218_255778_42420 {
    if G1 enter OFF \
    else do { A1 } enter on
  }
}
