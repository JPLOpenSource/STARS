state machine String_Guards {

  action a1
  action a2
  action a3
  action a4
  action a5
  action a6
  action b2
  action b3
  action b4
  action barEntry
  action barExit
  action farEntry
  action farExit
  action initialAction

  guard g1
  guard g2
  guard g3
  guard g4
  guard g5

  signal Ev1
  signal Ev2

  state OFF {
    state Far {
     entry do { farEntry }
     exit do { farExit }
    }

    initial enter Far
    junction J7 {
      if g1 do { b2 } enter J8 \
      else do { a1 } enter OFF
    }
    junction J8 {
      if g2 do { b3 } enter J9 \
      else do { a2 } enter OFF
    }
    junction J9 {
      if g3 do { b4 } enter ON \
      else do { a3 } enter OFF
    }
    junction J10 {
      if g5 do { a4 } enter OFF \
      else do { a6 } enter ON
    }
    on Ev1 enter J7
    on Ev2 if g4 do { a5 } enter J10
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
}
