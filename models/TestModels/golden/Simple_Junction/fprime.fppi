state machine Simple_Junction {

  action DiagEntry
  action DiagExit
  action InitEntry
  action InitExit
  action OffEntry
  action OffExit
  action OnEntry
  action OnExit
  action a1

  guard g1

  signal Ev1

  initial enter OFF
  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    initial enter Diag
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    on Ev1 enter J0
  }

  state ON {
   entry do { OnEntry }
   exit do { OnExit }
    initial enter Init
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    on Ev1 enter OFF
  }

  choice J0 {
    if g1 enter OFF else do { a1 } enter ON
  }
}
