state machine Simple_Junction {

  action OnEntry
  action a1
  action OnExit
  action DiagEntry
  action OffEntry
  action OffExit
  action InitEntry
  action InitExit
  action DiagExit

  guard g1

  signal Ev1

  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    state Diag {
     entry do { DiagEntry }
     exit do { DiagExit }
    }

    initial enter Diag
    on Ev1 enter J_19_0_3_9120299_1628896586656_557397_42413
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
  junction J_19_0_3_9120299_1628896586656_557397_42413 {
    if g1 enter OFF \
    else do { a1 } enter ON
  }
}
