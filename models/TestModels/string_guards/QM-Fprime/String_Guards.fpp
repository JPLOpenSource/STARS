state machine String_Guards {

  action a5
  action a1
  action a4
  action farEntry
  action barExit
  action farExit
  action b2
  action a6
  action barEntry
  action initialAction

  guard g1
  guard g4
  guard g5

  signal Ev1
  signal Ev2

  state ON {
    state Bar {
     entry do { barEntry }
     exit do { barExit }
    }

    on Ev2 enter OFF
  }

  state OFF {
    state Far {
     entry do { farEntry }
     exit do { farExit }
    }

    junction J7 {
      if g1 do { b2 } enter J8 \
      else do { a1 } enter OFF
    }
    on Ev1
    on Ev2
  }

  initial do { initialAction } enter OFF
  initial enter Bar
  initial enter Far
}
