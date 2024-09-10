state machine Cameo {

  action S1Entry
  action S1Exit
  action a1
  action a2
  action a4
  action runningEntry
  action runningExit
  action s2Entry
  action s2Exit
  action s3Entry
  action s3Exit

  guard guard
  guard guard2
  guard guard3
  guard guard4

  signal Ev1
  signal Ev2
  signal Ev3
  signal Ev4
  signal Ev5

  state StateS1 {
   entry do { S1Entry }
   exit do { S1Exit }
    on Ev2 do { a2 } enter Running
  }

  state Running {
   entry do { runningEntry }
   exit do { runningExit }
    state StateS2 {
     entry do { s2Entry }
     exit do { s2Exit }
    }

    state StateS3 {
     entry do { s3Entry }
     exit do { s3Exit }
    }

    initial enter J_19_0_3_9120299_1630629321491_798841_42213
    junction J_19_0_3_9120299_1630629321491_798841_42213 {
      if guard4 enter StateS3 \
      else enter StateS2
    }
    on Ev1 if guard2 do { a1 } enter StateS1
    on Ev3 enter J_19_0_3_9120299_1630543524955_285094_42225
    on Ev4 do { a4 } enter J_19_0_3_9120299_1630543524955_285094_42225
    on Ev5 enter Running
  }

  initial enter J_19_0_3_9120299_1629507981810_800370_42165
  junction J_19_0_3_9120299_1629507981810_800370_42165 {
    if guard enter StateS1 \
    else enter Running
  }
  junction J_19_0_3_9120299_1630543524955_285094_42225 {
    if guard3 enter StateS1 \
    else do { a2 } enter Running
  }
}
