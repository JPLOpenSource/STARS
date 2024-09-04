state machine Simple_Junction {

  action OnEntry
  action OffExit
  action DiagEntry
  action InitExit
  action DiagExit
  action a1
  action InitEntry
  action OffEntry
  action OnExit

  guard g1

  signal Ev1

  state ON {
   entry do { OnEntry }
   exit do { OnExit }
    state Init {
     entry do { InitEntry }
     exit do { InitExit }
    }

    on Ev1 enter OFF
  }

  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    junction J7 {
      if g1 enter OFF \
      else do { a1 } enter ON
    }
    on Ev1
  }

  initial enter OFF
  initial enter Init
  initial enter Diag
}
