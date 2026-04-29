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

  guard guard()
  guard guard2
  guard guard3()
  guard guard4()

  signal Ev1
  signal Ev2
  signal Ev3
  signal Ev4
  signal Ev5

  initial enter J5
  state Running {
   entry do { runningEntry }
   exit do { runningExit }
    initial enter J4
    on Ev1 if guard2 do { a1 } enter StateS1
    on Ev3 enter J6
    on Ev4 do { a4 } enter J6
    on Ev5 enter Running
    state StateS2 {
     entry do { s2Entry }
     exit do { s2Exit }
    }

    state StateS3 {
     entry do { s3Entry }
     exit do { s3Exit }
    }

    choice J4 {
      if guard4() enter StateS3 else enter StateS2
    }
  }

  state StateS1 {
   entry do { S1Entry }
   exit do { S1Exit }
    on Ev2 do { a2 } enter Running
  }

  choice J5 {
    if guard() enter StateS1 else enter Running
  }
  choice J6 {
    if guard3() enter StateS1 else do { a2 } enter Running
  }
}
