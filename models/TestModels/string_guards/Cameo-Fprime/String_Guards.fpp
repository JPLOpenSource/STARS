state machine String_Guards {

  action a4
  action farExit
  action farEntry
  action b4
  action a1
  action a2
  action a6
  action a5
  action barExit
  action b2
  action barEntry
  action initialAction
  action a3
  action b3

  guard g1
  guard g3
  guard g5
  guard g4
  guard g2

  signal Ev1
  signal Ev2

  state OFF {
    state Far {
     entry do { farEntry }
     exit do { farExit }
    }

    initial enter Far
    on Ev1 enter J_19_0_3_9120299_1629493344508_32376_42347
    on Ev2 enter J_19_0_3_9120299_1629493648102_349596_42609
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
  junction J_19_0_3_9120299_1629493344508_32376_42347 {
    if g1 do { b2 } enter J_19_0_3_9120299_1629493399322_672823_42359 \
    else do { a1 } enter OFF
  }
  junction J_19_0_3_9120299_1629493399322_672823_42359 {
    if g2 do { b3 } enter J_19_0_3_9120299_1629493464056_47865_42441 \
    else do { a2 } enter OFF
  }
  junction J_19_0_3_9120299_1629493464056_47865_42441 {
    if g3 do { b4 } enter ON \
    else do { a3 } enter OFF
  }
  junction J_19_0_3_9120299_1629493671793_144012_42620 {
    if g5 do { a4 } enter OFF \
    else do { a6 } enter ON
  }
}
