state machine Actions {

  action a2
  action s1Entry
  action s1Exit
  action s2Entry
  action s2Exit

  guard g1

  signal EV1

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    on EV1 if g1 enter S2
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    on EV1 do { a2 } enter S1
  }

  initial enter S1
}
