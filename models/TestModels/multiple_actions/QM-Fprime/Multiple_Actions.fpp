state machine Multiple_Actions {

  action s2Entry2
  action a1
  action s1Entry
  action s1Exit2
  action a2
  action s2Exit
  action s2Entry
  action s1Entry2
  action s2Exit2
  action s1Exit

  guard g1

  signal EV1

  state S1 {
   entry do { s1Entry, s1Entry2 }
   exit do { s1Exit, s1Exit2 }
    on EV1
  }

  state S2 {
   entry do { s2Entry, s2Entry2 }
   exit do { s2Exit, s2Exit2 }
    on EV1 do { a1, a2 } enter S1
  }

  initial enter S1
}
