state machine Complex_Junction {

  action InitExit
  action DiagExit
  action a2
  action a1
  action DiagEntry
  action OnExit
  action OffEntry
  action OffExit
  action InitEntry
  action OnEntry

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
      if g1 do { a1 } enter OFF \
      else do { a2 } enter J8
    }
    on Ev1
  }

  initial enter OFF
  initial enter Init
  initial enter Diag
}
