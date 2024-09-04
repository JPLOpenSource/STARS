state machine Simple_Junction {

  action InitEntry
  action DiagExit
  action OnExit
  action InitExit
  action OffExit
  action DiagEntry
  action a1
  action OnEntry
  action OffEntry

  guard g1

  signal Ev1
  signal EV1

  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    initial enter Diag
    on EV1 enter J5
  }

  state ON {
   entry do { OnEntry }
   exit do { OnExit }
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    initial enter Init
    on Ev1 enter OFF
  }

  initial enter OFF
  junction J5 {
    if g1 enter OFF \
    else do { a1 } enter ON
  }
}
