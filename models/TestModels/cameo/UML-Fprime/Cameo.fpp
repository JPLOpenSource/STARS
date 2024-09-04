state machine Cameo {

  action runningEntry
  action s2Entry
  action S1Exit
  action runningExit
  action a4
  action S1Entry
  action a1
  action a2
  action s3Exit
  action s3Entry
  action s2Exit

  guard guard4
  guard guard2
  guard guard
  guard guard3

  signal Ev5
  signal Ev4
  signal Ev1
  signal Ev3
  signal Ev2

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

    initial enter J5
    junction J5 {
      if guard4 enter StateS3 \
      else enter StateS2
    }
    on Ev5 enter Running
    on Ev4 do { a4 } enter J7
    on Ev3 enter J7
    on Ev1 if guard2 do { a1 } enter StateS1
  }

  initial enter J6
  junction J6 {
    if guard enter StateS1 \
    else enter Running
  }
  junction J7 {
    if guard3 enter StateS1 \
    else do { a2 } enter Running
  }
}
