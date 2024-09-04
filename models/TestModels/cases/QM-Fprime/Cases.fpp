state machine Cases {

  action OFFENTRY
  action OnEntry
  action DiagExit
  action OnExit
  action DiagEntry
  action A1
  action InitEntry
  action InitExit
  action offexit

  guard G1

  signal ev2
  signal EV1

  state on {
   entry do { OnEntry }
   exit do { OnExit }
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    on ev2 enter OFF
  }

  state OFF {
   entry do { OFFENTRY }
   exit do { offexit }
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    junction J7 {
      if G1 enter OFF \
      else do { A1 } enter on
    }
    on EV1
  }

  initial enter OFF
  initial enter Init
  initial enter Diag
}
