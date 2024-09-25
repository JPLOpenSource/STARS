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

  signal EV1

  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    initial enter Diag
    junction J4 {
      if g1 enter OFF \
      else do { a1 } enter ON
    }
    on EV1 enter J4
  }

  state ON {
   entry do { OnEntry }
   exit do { OnExit }
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    initial enter Init
    on EV1 enter OFF
  }

  initial enter OFF
}
