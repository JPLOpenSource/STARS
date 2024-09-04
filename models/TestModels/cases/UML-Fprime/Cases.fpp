state machine Cases {

  action DiagEntry
  action DiagExit
  action offexit
  action OnExit
  action OnEntry
  action A1
  action InitEntry
  action OFFENTRY
  action InitExit

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
    on EV1 enter J5
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
  junction J5 {
    if G1 enter OFF \
    else do { A1 } enter on
  }
}
