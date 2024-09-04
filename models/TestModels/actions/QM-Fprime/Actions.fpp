state machine Actions {

  action a2
  action s2Entry
  action s2Exit
  action s1Exit
  action s1Entry

  guard g1

  signal EV1

  state S1 {
   entry do { s1Entry }
   exit do { s1Exit }
    on EV1
  }

  state S2 {
   entry do { s2Entry }
   exit do { s2Exit }
    on EV1 do { a2 } enter S1
  }

  initial enter S1
}
