state machine Complex_Junction {

  action a3
  action a2
  action a5
  action a6
  action OnExit
  action InitExit
  action a4
  action InitEntry
  action OffEntry
  action a1
  action DiagExit
  action OnEntry
  action DiagEntry
  action OffExit

  guard g1
  guard g2
  guard g3

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
    if g1 do { a1 } enter OFF \
    else do { a2 } enter J_19_0_3_9120299_1629149081411_589697_42191
  }
  junction J_19_0_3_9120299_1629149081411_589697_42191 {
    if g2 do { a5 } enter ON \
    else do { a3 } enter J_19_0_3_9120299_1629149102573_951989_42198
  }
  junction J_19_0_3_9120299_1629149102573_951989_42198 {
    if g3 do { a6 } enter ON \
    else do { a4 } enter OFF
  }
}
