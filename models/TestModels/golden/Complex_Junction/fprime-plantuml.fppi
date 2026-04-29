state machine Complex_Junction {

  action DiagEntry
  action DiagExit
  action InitEntry
  action InitExit
  action OffEntry
  action OffExit
  action OnEntry
  action OnExit
  action a1
  action a2
  action a3
  action a4
  action a5
  action a6

  guard g1()
  guard g2()
  guard g3()

  signal Ev1

  initial enter OFF
  state OFF {
   entry do { OffEntry }
   exit do { OffExit }
    initial enter Diag
    on Ev1 enter J4
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

  choice J4 {
    if g1() do { a1 } enter OFF else do { a2 } enter J5
  }
  choice J5 {
    if g2() do { a5 } enter ON else do { a3 } enter J6
  }
  choice J6 {
    if g3() do { a6 } enter ON else do { a4 } enter OFF
  }
}
