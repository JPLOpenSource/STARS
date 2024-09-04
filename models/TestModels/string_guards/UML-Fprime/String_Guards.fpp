state machine String_Guards {

  action farEntry
  action initialAction
  action barEntry
  action a1
  action a6
  action a5
  action farExit
  action a3
  action a4
  action a2
  action b4
  action barExit
  action b2
  action b3

  guard g1
  guard g3
  guard g5
  guard g2
  guard g4

  signal Ev2
  signal Ev1

  state OFF {
    state Far {
     entry do { farEntry }
     exit do { farExit }
    }

    initial enter Far
    on Ev1 enter J5
    on Ev2 enter J8
  }

  state ON {
    state Bar {
     entry do { barEntry }
     exit do { barExit }
    }

    initial enter Bar
    on Ev2 enter OFF
  }

  initial do { initialAction } enter OFF
  junction J5 {
    if g1 do { b2 } enter J6 \
    else do { a1 } enter OFF
  }
  junction J6 {
    if g2 do { b3 } enter J7 \
    else do { a2 } enter OFF
  }
  junction J7 {
    if g3 do { b4 } enter ON \
    else do { a3 } enter OFF
  }
  junction J9 {
    if g5 do { a4 } enter OFF \
    else do { a6 } enter ON
  }
}
