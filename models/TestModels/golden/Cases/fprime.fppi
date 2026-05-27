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

  initial enter OFF
  state OFF {
   entry do { OFFENTRY }
   exit do { offexit }
    initial enter Diag
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    on EV1 enter J0
  }

  state on_state {
   entry do { OnEntry }
   exit do { OnExit }
    initial enter Init
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    on ev2 enter OFF
  }

  choice J0 {
    if G1 enter OFF else do { A1 } enter on_state
  }
}
