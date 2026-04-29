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

  guard g1()

  signal Ev1

  initial enter OFF
  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    initial enter Diag
    on Ev1 enter J0
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

  }

  state ON {
   entry do { OnEntry }
   exit do { OnExit }
    initial enter Init
    on Ev1 enter OFF
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

  }

  choice J0 {
    if g1() enter OFF else do { a1 } enter ON
  }
}
